---
layout: default
title: "Browser Use Tutorial - Chapter 7: Custom Actions"
nav_order: 7
has_children: false
parent: Browser Use Tutorial
---

# Chapter 7: Custom Actions - Building Domain-Specific Browser Actions

> Create custom browser actions for specialized tasks, domain-specific automation, and reusable automation components.

## Overview

Custom actions extend Browser Use beyond basic navigation and interaction. They enable domain-specific automation, reusable components, and complex task automation. This chapter covers creating and implementing custom browser actions.

## Custom Action Fundamentals

### Action Structure

```python
# custom_action_basics.py
from browser_use import Agent, Controller
from langchain_openai import ChatOpenAI
from browser_use.controller.service import ActionService
import asyncio

class CustomActionService(ActionService):
    """Custom action service for domain-specific operations"""

    def __init__(self):
        super().__init__()
        self.register_actions()

    def register_actions(self):
        """Register custom actions"""
        self.register_action("extract_product_data", self.extract_product_data)
        self.register_action("fill_contact_form", self.fill_contact_form)
        self.register_action("compare_prices", self.compare_prices)
        self.register_action("generate_report", self.generate_report)

    async def extract_product_data(self, page, **kwargs):
        """Extract product information from e-commerce pages"""
        try:
            # Custom product extraction logic
            title = await page.locator('h1.product-title').text_content()
            price = await page.locator('.price').text_content()
            description = await page.locator('.product-description').text_content()

            return {
                "title": title.strip(),
                "price": price.strip(),
                "description": description.strip(),
                "url": page.url
            }
        except Exception as e:
            return {"error": f"Failed to extract product data: {str(e)}"}

    async def fill_contact_form(self, page, name, email, message):
        """Fill out contact forms automatically"""
        try:
            await page.fill('input[name="name"]', name)
            await page.fill('input[name="email"]', email)
            await page.fill('textarea[name="message"]', message)
            await page.click('button[type="submit"]')

            return {"status": "Contact form submitted successfully"}
        except Exception as e:
            return {"error": f"Failed to fill contact form: {str(e)}"}

    async def compare_prices(self, page, product_name):
        """Compare prices across different retailers"""
        # Implementation for price comparison
        pass

    async def generate_report(self, page, data, format="html"):
        """Generate reports from collected data"""
        # Implementation for report generation
        pass

async def custom_action_demo():
    """Demonstrate custom actions"""

    # Create custom controller
    controller = Controller()
    custom_service = CustomActionService()
    controller.add_service(custom_service)

    agent = Agent(
        task="""
        Use custom actions to perform specialized tasks:

        1. Go to an e-commerce product page
        2. Use the extract_product_data action to get product info
        3. Go to a contact page
        4. Use fill_contact_form to send an inquiry
        5. Generate a report of the actions performed

        Demonstrate the power of domain-specific automation.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        controller=controller,
        max_steps=30
    )

    result = await agent.run()
    print(f"Custom Actions Result: {result}")

if __name__ == "__main__":
    asyncio.run(custom_action_demo())
```

### Action Registration and Discovery

```python
# action_registration.py
from browser_use.controller.service import ActionService
from typing import Dict, Any, List
import json

class ActionRegistry:
    """Registry for custom actions"""

    def __init__(self):
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.load_builtin_actions()

    def load_builtin_actions(self):
        """Load built-in actions"""
        self.register_action({
            "name": "navigate_to",
            "description": "Navigate to a URL",
            "parameters": {
                "url": {"type": "string", "description": "URL to navigate to"}
            }
        })

        self.register_action({
            "name": "extract_text",
            "description": "Extract text from page elements",
            "parameters": {
                "selector": {"type": "string", "description": "CSS selector"},
                "multiple": {"type": "boolean", "description": "Extract multiple elements"}
            }
        })

    def register_action(self, action_def: Dict[str, Any]):
        """Register a custom action"""
        name = action_def["name"]
        self.actions[name] = action_def

    def get_action(self, name: str) -> Dict[str, Any]:
        """Get action definition"""
        return self.actions.get(name)

    def list_actions(self) -> List[str]:
        """List all registered actions"""
        return list(self.actions.keys())

    def get_action_schema(self, name: str) -> Dict[str, Any]:
        """Get JSON schema for action"""
        action = self.get_action(name)
        if action:
            return {
                "type": "object",
                "properties": action.get("parameters", {}),
                "required": action.get("required", [])
            }
        return {}

# Global registry instance
action_registry = ActionRegistry()
```

