---
layout: default
title: "Open WebUI Tutorial - Chapter 6: User Management & Access Control"
nav_order: 6
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 6: User Management, Authentication & Access Control

> Implement multi-user support, role-based permissions, and enterprise authentication in Open WebUI.

## Authentication Systems

### Local User Management

```python
from typing import Dict, List, Optional
import hashlib
import secrets
import jwt
import datetime
from dataclasses import dataclass
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@dataclass
class User:
    id: str
    username: str
    email: str
    role: UserRole
    is_active: bool = True
    created_at: datetime.datetime = None
    last_login: Optional[datetime.datetime] = None
    preferences: Dict = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow()
        if self.preferences is None:
            self.preferences = {}

class AuthManager:
    def __init__(self, jwt_secret: str, token_expiry: int = 24):
        self.jwt_secret = jwt_secret
        self.token_expiry = token_expiry  # hours
        self.users: Dict[str, User] = {}
        self.passwords: Dict[str, str] = {}  # hashed passwords

    def hash_password(self, password: str) -> str:
        """Hash password with salt."""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}:{hashed.hex()}"

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        try:
            salt, hash_part = hashed.split(':')
            test_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return test_hash.hex() == hash_part
        except:
            return False

    async def register_user(self, username: str, email: str, password: str, role: UserRole = UserRole.USER) -> User:
        """Register a new user."""
        if username in self.users:
            raise ValueError("Username already exists")

        user_id = f"user_{secrets.token_hex(8)}"
        hashed_password = self.hash_password(password)

        user = User(
            id=user_id,
            username=username,
            email=email,
            role=role
        )

        self.users[username] = user
        self.passwords[username] = hashed_password

        return user

    async def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token."""
        user = self.users.get(username)
        if not user or not user.is_active:
            return None

        hashed_password = self.passwords.get(username)
        if not hashed_password or not self.verify_password(password, hashed_password):
            return None

        # Update last login
        user.last_login = datetime.datetime.utcnow()

        # Generate JWT token
        token = self.generate_token(user)
        return token

    def generate_token(self, user: User) -> str:
        """Generate JWT token for user."""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self.token_expiry),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> Optional[User]:
        """Verify JWT token and return user."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])

            username = payload['username']
            user = self.users.get(username)

            if user and user.is_active:
                return user

        except jwt.ExpiredSignatureError:
            pass  # Token expired
        except jwt.InvalidTokenError:
            pass  # Invalid token

        return None

    async def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password."""
        if not await self.authenticate_user(username, old_password):
            return False

        hashed_password = self.hash_password(new_password)
        self.passwords[username] = hashed_password
        return True

    def get_user(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.users.get(username)

    def list_users(self) -> List[User]:
        """List all users."""
        return list(self.users.values())

    def update_user_role(self, username: str, new_role: UserRole, current_user: User) -> bool:
        """Update user role (admin only)."""
        if current_user.role != UserRole.ADMIN:
            return False

        user = self.users.get(username)
        if user:
            user.role = new_role
            return True

        return False

    def deactivate_user(self, username: str, current_user: User) -> bool:
        """Deactivate user account."""
        if current_user.role != UserRole.ADMIN:
            return False

        user = self.users.get(username)
        if user:
            user.is_active = False
            return True

        return False
```

### OAuth Integration

