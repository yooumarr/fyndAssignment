import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def call_gemini(prompt, max_retries=3):
    """Call Gemini API with retry logic"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config={"temperature":0.3}
            )
            return response.text.strip()
        except Exception as e:
            if attempt < max_retries -1:
                time.sleep(5)
            else:
                print(f"Gemini API error: {e}")
                return ''
    return ''

def analyze_review(rating, review_text):
    """
    Generate all three AI outputs for a review:
    1. User response (friendly)
    2. Summary (for admin)
    3. Recommended actions (for admin)
    """
    #prompt
    prompt = f"""
    You are analyzing a customer review for a business.

    RATING: {rating}/5 stars
    REVIEW: {review_text}

    Generate THREE outputs:

    1. USER RESPONSE: A friendly, professional response to show the customer (2-3 sentences).
    2. SUMMARY: A one-sentence internal summary for the business team.
    3. ACTIONS: 1-2 recommended actions for the business based on this feedback.

    Return your answer as valid JSON with these exact keys:
    {{
        "user_response": "text here",
        "summary": "text here", 
        "actions": "text here"
    }}

    Do not include any other text, only JSON.
    """

    response = call_gemini(prompt)

    #parse json response
    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        json_str = response[start:end]
        result = json.loads(json_str)

        # validate keys
        required_keys = ['user_response','summary','actions']
        for key in required_keys:
            if key not in result:
                result[key] = f"Error: Missing {key}"

        return result
    
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "user_response": "Thank you for your feedback! We appreciate you taking the time to share your experience.",
            "summary": f"{rating}-star review: Could not parse AI analysis",
            "actions": "Review this feedback manually for insights."
        }
    
def get_sentiment(rating, review_text):
    """Simple sentiment detection based on rating and keywords."""
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"