## Domain-Specific Actions

### E-commerce Actions

```python
# ecommerce_actions.py
from browser_use.controller.service import ActionService
import asyncio

class EcommerceActionService(ActionService):
    """Custom actions for e-commerce automation"""

    def __init__(self):
        super().__init__()
        self.register_ecommerce_actions()

    def register_ecommerce_actions(self):
        """Register e-commerce specific actions"""
        self.register_action("search_products", self.search_products)
        self.register_action("add_to_cart", self.add_to_cart)
        self.register_action("checkout_process", self.checkout_process)
        self.register_action("price_comparison", self.price_comparison)

    async def search_products(self, page, query, category=None):
        """Search for products on e-commerce site"""
        try:
            # Enter search query
            await page.fill('input[name="q"]', query)

            # Select category if provided
            if category:
                await page.select_option('select[name="category"]', category)

            # Submit search
            await page.click('button[type="submit"]')

            # Wait for results
            await page.wait_for_selector('.product-results')

            # Extract product information
            products = await page.query_selector_all('.product-item')

            results = []
            for product in products[:5]:  # First 5 results
                title = await product.query_selector('.product-title')
                price = await product.query_selector('.product-price')

                results.append({
                    "title": await title.text_content() if title else "",
                    "price": await price.text_content() if price else "",
                    "url": await product.get_attribute('href') or ""
                })

            return {
                "query": query,
                "results_count": len(results),
                "products": results
            }

        except Exception as e:
            return {"error": f"Product search failed: {str(e)}"}

    async def add_to_cart(self, page, product_url=None, quantity=1):
        """Add product to shopping cart"""
        try:
            if product_url:
                await page.goto(product_url)

            # Find and click add to cart button
            add_to_cart_btn = await page.query_selector('button.add-to-cart, .add-to-cart-btn')

            if add_to_cart_btn:
                # Set quantity if needed
                if quantity > 1:
                    qty_input = await page.query_selector('input[name="quantity"]')
                    if qty_input:
                        await qty_input.fill(str(quantity))

                await add_to_cart_btn.click()

                # Wait for cart update
                await page.wait_for_selector('.cart-updated, .cart-count')

                return {"status": "Product added to cart", "quantity": quantity}
            else:
                return {"error": "Add to cart button not found"}

        except Exception as e:
            return {"error": f"Add to cart failed: {str(e)}"}

    async def checkout_process(self, page):
        """Complete checkout process"""
        try:
            # Navigate to checkout if not already there
            if 'checkout' not in page.url:
                await page.click('.checkout-btn, [href*="checkout"]')
                await page.wait_for_load_state('networkidle')

            # Fill shipping information
            await page.fill('input[name="firstName"]', 'John')
            await page.fill('input[name="lastName"]', 'Doe')
            await page.fill('input[name="email"]', 'john.doe@example.com')
            await page.fill('input[name="address"]', '123 Main St')
            await page.fill('input[name="city"]', 'Anytown')
            await page.select_option('select[name="state"]', 'CA')
            await page.fill('input[name="zipCode"]', '12345')

            # Select shipping method
            await page.click('input[name="shipping"][value="standard"]')

            # Continue to payment
            await page.click('button:contains("Continue"), .continue-btn')

            return {"status": "Checkout information completed"}

        except Exception as e:
            return {"error": f"Checkout process failed: {str(e)}"}

    async def price_comparison(self, page, product_name):
        """Compare prices across different sites"""
        # Implementation would involve multiple tabs/sites
        # This is a simplified version
        try:
            # Search for product
            search_results = await self.search_products(page, product_name)

            # Analyze prices
            prices = []
            for product in search_results.get('products', []):
                price_text = product.get('price', '')
                # Parse price (simplified)
                if '$' in price_text:
                    price = float(price_text.replace('$', '').replace(',', ''))
                    prices.append(price)

            if prices:
                return {
                    "product": product_name,
                    "min_price": min(prices),
                    "max_price": max(prices),
                    "avg_price": sum(prices) / len(prices),
                    "results_count": len(prices)
                }
            else:
                return {"error": "No prices found"}

        except Exception as e:
            return {"error": f"Price comparison failed: {str(e)}"}
```