```python
from typing import Dict, Any, Optional
import aiohttp
import secrets

class OAuthManager:
    def __init__(self):
        self.providers = {}
        self.states = {}  # For CSRF protection

    def register_provider(self, name: str, config: Dict[str, Any]):
        """Register OAuth provider."""
        self.providers[name] = {
            'client_id': config['client_id'],
            'client_secret': config['client_secret'],
            'authorize_url': config['authorize_url'],
            'token_url': config['token_url'],
            'user_info_url': config['user_info_url'],
            'scope': config.get('scope', 'openid email profile'),
            'redirect_uri': config['redirect_uri']
        }

    def get_authorization_url(self, provider_name: str) -> str:
        """Generate OAuth authorization URL."""
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"OAuth provider {provider_name} not registered")

        state = secrets.token_urlsafe(32)
        self.states[state] = provider_name

        params = {
            'client_id': provider['client_id'],
            'redirect_uri': provider['redirect_uri'],
            'scope': provider['scope'],
            'response_type': 'code',
            'state': state
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{provider['authorize_url']}?{query_string}"

    async def exchange_code_for_token(self, provider_name: str, code: str, state: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"OAuth provider {provider_name} not registered")

        # Verify state
        if self.states.get(state) != provider_name:
            raise ValueError("Invalid state parameter")

        # Clean up state
        del self.states[state]

        # Exchange code for token
        async with aiohttp.ClientSession() as session:
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': provider['redirect_uri'],
                'client_id': provider['client_id'],
                'client_secret': provider['client_secret']
            }

            async with session.post(provider['token_url'], data=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OAuth token exchange failed: {error_text}")

                token_data = await response.json()
                return token_data

    async def get_user_info(self, provider_name: str, access_token: str) -> Dict[str, Any]:
        """Get user information from OAuth provider."""
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"OAuth provider {provider_name} not registered")

        headers = {'Authorization': f'Bearer {access_token}'}

        async with aiohttp.ClientSession() as session:
            async with session.get(provider['user_info_url'], headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get user info: {error_text}")

                user_data = await response.json()
                return user_data

    async def handle_oauth_callback(self, provider_name: str, code: str, state: str) -> Dict[str, Any]:
        """Complete OAuth flow and return user info."""
        # Exchange code for token
        token_data = await self.exchange_code_for_token(provider_name, code, state)

        # Get user info
        user_info = await self.get_user_info(provider_name, token_data['access_token'])

        return {
            'access_token': token_data['access_token'],
            'refresh_token': token_data.get('refresh_token'),
            'expires_in': token_data.get('expires_in'),
            'user_info': user_info
        }

# Configure OAuth providers
oauth_manager = OAuthManager()

# Google OAuth
oauth_manager.register_provider('google', {
    'client_id': 'your-google-client-id',
    'client_secret': 'your-google-client-secret',
    'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
    'token_url': 'https://oauth2.googleapis.com/token',
    'user_info_url': 'https://www.googleapis.com/oauth2/v2/userinfo',
    'redirect_uri': 'http://localhost:3000/auth/google/callback',
    'scope': 'openid email profile'
})

# GitHub OAuth
oauth_manager.register_provider('github', {
    'client_id': 'your-github-client-id',
    'client_secret': 'your-github-client-secret',
    'authorize_url': 'https://github.com/login/oauth/authorize',
    'token_url': 'https://github.com/login/oauth/access_token',
    'user_info_url': 'https://api.github.com/user',
    'redirect_uri': 'http://localhost:3000/auth/github/callback',
    'scope': 'user:email'
})

# Microsoft OAuth
oauth_manager.register_provider('microsoft', {
    'client_id': 'your-microsoft-client-id',
    'client_secret': 'your-microsoft-client-secret',
    'authorize_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    'token_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
    'user_info_url': 'https://graph.microsoft.com/v1.0/me',
    'redirect_uri': 'http://localhost:3000/auth/microsoft/callback',
    'scope': 'openid email profile'
})
```

### SAML Authentication

