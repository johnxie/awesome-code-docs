---
layout: default
title: "Chapter 6: Building Memory-Enabled Applications"
parent: "Mem0 Tutorial"
nav_order: 6
---

# Chapter 6: Building Memory-Enabled Applications

> Implement real-world applications powered by intelligent memory systems.

## 🎯 Overview

This chapter demonstrates practical applications of Mem0 across different domains, showing how to build memory-enabled AI systems for customer support, content creation, learning platforms, and more. You'll learn to integrate memory capabilities into complete applications.

## 💬 Customer Support Chatbot

### Memory-Enhanced Support Agent

```python
from mem0 import Memory
from typing import Dict, List, Any, Optional
import time

class MemoryEnhancedSupportAgent:
    """Customer support chatbot with memory of user interactions"""

    def __init__(self, llm_provider="openai"):
        self.memory = Memory()
        self.llm_provider = llm_provider

        # Initialize LLM client
        if llm_provider == "openai":
            from openai import OpenAI
            self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Support knowledge base
        self.support_kb = self._initialize_support_kb()

    def _initialize_support_kb(self) -> Dict[str, Any]:
        """Initialize support knowledge base"""

        kb = {
            "common_issues": {
                "password_reset": "To reset your password, go to settings > security > reset password",
                "billing_issue": "For billing questions, visit billing.example.com or contact support@billing.com",
                "account_locked": "Accounts are locked after 5 failed attempts. Contact support to unlock.",
                "feature_request": "Feature requests can be submitted at features.example.com"
            },
            "product_info": {
                "pricing": "We offer Basic ($9/mo), Pro ($29/mo), and Enterprise ($99/mo) plans",
                "free_trial": "Free trial lasts 14 days and includes all Pro features",
                "refund_policy": "Refunds available within 30 days of purchase for unused services"
            },
            "troubleshooting": {
                "slow_loading": "Try clearing cache, using incognito mode, or checking internet connection",
                "error_500": "This is a server error. Please try again in 5 minutes or contact support",
                "login_issue": "Ensure caps lock is off and try resetting password if needed"
            }
        }

        # Store KB in memory for easy retrieval
        for category, items in kb.items():
            for topic, info in items.items():
                self.memory.add(
                    f"Support KB - {category}: {topic} - {info}",
                    user_id="system",
                    metadata={
                        "category": "support_kb",
                        "subcategory": category,
                        "topic": topic,
                        "source": "knowledge_base"
                    }
                )

        return kb

    def handle_customer_query(self, user_id: str, query: str) -> Dict[str, Any]:
        """Handle customer support query with memory context"""

        # Retrieve user history
        user_history = self.memory.search("", user_id=user_id, limit=10)

        # Analyze query
        query_analysis = self._analyze_support_query(query)

        # Get relevant knowledge base info
        kb_info = self._get_relevant_kb_info(query_analysis)

        # Build context from user history
        context = self._build_user_context(user_history, query_analysis)

        # Generate personalized response
        response = self._generate_support_response(query, context, kb_info, user_history)

        # Store interaction
        self._store_support_interaction(user_id, query, response, query_analysis)

        # Check if escalation needed
        needs_escalation = self._check_escalation_needed(query_analysis, len(user_history))

        return {
            "response": response,
            "confidence": query_analysis.get("confidence", 0.5),
            "category": query_analysis.get("category", "general"),
            "needs_escalation": needs_escalation,
            "suggested_actions": self._get_suggested_actions(query_analysis)
        }

    def _analyze_support_query(self, query: str) -> Dict[str, Any]:
        """Analyze support query to categorize and prioritize"""

        analysis = {
            "category": "general",
            "urgency": "low",
            "confidence": 0.5,
            "keywords": [],
            "sentiment": "neutral"
        }

        query_lower = query.lower()

        # Categorize query
        if any(word in query_lower for word in ["password", "login", "account", "access"]):
            analysis["category"] = "account_access"
        elif any(word in query_lower for word in ["billing", "payment", "charge", "refund", "price"]):
            analysis["category"] = "billing"
        elif any(word in query_lower for word in ["slow", "error", "bug", "broken", "not working"]):
            analysis["category"] = "technical_issue"
        elif any(word in query_lower for word in ["feature", "request", "suggest", "improve"]):
            analysis["category"] = "feature_request"

        # Determine urgency
        urgent_keywords = ["urgent", "emergency", "asap", "immediately", "critical"]
        if any(word in query_lower for word in urgent_keywords):
            analysis["urgency"] = "high"
        elif analysis["category"] == "technical_issue":
            analysis["urgency"] = "medium"

        # Extract keywords
        common_keywords = ["help", "problem", "issue", "question", "support", "please"]
        analysis["keywords"] = [word for word in query.split() if word.lower() in common_keywords]

        # Simple sentiment analysis
        positive_words = ["thank", "good", "great", "helpful", "appreciate"]
        negative_words = ["frustrated", "angry", "disappointed", "terrible", "hate"]

        if any(word in query_lower for word in positive_words):
            analysis["sentiment"] = "positive"
        elif any(word in query_lower for word in negative_words):
            analysis["sentiment"] = "negative"

        # Calculate confidence based on clarity
        analysis["confidence"] = min(1.0, len(query.split()) / 20)  # More words = more confidence

        return analysis

    def _get_relevant_kb_info(self, query_analysis: Dict[str, Any]) -> str:
        """Get relevant knowledge base information"""

        category = query_analysis.get("category", "general")

        # Search for relevant KB entries
        kb_search = self.memory.search(
            f"support_kb {category}",
            user_id="system",
            limit=3
        )

        if kb_search:
            kb_info = "\n".join([entry["content"] for entry in kb_search])
            return f"Relevant information:\n{kb_info}"

        return "No specific knowledge base information available."

    def _build_user_context(self, user_history: List[Dict[str, Any]], query_analysis: Dict[str, Any]) -> str:
        """Build context from user's interaction history"""

        if not user_history:
            return "First-time user interaction."

        # Get recent relevant interactions
        relevant_history = []
        for interaction in user_history[-5:]:  # Last 5 interactions
            content = interaction.get("content", "")
            if query_analysis["category"] in content.lower():
                relevant_history.append(content)

        if relevant_history:
            context = "Previous related interactions:\n" + "\n".join(relevant_history[-3:])
            return context

        return f"User has had {len(user_history)} previous interactions."

    def _generate_support_response(self, query: str, context: str, kb_info: str,
                                 user_history: List[Dict[str, Any]]) -> str:
        """Generate personalized support response"""

        system_prompt = f"""You are a helpful customer support agent with access to user interaction history.

CONTEXT:
{context}

KNOWLEDGE BASE:
{kb_info}

USER HISTORY: {len(user_history)} previous interactions

Respond professionally, empathetically, and provide specific solutions when possible.
Reference previous interactions if relevant.
If you cannot solve the issue, suggest next steps clearly."""

        if self.llm_provider == "openai":
            response = self.llm.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.3,  # Lower temperature for support responses
                max_tokens=500
            )
            return response.choices[0].message.content

        return "Support response generation failed."

    def _store_support_interaction(self, user_id: str, query: str, response: str,
                                 query_analysis: Dict[str, Any]):
        """Store support interaction in memory"""

        # Store user query
        self.memory.add(
            f"Support query: {query}",
            user_id=user_id,
            metadata={
                "interaction_type": "support_query",
                "category": query_analysis.get("category"),
                "urgency": query_analysis.get("urgency"),
                "sentiment": query_analysis.get("sentiment"),
                "resolved": False  # Will be updated when resolved
            }
        )

        # Store agent response
        self.memory.add(
            f"Support response: {response}",
            user_id=user_id,
            metadata={
                "interaction_type": "support_response",
                "category": query_analysis.get("category"),
                "confidence": query_analysis.get("confidence"),
                "response_length": len(response)
            }
        )

    def _check_escalation_needed(self, query_analysis: Dict[str, Any], history_length: int) -> bool:
        """Check if query needs escalation to human agent"""

        # Escalate if high urgency
        if query_analysis.get("urgency") == "high":
            return True

        # Escalate if repeated similar issues
        if history_length > 10:  # Many interactions suggest unresolved issues
            return True

        # Escalate if low confidence in automated response
        if query_analysis.get("confidence", 0.5) < 0.3:
            return True

        # Escalate complex technical issues
        if query_analysis.get("category") == "technical_issue" and history_length > 3:
            return True

        return False

    def _get_suggested_actions(self, query_analysis: Dict[str, Any]) -> List[str]:
        """Get suggested next actions for user"""

        actions = []

        category = query_analysis.get("category")

        if category == "account_access":
            actions.extend([
                "Try resetting password at settings > security",
                "Check if caps lock is enabled",
                "Contact support if account appears locked"
            ])
        elif category == "billing":
            actions.extend([
                "Visit billing dashboard at billing.example.com",
                "Check payment method on file",
                "Review invoice for charge details"
            ])
        elif category == "technical_issue":
            actions.extend([
                "Try clearing browser cache",
                "Restart the application",
                "Check internet connection"
            ])

        return actions[:3]  # Return top 3 actions

    def get_support_metrics(self, user_id: str = None) -> Dict[str, Any]:
        """Get support interaction metrics"""

        # Get all support interactions
        if user_id:
            interactions = self.memory.search("support", user_id=user_id, limit=100)
        else:
            interactions = self.memory.search("support", limit=1000)

        metrics = {
            "total_interactions": len(interactions),
            "categories": {},
            "resolution_rate": 0,
            "avg_response_time": 0,
            "escalation_rate": 0
        }

        resolved_count = 0
        escalated_count = 0

        for interaction in interactions:
            metadata = interaction.get("metadata", {})

            # Count categories
            category = metadata.get("category", "unknown")
            metrics["categories"][category] = metrics["categories"].get(category, 0) + 1

            # Count resolutions
            if metadata.get("resolved", False):
                resolved_count += 1

            # Count escalations (this would need to be tracked)
            if metadata.get("escalated", False):
                escalated_count += 1

        # Calculate rates
        if metrics["total_interactions"] > 0:
            metrics["resolution_rate"] = resolved_count / metrics["total_interactions"]
            metrics["escalation_rate"] = escalated_count / metrics["total_interactions"]

        return metrics

# Usage
support_agent = MemoryEnhancedSupportAgent()

# Handle customer queries
queries = [
    "I forgot my password and can't log in",
    "I'm being charged twice for my subscription",
    "The app keeps crashing when I try to save",
    "How do I upgrade to the Pro plan?"
]

for i, query in enumerate(queries):
    user_id = f"user_{i+1}"
    result = support_agent.handle_customer_query(user_id, query)

    print(f"\nQuery: {query}")
    print(f"Category: {result['category']}")
    print(f"Response: {result['response'][:100]}...")
    print(f"Needs escalation: {result['needs_escalation']}")
    if result['suggested_actions']:
        print(f"Suggested actions: {result['suggested_actions'][:2]}")

# Get support metrics
metrics = support_agent.get_support_metrics()
print(f"\nSupport Metrics: {metrics}")
```