### Social Media Actions

```python
# social_media_actions.py
from browser_use.controller.service import ActionService
import asyncio

class SocialMediaActionService(ActionService):
    """Custom actions for social media automation"""

    def __init__(self):
        super().__init__()
        self.register_social_actions()

    def register_social_actions(self):
        """Register social media actions"""
        self.register_action("post_content", self.post_content)
        self.register_action("analyze_engagement", self.analyze_engagement)
        self.register_action("follow_users", self.follow_users)
        self.register_action("extract_posts", self.extract_posts)

    async def post_content(self, page, content, platform="twitter"):
        """Post content to social media"""
        try:
            if platform == "twitter":
                # Twitter/X posting
                await page.fill('[data-testid="tweetTextarea_0"]', content)
                await page.click('[data-testid="tweetButtonInline"]')

            elif platform == "linkedin":
                # LinkedIn posting
                await page.click('.share-box__open')
                await page.fill('.editor-content', content)
                await page.click('.share-actions__primary-action')

            elif platform == "facebook":
                # Facebook posting
                await page.fill('[data-testid="status-attachment-mentions-input"]', content)
                await page.click('[data-testid="react-composer-post-button"]')

            return {"status": f"Content posted to {platform}", "content_length": len(content)}

        except Exception as e:
            return {"error": f"Posting failed: {str(e)}"}

    async def analyze_engagement(self, page, post_url):
        """Analyze engagement metrics for a post"""
        try:
            await page.goto(post_url)

            # Extract engagement metrics
            likes = await page.query_selector('[data-testid*="like"], .like-count')
            retweets = await page.query_selector('[data-testid*="retweet"], .retweet-count')
            replies = await page.query_selector('[data-testid*="reply"], .reply-count')
            views = await page.query_selector('.view-count, [data-testid*="view"]')

            metrics = {
                "likes": await likes.text_content() if likes else "0",
                "retweets": await retweets.text_content() if retweets else "0",
                "replies": await replies.text_content() if replies else "0",
                "views": await views.text_content() if views else "0"
            }

            return {
                "post_url": post_url,
                "engagement_metrics": metrics
            }

        except Exception as e:
            return {"error": f"Engagement analysis failed: {str(e)}"}

    async def follow_users(self, page, usernames):
        """Follow users on social media"""
        try:
            followed = []

            for username in usernames:
                try:
                    # Navigate to user profile
                    await page.goto(f"https://twitter.com/{username}")

                    # Click follow button
                    follow_btn = await page.query_selector('[data-testid="follow"], .follow-button')
                    if follow_btn:
                        await follow_btn.click()
                        followed.append(username)

                        # Small delay to avoid rate limiting
                        await asyncio.sleep(1)

                except Exception as e:
                    continue  # Skip failed follows

            return {
                "attempted": len(usernames),
                "successful": len(followed),
                "followed_users": followed
            }

        except Exception as e:
            return {"error": f"Follow operation failed: {str(e)}"}

    async def extract_posts(self, page, username, limit=10):
        """Extract recent posts from a user"""
        try:
            await page.goto(f"https://twitter.com/{username}")

            # Wait for posts to load
            await page.wait_for_selector('[data-testid="tweetText"]')

            # Extract posts
            posts = []
            post_elements = await page.query_selector_all('[data-testid="tweetText"]')

            for i, post_elem in enumerate(post_elements[:limit]):
                try:
                    text = await post_elem.text_content()
                    timestamp = await post_elem.query_selector('time')
                    time_text = await timestamp.get_attribute('datetime') if timestamp else ""

                    posts.append({
                        "text": text.strip(),
                        "timestamp": time_text,
                        "url": f"https://twitter.com/{username}/status/some-id-{i}"
                    })

                except Exception as e:
                    continue

            return {
                "username": username,
                "posts_extracted": len(posts),
                "posts": posts
            }

        except Exception as e:
            return {"error": f"Post extraction failed: {str(e)}"}
```