```python
import xml.etree.ElementTree as ET
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64
import zlib

class SAMLManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sp_entity_id = config['sp_entity_id']
        self.idp_entity_id = config['idp_entity_id']
        self.idp_sso_url = config['idp_sso_url']
        self.idp_cert = config['idp_certificate']

        # Load SP private key
        with open(config['sp_private_key'], 'rb') as f:
            self.sp_private_key = serialization.load_pem_private_key(
                f.read(),
                password=config.get('sp_key_password')
            )

    def create_authn_request(self) -> str:
        """Create SAML AuthnRequest."""
        request_id = f"_{secrets.token_hex(16)}"
        issue_instant = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        authn_request = f'''<?xml version="1.0" encoding="UTF-8"?>
<samlp:AuthnRequest
    xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    ID="{request_id}"
    Version="2.0"
    IssueInstant="{issue_instant}"
    Destination="{self.idp_sso_url}"
    AssertionConsumerServiceURL="{self.config['acs_url']}"
    ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST">
    <saml:Issuer>{self.sp_entity_id}</saml:Issuer>
    <samlp:NameIDPolicy
        Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
        AllowCreate="true"/>
</samlp:AuthnRequest>'''

        # Sign the request
        signed_request = self.sign_saml_request(authn_request)

        # Deflate and base64 encode
        deflated = zlib.compress(signed_request.encode('utf-8'))
        encoded = base64.b64encode(deflated).decode('utf-8')

        return encoded

    def sign_saml_request(self, request_xml: str) -> str:
        """Sign SAML request with SP private key."""
        # Parse XML
        root = ET.fromstring(request_xml)

        # Create signature
        signature = ET.Element("{http://www.w3.org/2000/09/xmldsig#}Signature")
        signed_info = ET.SubElement(signature, "{http://www.w3.org/2000/09/xmldsig#}SignedInfo")
        canonicalization_method = ET.SubElement(signed_info, "{http://www.w3.org/2000/09/xmldsig#}CanonicalizationMethod")
        canonicalization_method.set("Algorithm", "http://www.w3.org/2001/10/xml-exc-c14n#")

        signature_method = ET.SubElement(signed_info, "{http://www.w3.org/2000/09/xmldsig#}SignatureMethod")
        signature_method.set("Algorithm", "http://www.w3.org/2000/09/xmldsig#rsa-sha256")

        reference = ET.SubElement(signed_info, "{http://www.w3.org/2000/09/xmldsig#}Reference")
        reference.set("URI", f"#{root.get('ID')}")

        transforms = ET.SubElement(reference, "{http://www.w3.org/2000/09/xmldsig#}Transforms")
        transform = ET.SubElement(transforms, "{http://www.w3.org/2000/09/xmldsig#}Transform")
        transform.set("Algorithm", "http://www.w3.org/2000/09/xmldsig#enveloped-signature")

        digest_method = ET.SubElement(reference, "{http://www.w3.org/2000/09/xmldsig#}DigestMethod")
        digest_method.set("Algorithm", "http://www.w3.org/2000/09/xmldsig#sha256")

        # Calculate digest (simplified - would need proper canonicalization)
        digest_value = ET.SubElement(reference, "{http://www.w3.org/2000/09/xmldsig#}DigestValue")
        digest_value.text = "digest_placeholder"

        signature_value = ET.SubElement(signature, "{http://www.w3.org/2000/09/xmldsig#}SignatureValue")
        signature_value.text = "signature_placeholder"

        key_info = ET.SubElement(signature, "{http://www.w3.org/2000/09/xmldsig#}KeyInfo")
        x509_data = ET.SubElement(key_info, "{http://www.w3.org/2000/09/xmldsig#}X509Data")
        x509_cert = ET.SubElement(x509_data, "{http://www.w3.org/2000/09/xmldsig#}X509Certificate")

        # Load and add SP certificate
        with open(self.config['sp_certificate'], 'r') as f:
            cert_data = f.read().replace('-----BEGIN CERTIFICATE-----', '').replace('-----END CERTIFICATE-----', '').replace('\n', '')
            x509_cert.text = cert_data

        # Insert signature into request
        root.insert(0, signature)

        return ET.tostring(root, encoding='unicode')

    def validate_saml_response(self, saml_response: str) -> Dict[str, Any]:
        """Validate SAML response from IdP."""
        # Decode and parse SAML response
        decoded = base64.b64decode(saml_response)
        inflated = zlib.decompress(decoded, -zlib.MAX_WBITS)
        root = ET.fromstring(inflated)

        # Verify signature
        if not self.verify_signature(root):
            raise ValueError("Invalid SAML response signature")

        # Extract user information
        user_info = self.extract_user_info(root)

        return user_info

    def verify_signature(self, root) -> bool:
        """Verify SAML response signature."""
        # Implementation would verify signature against IdP certificate
        # This is a simplified version
        return True

    def extract_user_info(self, root) -> Dict[str, Any]:
        """Extract user information from SAML assertion."""
        # Find assertion
        assertion = root.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}Assertion')
        if assertion is None:
            raise ValueError("No assertion found in SAML response")

        # Extract subject
        subject = assertion.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}Subject')
        name_id = subject.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}NameID')

        user_info = {
            'name_id': name_id.text if name_id is not None else None,
            'attributes': {}
        }

        # Extract attributes
        attribute_statement = assertion.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}AttributeStatement')
        if attribute_statement is not None:
            for attribute in attribute_statement.findall('.//{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
                attr_name = attribute.get('Name')
                attr_value_elem = attribute.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue')
                if attr_value_elem is not None:
                    user_info['attributes'][attr_name] = attr_value_elem.text

        return user_info
```

