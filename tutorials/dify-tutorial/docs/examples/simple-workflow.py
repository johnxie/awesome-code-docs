"""
Example: Creating a Simple Dify Workflow

This example demonstrates how to create a basic workflow that:
1. Takes user input
2. Processes it through an LLM
3. Returns the response

Part of the Dify Platform Deep Dive Tutorial
"""

import requests
import json
from typing import Dict, Any

class DifyWorkflowExample:
    def __init__(self, api_key: str, base_url: str = "http://localhost:5001"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_simple_app(self) -> Dict[str, Any]:
        """
        Create a simple chatbot application via API
        
        Returns:
            Dict containing app information
        """
        app_data = {
            "name": "Simple Tutorial Bot",
            "description": "A basic chatbot for learning Dify workflows",
            "mode": "chat",  # chat, completion, or workflow
            "icon": "🤖",
            "icon_background": "#3B82F6"
        }
        
        response = requests.post(
            f"{self.base_url}/v1/apps",
            headers=self.headers,
            json=app_data
        )
        
        if response.status_code == 201:
            print("✅ App created successfully!")
            return response.json()
        else:
            print(f"❌ Error creating app: {response.text}")
            return {}
    
    def configure_model(self, app_id: str) -> bool:
        """
        Configure the LLM model for the application
        
        Args:
            app_id: The application ID
            
        Returns:
            Boolean indicating success
        """
        model_config = {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        }
        
        response = requests.put(
            f"{self.base_url}/v1/apps/{app_id}/model-config",
            headers=self.headers,
            json=model_config
        )
        
        return response.status_code == 200
    
    def send_message(self, app_id: str, message: str, user_id: str = "tutorial-user") -> Dict[str, Any]:
        """
        Send a message to the chatbot and get response
        
        Args:
            app_id: The application ID
            message: User message
            user_id: Unique user identifier
            
        Returns:
            Bot response data
        """
        message_data = {
            "query": message,
            "user": user_id,
            "conversation_id": "",  # Empty for new conversation
            "inputs": {}
        }
        
        response = requests.post(
            f"{self.base_url}/v1/apps/{app_id}/chat-messages",
            headers=self.headers,
            json=message_data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error sending message: {response.text}")
            return {}

def main():
    """
    Main function to demonstrate the workflow
    """
    # Initialize the Dify client
    # Get your API key from the Dify admin interface
    api_key = "your-api-key-here"
    dify = DifyWorkflowExample(api_key)
    
    try:
        # Step 1: Create the application
        print("🚀 Creating Dify application...")
        app_data = dify.create_simple_app()
        
        if not app_data:
            print("Failed to create app. Exiting.")
            return
            
        app_id = app_data["id"]
        print(f"📱 App created with ID: {app_id}")
        
        # Step 2: Configure the model
        print("⚙️ Configuring LLM model...")
        if dify.configure_model(app_id):
            print("✅ Model configured successfully!")
        else:
            print("❌ Failed to configure model")
            return
        
        # Step 3: Test the workflow
        print("\n💬 Testing the chatbot...")
        
        test_messages = [
            "Hello! What can you help me with?",
            "Explain what Dify is in simple terms",
            "What are the main components of Dify's architecture?"
        ]
        
        for message in test_messages:
            print(f"\n👤 User: {message}")
            
            response = dify.send_message(app_id, message)
            
            if response and "answer" in response:
                print(f"🤖 Bot: {response['answer']}")
            else:
                print("❌ No response received")
        
        print("\n🎉 Tutorial workflow completed successfully!")
        print(f"📊 App dashboard: http://localhost:3000/apps/{app_id}")
        
    except Exception as e:
        print(f"💥 An error occurred: {str(e)}")

if __name__ == "__main__":
    main()


# Additional utility functions for advanced workflows

def create_workflow_with_nodes():
    """
    Example of creating a more complex workflow with multiple nodes
    
    This demonstrates:
    - Input validation node
    - LLM processing node  
    - Output formatting node
    - Conditional branching
    """
    workflow_definition = {
        "nodes": [
            {
                "id": "input_validator",
                "type": "code",
                "code": """
                def validate_input(user_input):
                    if len(user_input.strip()) < 3:
                        return {"valid": False, "message": "Input too short"}
                    return {"valid": True, "message": user_input}
                """,
                "inputs": ["user_input"],
                "outputs": ["validation_result"]
            },
            {
                "id": "llm_processor", 
                "type": "llm",
                "model": "gpt-3.5-turbo",
                "prompt": "Process this user input: {{validation_result.message}}",
                "inputs": ["validation_result"],
                "outputs": ["llm_response"]
            },
            {
                "id": "formatter",
                "type": "code", 
                "code": """
                def format_response(response):
                    return {
                        "formatted_response": f"🤖 {response}",
                        "timestamp": datetime.now().isoformat()
                    }
                """,
                "inputs": ["llm_response"],
                "outputs": ["final_output"]
            }
        ],
        "connections": [
            {"from": "input_validator", "to": "llm_processor"},
            {"from": "llm_processor", "to": "formatter"}
        ]
    }
    
    return workflow_definition

# Configuration examples for different use cases

WORKFLOW_TEMPLATES = {
    "simple_chat": {
        "description": "Basic chatbot workflow",
        "nodes": ["input", "llm", "output"],
        "use_case": "General conversation"
    },
    
    "rag_assistant": {
        "description": "RAG-powered knowledge assistant",
        "nodes": ["input", "retrieval", "llm", "citation", "output"],
        "use_case": "Document-based Q&A"
    },
    
    "multi_step_agent": {
        "description": "Agent with tool calling capabilities",
        "nodes": ["input", "planner", "tool_executor", "synthesizer", "output"],
        "use_case": "Complex task automation"
    }
}