## Advanced Custom Actions

### Machine Learning Integration

```python
# ml_actions.py
from browser_use.controller.service import ActionService
import asyncio
from typing import List, Dict, Any
import json

class MLActionsService(ActionService):
    """Custom actions with ML capabilities"""

    def __init__(self):
        super().__init__()
        self.register_ml_actions()

    def register_ml_actions(self):
        """Register ML-powered actions"""
        self.register_action("sentiment_analysis", self.sentiment_analysis)
        self.register_action("content_categorization", self.content_categorization)
        self.register_action("duplicate_detection", self.duplicate_detection)
        self.register_action("smart_extraction", self.smart_extraction)

    async def sentiment_analysis(self, page, text_elements: List[str]):
        """Analyze sentiment of text content"""
        try:
            # Extract text from specified elements
            sentiments = []

            for selector in text_elements:
                elements = await page.query_selector_all(selector)
                for elem in elements:
                    text = await elem.text_content()
                    if text.strip():
                        # Simple sentiment analysis (in real implementation, use ML model)
                        sentiment = self._analyze_sentiment(text.strip())
                        sentiments.append({
                            "text": text.strip()[:100] + "...",
                            "sentiment": sentiment
                        })

            return {
                "analysis_type": "sentiment",
                "total_elements": len(sentiments),
                "results": sentiments
            }

        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}

    async def content_categorization(self, page, content_selectors: List[str]):
        """Categorize content automatically"""
        try:
            categories = []

            for selector in content_selectors:
                elements = await page.query_selector_all(selector)
                for elem in elements:
                    text = await elem.text_content()
                    if text.strip():
                        category = self._categorize_content(text.strip())
                        categories.append({
                            "content": text.strip()[:100] + "...",
                            "category": category,
                            "confidence": 0.85  # Mock confidence score
                        })

            return {
                "analysis_type": "categorization",
                "total_categorized": len(categories),
                "categories": categories
            }

        except Exception as e:
            return {"error": f"Content categorization failed: {str(e)}"}

    async def duplicate_detection(self, page, content_list: List[str]):
        """Detect duplicate content"""
        try:
            # Simple duplicate detection (real implementation would use ML)
            seen_content = set()
            duplicates = []
            unique = []

            for content in content_list:
                normalized = content.lower().strip()
                if normalized in seen_content:
                    duplicates.append(content[:100] + "...")
                else:
                    seen_content.add(normalized)
                    unique.append(content[:100] + "...")

            return {
                "analysis_type": "duplicate_detection",
                "total_items": len(content_list),
                "unique_count": len(unique),
                "duplicate_count": len(duplicates),
                "duplicates": duplicates[:5]  # Show first 5 duplicates
            }

        except Exception as e:
            return {"error": f"Duplicate detection failed: {str(e)}"}

    async def smart_extraction(self, page, extraction_rules: Dict[str, Any]):
        """Smart content extraction with rules"""
        try:
            extracted_data = {}

            for field_name, rules in extraction_rules.items():
                selector = rules.get('selector')
                extraction_type = rules.get('type', 'text')

                if selector:
                    if extraction_type == 'text':
                        elem = await page.query_selector(selector)
                        if elem:
                            extracted_data[field_name] = await elem.text_content()
                        else:
                            extracted_data[field_name] = None

                    elif extraction_type == 'attribute':
                        elem = await page.query_selector(selector)
                        if elem:
                            attr = rules.get('attribute', 'href')
                            extracted_data[field_name] = await elem.get_attribute(attr)
                        else:
                            extracted_data[field_name] = None

                    elif extraction_type == 'multiple':
                        elements = await page.query_selector_all(selector)
                        extracted_data[field_name] = []
                        for elem in elements:
                            if rules.get('attribute'):
                                value = await elem.get_attribute(rules['attribute'])
                            else:
                                value = await elem.text_content()
                            extracted_data[field_name].append(value)

            return {
                "extraction_type": "smart",
                "rules_applied": len(extraction_rules),
                "extracted_data": extracted_data
            }

        except Exception as e:
            return {"error": f"Smart extraction failed: {str(e)}"}

    # Helper methods (simplified implementations)
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'poor']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _categorize_content(self, text: str) -> str:
        """Simple content categorization"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['price', 'cost', 'buy', 'purchase']):
            return "commerce"
        elif any(word in text_lower for word in ['news', 'article', 'story']):
            return "news"
        elif any(word in text_lower for word in ['tutorial', 'guide', 'how to']):
            return "educational"
        else:
            return "general"
```