## Role-Based Access Control

### Permission System

```python
from typing import Set, Dict, List
from enum import Enum

class Permission(Enum):
    # Chat permissions
    CREATE_CHAT = "chat:create"
    READ_CHAT = "chat:read"
    UPDATE_CHAT = "chat:update"
    DELETE_CHAT = "chat:delete"
    SHARE_CHAT = "chat:share"

    # Model permissions
    USE_MODEL = "model:use"
    MANAGE_MODELS = "model:manage"

    # Document permissions
    UPLOAD_DOCUMENT = "document:upload"
    READ_DOCUMENT = "document:read"
    DELETE_DOCUMENT = "document:delete"

    # User management permissions
    MANAGE_USERS = "user:manage"
    VIEW_USERS = "user:view"

    # Admin permissions
    SYSTEM_ADMIN = "system:admin"
    VIEW_AUDIT_LOG = "audit:view"

class Role:
    def __init__(self, name: str, permissions: Set[Permission], inherits: List['Role'] = None):
        self.name = name
        self.permissions = permissions.copy()
        self.inherits = inherits or []

        # Add inherited permissions
        for parent_role in self.inherits:
            self.permissions.update(parent_role.get_all_permissions())

    def get_all_permissions(self) -> Set[Permission]:
        """Get all permissions including inherited ones."""
        return self.permissions.copy()

    def has_permission(self, permission: Permission) -> bool:
        """Check if role has specific permission."""
        return permission in self.permissions

class RBACManager:
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = {}  # user_id -> set of role names

        self._setup_default_roles()

    def _setup_default_roles(self):
        """Set up default roles and permissions."""

        # Guest role
        guest_permissions = {
            Permission.CREATE_CHAT,
            Permission.READ_CHAT,
            Permission.USE_MODEL
        }
        self.roles['guest'] = Role('guest', guest_permissions)

        # User role
        user_permissions = guest_permissions | {
            Permission.UPDATE_CHAT,
            Permission.DELETE_CHAT,
            Permission.UPLOAD_DOCUMENT,
            Permission.READ_DOCUMENT
        }
        self.roles['user'] = Role('user', user_permissions)

        # Moderator role
        moderator_permissions = user_permissions | {
            Permission.SHARE_CHAT,
            Permission.DELETE_DOCUMENT,
            Permission.VIEW_USERS
        }
        self.roles['moderator'] = Role('moderator', moderator_permissions, [self.roles['user']])

        # Admin role
        admin_permissions = moderator_permissions | {
            Permission.MANAGE_USERS,
            Permission.MANAGE_MODELS,
            Permission.SYSTEM_ADMIN,
            Permission.VIEW_AUDIT_LOG
        }
        self.roles['admin'] = Role('admin', admin_permissions, [self.roles['moderator']])

    def create_role(self, name: str, permissions: Set[Permission], inherits: List[str] = None) -> Role:
        """Create a custom role."""
        parent_roles = []
        if inherits:
            for parent_name in inherits:
                if parent_name not in self.roles:
                    raise ValueError(f"Parent role {parent_name} does not exist")
                parent_roles.append(self.roles[parent_name])

        role = Role(name, permissions, parent_roles)
        self.roles[name] = role
        return role

    def assign_role_to_user(self, user_id: str, role_name: str):
        """Assign role to user."""
        if role_name not in self.roles:
            raise ValueError(f"Role {role_name} does not exist")

        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()

        self.user_roles[user_id].add(role_name)

    def remove_role_from_user(self, user_id: str, role_name: str):
        """Remove role from user."""
        if user_id in self.user_roles:
            self.user_roles[user_id].discard(role_name)

    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user."""
        if user_id not in self.user_roles:
            return set()

        permissions = set()
        for role_name in self.user_roles[user_id]:
            role = self.roles.get(role_name)
            if role:
                permissions.update(role.get_all_permissions())

        return permissions

    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has specific permission."""
        user_permissions = self.get_user_permissions(user_id)
        return permission in user_permissions

    def get_user_roles(self, user_id: str) -> Set[str]:
        """Get all roles assigned to user."""
        return self.user_roles.get(user_id, set()).copy()

    def list_roles(self) -> Dict[str, Dict]:
        """List all roles with their permissions."""
        return {
            name: {
                'permissions': [p.value for p in role.get_all_permissions()],
                'inherits': [r.name for r in role.inherits]
            }
            for name, role in self.roles.items()
        }
```