## 📚 Personalized Learning Assistant

### Adaptive Learning System

```python
from mem0 import Memory
from typing import Dict, List, Any, Optional
import json

class PersonalizedLearningAssistant:
    """AI learning assistant that adapts to student needs and progress"""

    def __init__(self):
        self.memory = Memory()
        self.learning_paths = self._initialize_learning_paths()

    def _initialize_learning_paths(self) -> Dict[str, Any]:
        """Initialize structured learning paths"""

        return {
            "python_basics": {
                "title": "Python Programming Basics",
                "topics": ["variables", "loops", "functions", "classes", "file_io"],
                "prerequisites": [],
                "difficulty": "beginner"
            },
            "machine_learning": {
                "title": "Machine Learning Fundamentals",
                "topics": ["linear_regression", "classification", "neural_networks", "evaluation"],
                "prerequisites": ["python_basics", "statistics"],
                "difficulty": "intermediate"
            },
            "web_development": {
                "title": "Web Development",
                "topics": ["html", "css", "javascript", "react", "node_js"],
                "prerequisites": ["python_basics"],
                "difficulty": "beginner"
            }
        }

    def assess_student_level(self, student_id: str, subject: str) -> Dict[str, Any]:
        """Assess student's current knowledge level"""

        # Get student's learning history
        learning_history = self.memory.search(
            f"learning {subject}",
            user_id=student_id,
            limit=20
        )

        assessment = {
            "subject": subject,
            "overall_level": "beginner",
            "known_topics": [],
            "struggling_topics": [],
            "recommended_next": [],
            "confidence_score": 0.0
        }

        if not learning_history:
            # New student
            assessment["recommended_next"] = self.learning_paths.get(subject, {}).get("topics", [])[:2]
            return assessment

        # Analyze learning history
        topic_performance = {}
        for interaction in learning_history:
            content = interaction.get("content", "").lower()
            metadata = interaction.get("metadata", {})

            # Extract topic information
            for topic in self.learning_paths.get(subject, {}).get("topics", []):
                if topic.replace("_", " ") in content:
                    if topic not in topic_performance:
                        topic_performance[topic] = {"correct": 0, "attempts": 0}

                    # Check if it was a successful learning interaction
                    if "correct" in content or "good" in content or metadata.get("success", False):
                        topic_performance[topic]["correct"] += 1
                    topic_performance[topic]["attempts"] += 1

        # Calculate topic mastery
        for topic, performance in topic_performance.items():
            accuracy = performance["correct"] / performance["attempts"] if performance["attempts"] > 0 else 0

            if accuracy > 0.8:
                assessment["known_topics"].append(topic)
            elif accuracy < 0.5:
                assessment["struggling_topics"].append(topic)

        # Determine overall level
        known_count = len(assessment["known_topics"])
        total_topics = len(self.learning_paths.get(subject, {}).get("topics", []))

        if known_count / total_topics > 0.7:
            assessment["overall_level"] = "advanced"
        elif known_count / total_topics > 0.4:
            assessment["overall_level"] = "intermediate"

        # Recommend next topics
        all_topics = set(self.learning_paths.get(subject, {}).get("topics", []))
        completed_topics = set(assessment["known_topics"])
        remaining_topics = list(all_topics - completed_topics)

        # Prioritize struggling topics for review
        assessment["recommended_next"] = assessment["struggling_topics"][:2] + remaining_topics[:2]

        # Calculate confidence
        assessment["confidence_score"] = min(1.0, len(learning_history) / 10)

        return assessment

    def provide_personalized_lesson(self, student_id: str, topic: str) -> Dict[str, Any]:
        """Provide personalized lesson based on student history"""

        # Get student assessment
        assessment = self.assess_student_level(student_id, "programming")  # Assuming programming context

        # Get topic-specific history
        topic_history = self.memory.search(
            f"learning {topic}",
            user_id=student_id,
            limit=10
        )

        # Adapt lesson based on assessment
        lesson = self._create_adaptive_lesson(topic, assessment, topic_history)

        # Store lesson interaction
        self.memory.add(
            f"Learning lesson: {topic} - {lesson['title']}",
            user_id=student_id,
            metadata={
                "interaction_type": "lesson",
                "topic": topic,
                "difficulty_level": lesson.get("difficulty", "intermediate"),
                "lesson_type": lesson.get("type", "explanation")
            }
        )

        return lesson

    def _create_adaptive_lesson(self, topic: str, assessment: Dict[str, Any],
                               topic_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create lesson adapted to student's level"""

        base_lessons = {
            "variables": {
                "beginner": {
                    "title": "Understanding Variables",
                    "content": "Variables are containers for storing data values. In Python, you create a variable by assigning a value: x = 5",
                    "examples": ["x = 5", "name = 'Alice'", "is_active = True"],
                    "exercises": ["Create a variable called age and assign it your age"]
                },
                "intermediate": {
                    "title": "Advanced Variable Types",
                    "content": "Python supports various data types including lists, dictionaries, and custom objects.",
                    "examples": ["my_list = [1, 2, 3]", "my_dict = {'key': 'value'}"],
                    "exercises": ["Create a dictionary with personal information"]
                }
            }
        }

        student_level = assessment.get("overall_level", "beginner")

        if topic in base_lessons and student_level in base_lessons[topic]:
            lesson = base_lessons[topic][student_level].copy()
            lesson["difficulty"] = student_level
            lesson["type"] = "explanation"
        else:
            # Generic lesson
            lesson = {
                "title": f"Introduction to {topic.replace('_', ' ').title()}",
                "content": f"This is an introduction to {topic}. We'll cover the basics and build from there.",
                "examples": [f"Example of {topic}"],
                "exercises": [f"Practice exercise for {topic}"],
                "difficulty": student_level,
                "type": "introduction"
            }

        # Add personalized elements
        if assessment.get("struggling_topics"):
            lesson["review_section"] = f"Let's review: {', '.join(assessment['struggling_topics'][:2])}"

        lesson["progress_indicator"] = f"Level: {student_level.title()}"

        return lesson

    def track_learning_progress(self, student_id: str, topic: str, performance: float):
        """Track student progress and update learning path"""

        # Store performance data
        self.memory.add(
            f"Learning progress: {topic} - Performance: {performance:.2f}",
            user_id=student_id,
            metadata={
                "interaction_type": "progress",
                "topic": topic,
                "performance_score": performance,
                "timestamp": time.time(),
                "success": performance > 0.7
            }
        )

        # Update learning path recommendations
        current_assessment = self.assess_student_level(student_id, "programming")

        # Provide feedback and next steps
        feedback = self._generate_progress_feedback(performance, topic, current_assessment)

        return {
            "performance": performance,
            "feedback": feedback,
            "next_recommendations": current_assessment.get("recommended_next", []),
            "current_level": current_assessment.get("overall_level")
        }

    def _generate_progress_feedback(self, performance: float, topic: str,
                                  assessment: Dict[str, Any]) -> str:
        """Generate personalized progress feedback"""

        if performance > 0.9:
            feedback = f"Excellent work on {topic}! You're mastering this concept."
        elif performance > 0.7:
            feedback = f"Good progress on {topic}. Keep practicing to solidify your understanding."
        elif performance > 0.5:
            feedback = f"You're making progress on {topic}. Let's review the fundamentals."
        else:
            feedback = f"{topic} is challenging. Let's break it down and go through it step by step."

        # Add personalized suggestions
        struggling = assessment.get("struggling_topics", [])
        if topic in struggling:
            feedback += f" You might want to review {topic} more carefully."

        known = assessment.get("known_topics", [])
        if known:
            feedback += f" Since you know {known[0]}, try applying it to {topic}."

        return feedback

    def get_learning_analytics(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive learning analytics"""

        # Get all learning interactions
        learning_data = self.memory.search("learning", user_id=student_id, limit=100)

        analytics = {
            "total_interactions": len(learning_data),
            "topics_covered": set(),
            "average_performance": 0.0,
            "learning_streak": 0,
            "time_spent_learning": 0,
            "strengths": [],
            "areas_for_improvement": []
        }

        performances = []
        topics = set()

        for interaction in learning_data:
            metadata = interaction.get("metadata", {})

            # Collect topics
            if "topic" in metadata:
                topics.add(metadata["topic"])

            # Collect performance scores
            if "performance_score" in metadata:
                performances.append(metadata["performance_score"])

            # Calculate learning time (estimate)
            if "timestamp" in metadata:
                analytics["time_spent_learning"] += 1  # 1 minute per interaction

        analytics["topics_covered"] = list(topics)

        if performances:
            analytics["average_performance"] = sum(performances) / len(performances)

            # Identify strengths (high performance topics)
            topic_performance = {}
            for interaction in learning_data:
                metadata = interaction.get("metadata", {})
                topic = metadata.get("topic")
                performance = metadata.get("performance_score")

                if topic and performance is not None:
                    if topic not in topic_performance:
                        topic_performance[topic] = []
                    topic_performance[topic].append(performance)

            for topic, scores in topic_performance.items():
                avg_score = sum(scores) / len(scores)
                if avg_score > 0.8:
                    analytics["strengths"].append(topic)
                elif avg_score < 0.6:
                    analytics["areas_for_improvement"].append(topic)

        return analytics

# Usage
learning_assistant = PersonalizedLearningAssistant()

# Assess student level
assessment = learning_assistant.assess_student_level("student_123", "programming")
print(f"Student Assessment: {assessment}")

# Provide personalized lesson
lesson = learning_assistant.provide_personalized_lesson("student_123", "variables")
print(f"Personalized Lesson: {lesson['title']}")
print(f"Content: {lesson['content'][:100]}...")

# Track progress
progress = learning_assistant.track_learning_progress("student_123", "variables", 0.85)
print(f"Progress Feedback: {progress['feedback']}")

# Get learning analytics
analytics = learning_assistant.get_learning_analytics("student_123")
print(f"Learning Analytics: {analytics}")
```