## Action Composition and Workflows

### Composite Actions

```python
# composite_actions.py
from browser_use.controller.service import ActionService
import asyncio

class CompositeActionService(ActionService):
    """Actions that combine multiple operations"""

    def __init__(self):
        super().__init__()
        self.register_composite_actions()

    def register_composite_actions(self):
        """Register composite actions"""
        self.register_action("research_and_summarize", self.research_and_summarize)
        self.register_action("automated_testing", self.automated_testing)
        self.register_action("content_creation", self.content_creation)

    async def research_and_summarize(self, page, topic, sources=3):
        """Research a topic and create a summary"""
        try:
            research_data = []

            # Step 1: Search for information
            await page.goto(f"https://www.google.com/search?q={topic}")
            await page.wait_for_load_state('networkidle')

            # Extract search results
            results = await page.query_selector_all('.g .yuRUbf a')
            search_urls = []
            for result in results[:sources]:
                href = await result.get_attribute('href')
                if href:
                    search_urls.append(href)

            # Step 2: Visit each source and extract content
            for url in search_urls:
                try:
                    await page.goto(url)
                    await page.wait_for_load_state('networkidle')

                    # Extract main content (simplified)
                    title_elem = await page.query_selector('h1, .title, [data-testid="headline"]')
                    content_elem = await page.query_selector('article, .content, .post-content')

                    title = await title_elem.text_content() if title_elem else "No title"
                    content = await content_elem.text_content() if content_elem else ""

                    research_data.append({
                        "url": url,
                        "title": title.strip(),
                        "content": content.strip()[:500] + "..." if len(content) > 500 else content.strip()
                    })

                except Exception as e:
                    continue  # Skip failed sources

            # Step 3: Generate summary
            summary = f"Research on '{topic}': Found {len(research_data)} sources with relevant information."

            return {
                "topic": topic,
                "sources_researched": len(research_data),
                "summary": summary,
                "research_data": research_data
            }

        except Exception as e:
            return {"error": f"Research and summarize failed: {str(e)}"}

    async def automated_testing(self, page, test_scenarios):
        """Run automated tests on a web application"""
        try:
            test_results = []

            for scenario in test_scenarios:
                scenario_result = {
                    "scenario": scenario.get("name", "Unnamed"),
                    "status": "pending",
                    "steps": []
                }

                try:
                    # Execute test steps
                    for step in scenario.get("steps", []):
                        step_result = await self._execute_test_step(page, step)
                        scenario_result["steps"].append(step_result)

                        if not step_result.get("success", False):
                            scenario_result["status"] = "failed"
                            break

                    if scenario_result["status"] == "pending":
                        scenario_result["status"] = "passed"

                except Exception as e:
                    scenario_result["status"] = "error"
                    scenario_result["error"] = str(e)

                test_results.append(scenario_result)

            # Calculate summary
            passed = sum(1 for r in test_results if r["status"] == "passed")
            failed = sum(1 for r in test_results if r["status"] == "failed")
            errors = sum(1 for r in test_results if r["status"] == "error")

            return {
                "test_summary": {
                    "total_scenarios": len(test_results),
                    "passed": passed,
                    "failed": failed,
                    "errors": errors,
                    "success_rate": passed / len(test_results) if test_results else 0
                },
                "detailed_results": test_results
            }

        except Exception as e:
            return {"error": f"Automated testing failed: {str(e)}"}

    async def content_creation(self, page, content_spec):
        """Create content based on specifications"""
        try:
            content_type = content_spec.get("type", "article")
            topic = content_spec.get("topic", "")
            audience = content_spec.get("audience", "general")
            length = content_spec.get("length", "medium")

            # Research phase
            research_result = await self.research_and_summarize(page, topic, sources=2)

            # Content generation prompt
            generation_prompt = f"""
            Create a {length} {content_type} about "{topic}" for a {audience} audience.

            Research findings: {research_result.get('summary', '')}

            Key points from research:
            {chr(10).join(f"- {item['title']}: {item['content'][:100]}" for item in research_result.get('research_data', []))}

            Structure the content with:
            - Engaging introduction
            - Main content with examples
            - Practical applications
            - Conclusion with key takeaways
            """

            # Generate content (simplified - would use LLM)
            generated_content = f"""
# {topic}

## Introduction
Based on research from {len(research_result.get('research_data', []))} sources...

## Main Content
[Content would be generated here based on research]

## Applications
- Practical use case 1
- Practical use case 2

## Conclusion
Key takeaways from the research and analysis.
"""

            return {
                "content_type": content_type,
                "topic": topic,
                "audience": audience,
                "research_sources": len(research_result.get('research_data', [])),
                "generated_content": generated_content,
                "word_count": len(generated_content.split())
            }

        except Exception as e:
            return {"error": f"Content creation failed: {str(e)}"}

    async def _execute_test_step(self, page, step):
        """Execute a single test step"""
        step_type = step.get("type")
        target = step.get("target")
        action = step.get("action")
        value = step.get("value")

        try:
            if step_type == "navigation":
                await page.goto(target)
                await page.wait_for_load_state('networkidle')
                return {"step": step, "success": True, "message": f"Navigated to {target}"}

            elif step_type == "click":
                await page.click(target)
                return {"step": step, "success": True, "message": f"Clicked {target}"}

            elif step_type == "input":
                await page.fill(target, value)
                return {"step": step, "success": True, "message": f"Filled {target} with value"}

            elif step_type == "assert":
                # Check if element exists or has expected content
                if action == "exists":
                    elem = await page.query_selector(target)
                    success = elem is not None
                elif action == "text_contains":
                    elem = await page.query_selector(target)
                    if elem:
                        text = await elem.text_content()
                        success = value in text
                    else:
                        success = False

                return {
                    "step": step,
                    "success": success,
                    "message": f"Assertion {'passed' if success else 'failed'}"
                }

            else:
                return {"step": step, "success": False, "message": f"Unknown step type: {step_type}"}

        except Exception as e:
            return {"step": step, "success": False, "message": f"Step failed: {str(e)}"}
```

## Summary

In this chapter, we've covered:

- **Custom Action Fundamentals**: Structure and registration of custom actions
- **Domain-Specific Actions**: E-commerce, social media, and ML-powered actions
- **Advanced Actions**: Composite actions combining multiple operations
- **Action Composition**: Building complex workflows from simpler actions
- **Integration Patterns**: Connecting actions with external systems and APIs

## Key Takeaways

1. **Modular Design**: Break complex operations into reusable custom actions
2. **Domain Expertise**: Create actions tailored to specific business domains
3. **Composition**: Build complex workflows from simpler, composable actions
4. **Error Handling**: Implement robust error handling in custom actions
5. **Performance**: Optimize actions for speed and resource efficiency
6. **Integration**: Connect actions with external APIs and data sources
7. **Testing**: Thoroughly test custom actions before production use

## Next Steps

Now that you can create custom actions, let's explore **production deployment** with scaling, reliability, and best practices.

---

**Ready for Chapter 8?** [Production Deployment](08-production.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*