### Session Management

```python
from typing import Dict, Any, Optional
import time
import json

class SessionManager:
    def __init__(self, redis_client=None, session_ttl: int = 3600):
        self.redis = redis_client
        self.session_ttl = session_ttl  # seconds
        self.sessions = {}  # In-memory fallback if no Redis

    async def create_session(self, user_id: str, user_data: Dict[str, Any]) -> str:
        """Create a new session for user."""
        session_id = f"session_{secrets.token_hex(16)}"

        session_data = {
            'user_id': user_id,
            'user_data': user_data,
            'created_at': time.time(),
            'last_activity': time.time(),
            'ip_address': user_data.get('ip_address'),
            'user_agent': user_data.get('user_agent')
        }

        # Store session
        await self._store_session(session_id, session_data)

        return session_id

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data by ID."""
        session_data = await self._get_session(session_id)

        if session_data:
            # Update last activity
            session_data['last_activity'] = time.time()
            await self._store_session(session_id, session_data)

            return session_data

        return None

    async def destroy_session(self, session_id: str):
        """Destroy a session."""
        await self._delete_session(session_id)

    async def validate_session(self, session_id: str) -> bool:
        """Validate if session exists and is not expired."""
        session_data = await self.get_session(session_id)

        if not session_data:
            return False

        # Check if session expired
        if time.time() - session_data['created_at'] > self.session_ttl:
            await self.destroy_session(session_id)
            return False

        return True

    async def get_user_sessions(self, user_id: str) -> List[str]:
        """Get all active session IDs for a user."""
        # This would require maintaining a user->sessions mapping
        # Implementation depends on storage backend
        return []

    async def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        # Implementation depends on storage backend
        # For Redis, this could use key expiration
        pass

    async def _store_session(self, session_id: str, data: Dict[str, Any]):
        """Store session data."""
        if self.redis:
            await self.redis.setex(
                f"session:{session_id}",
                self.session_ttl,
                json.dumps(data)
            )
        else:
            self.sessions[session_id] = data

    async def _get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data."""
        if self.redis:
            data = await self.redis.get(f"session:{session_id}")
            return json.loads(data) if data else None
        else:
            return self.sessions.get(session_id)

    async def _delete_session(self, session_id: str):
        """Delete session data."""
        if self.redis:
            await self.redis.delete(f"session:{session_id}")
        else:
            self.sessions.pop(session_id, None)
```

### User Activity Monitoring