## 🎨 Content Creation Assistant

### Memory-Driven Content Generation

```python
from mem0 import Memory
from typing import Dict, List, Any, Optional
import re

class ContentCreationAssistant:
    """AI assistant for content creation with memory of user preferences and style"""

    def __init__(self):
        self.memory = Memory()
        self.content_templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict[str, Any]:
        """Initialize content creation templates"""

        return {
            "blog_post": {
                "structure": ["title", "introduction", "main_content", "conclusion"],
                "tone_options": ["professional", "casual", "educational", "promotional"],
                "typical_length": "800-1200 words"
            },
            "social_media": {
                "platforms": ["twitter", "linkedin", "instagram", "facebook"],
                "max_lengths": {"twitter": 280, "linkedin": 3000, "instagram": 2200, "facebook": 63206},
                "tone_options": ["engaging", "professional", "fun", "informative"]
            },
            "email": {
                "types": ["newsletter", "promotional", "announcement", "personal"],
                "tone_options": ["formal", "friendly", "urgent", "persuasive"]
            }
        }

    def analyze_user_style(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's content creation style and preferences"""

        # Get user's content creation history
        content_history = self.memory.search(
            "content creation",
            user_id=user_id,
            limit=20
        )

        style_analysis = {
            "preferred_tones": [],
            "common_topics": [],
            "typical_length": "medium",
            "style_characteristics": [],
            "preferred_formats": []
        }

        tone_counts = {}
        topic_counts = {}
        length_indicators = []

        for item in content_history:
            content = item.get("content", "").lower()
            metadata = item.get("metadata", {})

            # Analyze tone preferences
            tones = ["professional", "casual", "formal", "friendly", "engaging"]
            for tone in tones:
                if tone in content:
                    tone_counts[tone] = tone_counts.get(tone, 0) + 1

            # Extract topics
            topics = self._extract_topics(content)
            for topic in topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1

            # Analyze length preferences
            content_length = len(content.split())
            length_indicators.append(content_length)

            # Analyze format preferences
            content_type = metadata.get("content_type")
            if content_type:
                style_analysis["preferred_formats"].append(content_type)

        # Determine preferences
        if tone_counts:
            style_analysis["preferred_tones"] = sorted(
                tone_counts.items(), key=lambda x: x[1], reverse=True
            )[:2]

        if topic_counts:
            style_analysis["common_topics"] = list(topic_counts.keys())[:5]

        if length_indicators:
            avg_length = sum(length_indicators) / len(length_indicators)
            if avg_length < 300:
                style_analysis["typical_length"] = "short"
            elif avg_length > 1000:
                style_analysis["typical_length"] = "long"
            else:
                style_analysis["typical_length"] = "medium"

        return style_analysis

    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from content"""

        # Simple topic extraction based on keywords
        topic_keywords = {
            "technology": ["ai", "machine learning", "software", "programming", "tech"],
            "business": ["marketing", "sales", "strategy", "growth", "startup"],
            "health": ["fitness", "nutrition", "wellness", "medical", "health"],
            "education": ["learning", "teaching", "course", "tutorial", "knowledge"],
            "lifestyle": ["travel", "food", "fashion", "home", "lifestyle"]
        }

        found_topics = []
        content_lower = content.lower()

        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                found_topics.append(topic)

        return found_topics

    def generate_content_idea(self, user_id: str, topic: str, content_type: str = "blog_post") -> Dict[str, Any]:
        """Generate content idea based on user preferences and history"""

        # Analyze user style
        user_style = self.analyze_user_style(user_id)

        # Get content type template
        template = self.content_templates.get(content_type, self.content_templates["blog_post"])

        # Generate personalized idea
        idea = {
            "topic": topic,
            "content_type": content_type,
            "suggested_title": self._generate_title(topic, user_style),
            "target_audience": self._infer_audience(user_style),
            "recommended_tone": user_style.get("preferred_tones", [["professional", 1]])[0][0],
            "estimated_length": template.get("typical_length", "medium"),
            "key_points": self._generate_key_points(topic, user_style),
            "unique_angle": self._find_unique_angle(topic, user_id)
        }

        # Store content idea in memory
        self.memory.add(
            f"Content idea generated: {idea['suggested_title']}",
            user_id=user_id,
            metadata={
                "interaction_type": "content_idea",
                "topic": topic,
                "content_type": content_type,
                "title": idea["suggested_title"]
            }
        )

        return idea

    def _generate_title(self, topic: str, user_style: Dict[str, Any]) -> str:
        """Generate compelling title based on user style"""

        # Simple title generation based on style
        tone = user_style.get("preferred_tones", [["professional", 1]])[0][0]

        title_templates = {
            "professional": [
                f"The Complete Guide to {topic.title()}",
                f"Understanding {topic.title()}: A Professional Perspective",
                f"{topic.title()}: Best Practices and Implementation"
            ],
            "casual": [
                f"Everything You Need to Know About {topic}",
                f"Why {topic.title()} Matters (And How to Get Started)",
                f"The Fun Side of {topic.title()}"
            ],
            "educational": [
                f"Learn {topic.title()}: From Beginner to Expert",
                f"{topic.title()} Explained: Concepts and Applications",
                f"Mastering {topic.title()}: A Step-by-Step Guide"
            ]
        }

        templates = title_templates.get(tone, title_templates["professional"])
        return templates[hash(topic) % len(templates)]  # Deterministic selection

    def _infer_audience(self, user_style: Dict[str, Any]) -> str:
        """Infer target audience from user style"""

        common_topics = user_style.get("common_topics", [])

        if "technology" in common_topics or "programming" in common_topics:
            return "developers and tech professionals"
        elif "business" in common_topics:
            return "business professionals and entrepreneurs"
        elif "education" in common_topics:
            return "students and educators"
        else:
            return "general audience"

    def _generate_key_points(self, topic: str, user_style: Dict[str, Any]) -> List[str]:
        """Generate key points for content based on user history"""

        # Get user's previous content on similar topics
        similar_content = self.memory.search(f"content {topic}", limit=5)

        key_points = []

        if similar_content:
            # Extract successful elements from previous content
            for item in similar_content:
                content = item.get("content", "")
                # Simple extraction of key sentences
                sentences = content.split(".")
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 20 and len(sentence) < 100:
                        key_points.append(sentence[:80] + "...")
                        if len(key_points) >= 3:
                            break
                if len(key_points) >= 3:
                    break
        else:
            # Default key points based on topic
            key_points = [
                f"Introduction to {topic} fundamentals",
                f"Practical applications and use cases",
                f"Best practices and common pitfalls",
                f"Future trends and developments"
            ]

        return key_points[:5]

    def _find_unique_angle(self, topic: str, user_id: str) -> str:
        """Find unique angle based on user's perspective"""

        # Get user's expertise areas
        user_content = self.memory.search("content", user_id=user_id, limit=10)

        expertise_areas = set()
        for item in user_content:
            content = item.get("content", "").lower()
            if "expert" in content or "experienced" in content:
                # Extract mentioned expertise
                words = content.split()
                for i, word in enumerate(words):
                    if word in ["expert", "experienced", "specialist"]:
                        # Look for topic before this word
                        if i > 0:
                            expertise_areas.add(words[i-1])

        if expertise_areas:
            expertise = list(expertise_areas)[0]
            return f"Unique perspective from {expertise} experience"
        else:
            return f"Fresh insights and practical applications"

    def track_content_performance(self, user_id: str, content_title: str,
                                metrics: Dict[str, Any]):
        """Track content performance and learn from results"""

        # Store performance data
        self.memory.add(
            f"Content performance: {content_title} - Views: {metrics.get('views', 0)}, Engagement: {metrics.get('engagement', 0)}",
            user_id=user_id,
            metadata={
                "interaction_type": "content_performance",
                "content_title": content_title,
                "views": metrics.get("views", 0),
                "engagement": metrics.get("engagement", 0),
                "shares": metrics.get("shares", 0),
                "timestamp": time.time()
            }
        )

        # Learn from performance
        self._learn_from_performance(user_id, metrics)

    def _learn_from_performance(self, user_id: str, metrics: Dict[str, Any]):
        """Learn from content performance for future recommendations"""

        engagement_score = metrics.get("engagement", 0)
        views = metrics.get("views", 0)

        # Store learning insights
        if engagement_score > 0.7:
            insight = "High engagement content characteristics learned"
        elif engagement_score < 0.3:
            insight = "Low engagement patterns identified"
        else:
            insight = "Moderate performance patterns recorded"

        self.memory.add(
            f"Content learning: {insight} - Engagement: {engagement_score:.2f}",
            user_id=user_id,
            metadata={
                "interaction_type": "learning_insight",
                "engagement_score": engagement_score,
                "views": views,
                "learning_type": "content_performance"
            }
        )

    def get_content_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized content creation recommendations"""

        # Analyze user history
        user_style = self.analyze_user_style(user_id)

        # Get performance insights
        performance_data = self.memory.search("content performance", user_id=user_id, limit=10)

        recommendations = {
            "suggested_topics": self._suggest_topics(user_style),
            "optimal_content_types": self._suggest_content_types(user_style),
            "best_performing_themes": self._analyze_successful_themes(performance_data),
            "improvement_areas": self._identify_improvement_areas(performance_data)
        }

        return recommendations

    def _suggest_topics(self, user_style: Dict[str, Any]) -> List[str]:
        """Suggest topics based on user style and interests"""

        common_topics = user_style.get("common_topics", [])

        # Expand on user's interests
        topic_expansions = {
            "technology": ["AI advancements", "programming languages", "cloud computing"],
            "business": ["digital marketing", "leadership", "innovation"],
            "health": ["mental wellness", "nutrition science", "fitness trends"],
            "education": ["online learning", "skill development", "teaching methods"]
        }

        suggestions = []
        for topic in common_topics:
            expansions = topic_expansions.get(topic, [f"Advanced {topic} concepts"])
            suggestions.extend(expansions[:2])

        return suggestions[:5] if suggestions else ["AI and technology trends", "Personal development", "Industry insights"]

    def _suggest_content_types(self, user_style: Dict[str, Any]) -> List[str]:
        """Suggest optimal content types"""

        preferred_formats = user_style.get("preferred_formats", [])

        if preferred_formats:
            return preferred_formats[:3]
        else:
            return ["blog_post", "social_media", "newsletter"]

    def _analyze_successful_themes(self, performance_data: List[Dict[str, Any]]) -> List[str]:
        """Analyze what themes perform well"""

        successful_themes = []

        for item in performance_data:
            metadata = item.get("metadata", {})
            engagement = metadata.get("engagement", 0)

            if engagement > 0.6:
                # Extract theme from title or content
                content = item.get("content", "")
                # Simple theme extraction
                if "guide" in content.lower():
                    successful_themes.append("how-to guides")
                elif "tips" in content.lower():
                    successful_themes.append("tips and tricks")
                elif "explained" in content.lower():
                    successful_themes.append("explanations")

        return list(set(successful_themes))[:3]

    def _identify_improvement_areas(self, performance_data: List[Dict[str, Any]]) -> List[str]:
        """Identify areas for content improvement"""

        improvements = []

        avg_engagement = sum(
            item.get("metadata", {}).get("engagement", 0)
            for item in performance_data
        ) / len(performance_data) if performance_data else 0

        if avg_engagement < 0.5:
            improvements.append("Increase engagement with more interactive elements")
        if len(performance_data) < 5:
            improvements.append("Create more content to establish patterns")
        if avg_engagement > 0.8:
            improvements.append("Continue with successful content strategies")

        return improvements

# Usage
content_assistant = ContentCreationAssistant()

# Analyze user style
user_style = content_assistant.analyze_user_style("creator_456")
print(f"User Style Analysis: {user_style}")

# Generate content idea
idea = content_assistant.generate_content_idea("creator_456", "machine learning", "blog_post")
print(f"Content Idea: {idea['suggested_title']}")
print(f"Key Points: {idea['key_points'][:2]}")

# Track performance
content_assistant.track_content_performance("creator_456", idea['suggested_title'], {
    "views": 1250,
    "engagement": 0.75,
    "shares": 25
})

# Get recommendations
recommendations = content_assistant.get_content_recommendations("creator_456")
print(f"Content Recommendations: {recommendations}")
```

## 🎯 Best Practices

### Application Architecture

1. **Memory-First Design**: Design applications with memory as a core component
2. **Context Awareness**: Use memory to maintain context across interactions
3. **Personalization**: Leverage memory for personalized user experiences
4. **Scalability**: Design memory systems that scale with application growth
5. **Privacy Compliance**: Implement proper data protection and user consent

### Implementation Guidelines

1. **Error Handling**: Implement robust error handling for memory operations
2. **Fallback Strategies**: Provide fallbacks when memory is unavailable
3. **Performance Monitoring**: Track memory operation performance
4. **Data Validation**: Validate memory data integrity and consistency
5. **Regular Maintenance**: Implement memory cleanup and optimization routines

## 📈 Next Steps

With memory-enabled applications mastered, you're ready to:

- **[Chapter 7: Performance Optimization](07-performance-optimization.md)** - Scaling memory systems for production workloads
- **[Chapter 8: Deployment & Monitoring](08-production-deployment.md)** - Deploying memory-enabled AI systems at scale

---

**Ready to build production-ready memory applications? Continue to [Chapter 7: Performance Optimization](07-performance-optimization.md)!** 🚀