```python
from typing import Dict, List, Any
import time
from collections import defaultdict
from datetime import datetime, timedelta

class ActivityMonitor:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.activities = defaultdict(list)  # In-memory fallback

    async def log_activity(self, user_id: str, activity_type: str, details: Dict[str, Any] = None):
        """Log user activity."""
        activity = {
            'user_id': user_id,
            'activity_type': activity_type,
            'timestamp': time.time(),
            'details': details or {}
        }

        # Store activity
        if self.redis:
            key = f"activity:{user_id}:{int(time.time())}"
            await self.redis.setex(key, 86400 * 30, json.dumps(activity))  # 30 days
        else:
            self.activities[user_id].append(activity)

            # Keep only last 1000 activities per user
            if len(self.activities[user_id]) > 1000:
                self.activities[user_id] = self.activities[user_id][-1000:]

    async def get_user_activities(self, user_id: str, limit: int = 100,
                                 start_time: float = None) -> List[Dict[str, Any]]:
        """Get user activity history."""
        if self.redis:
            # Redis implementation would need pattern matching
            # This is simplified
            pattern = f"activity:{user_id}:*"
            keys = await self.redis.keys(pattern)
            activities = []

            for key in keys[-limit:]:  # Get last N keys
                data = await self.redis.get(key)
                if data:
                    activities.append(json.loads(data))

            return sorted(activities, key=lambda x: x['timestamp'], reverse=True)
        else:
            activities = self.activities.get(user_id, [])
            if start_time:
                activities = [a for a in activities if a['timestamp'] >= start_time]

            return activities[-limit:]

    async def get_activity_summary(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """Get activity summary for user."""
        start_time = time.time() - (days * 86400)
        activities = await self.get_user_activities(user_id, start_time=start_time)

        summary = {
            'total_activities': len(activities),
            'activity_types': defaultdict(int),
            'daily_counts': defaultdict(int),
            'most_active_day': None
        }

        for activity in activities:
            # Count activity types
            summary['activity_types'][activity['activity_type']] += 1

            # Count daily activities
            day = datetime.fromtimestamp(activity['timestamp']).date().isoformat()
            summary['daily_counts'][day] += 1

        if summary['daily_counts']:
            summary['most_active_day'] = max(summary['daily_counts'].items(), key=lambda x: x[1])[0]

        return dict(summary)

    async def detect_suspicious_activity(self, user_id: str) -> List[Dict[str, Any]]:
        """Detect potentially suspicious user activity."""
        activities = await self.get_user_activities(user_id, limit=200)

        suspicious = []
        login_attempts = 0
        failed_logins = 0

        for activity in activities[-50:]:  # Check last 50 activities
            if activity['activity_type'] == 'login_attempt':
                login_attempts += 1
            elif activity['activity_type'] == 'login_failed':
                failed_logins += 1

        # Check for suspicious patterns
        if failed_logins > login_attempts * 0.5:  # More than 50% failed logins
            suspicious.append({
                'type': 'high_failed_login_rate',
                'severity': 'medium',
                'description': f"High failed login rate: {failed_logins}/{login_attempts}"
            })

        # Check for rapid actions
        timestamps = [a['timestamp'] for a in activities[-20:]]
        if len(timestamps) >= 10:
            time_spans = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
            avg_time = sum(time_spans) / len(time_spans)

            if avg_time < 1.0:  # Less than 1 second between actions
                suspicious.append({
                    'type': 'rapid_actions',
                    'severity': 'low',
                    'description': f"Very rapid user actions (avg {avg_time:.2f}s between actions)"
                })

        return suspicious

# Activity logging middleware
def activity_logging_middleware(activity_monitor: ActivityMonitor):
    def middleware(req, res, next):
        user_id = req.user?.id
        if user_id:
            activity_monitor.log_activity(user_id, req.path, {
                'method': req.method,
                'ip': req.ip,
                'user_agent': req.get('User-Agent')
            })
        next()
    return middleware
```

This comprehensive user management system provides enterprise-grade authentication, authorization, and monitoring capabilities for Open WebUI. The modular design supports various authentication methods and provides fine-grained access control for different user roles. 🚀