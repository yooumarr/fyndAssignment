import streamlit as st
from database import db
import llm_utils as llm
from datetime import datetime

st.set_page_config(
    page_title="Feedback System - User",
    layout="centered"
)

# Header
st.title("User Feedback")
st.write("Share your experience with us! We value your feedback.")

# Feedback Form
with st.form("feedback_form"):
    st.subheader("Your Feedback")
    
    # Star rating
    rating = st.slider("Rate your experience", 1, 5, 4, 
                      help="1 = Poor, 5 = Excellent")
    
    # Display stars visually
    stars_display = "⭐" * rating + "☆" * (5 - rating)
    st.write(f"**Selected Rating:** {stars_display}")
    
    # Review text
    review = st.text_area(
        "Your review",
        placeholder="Tell us about your experience...",
        height=120
    )
    
    submit_button = st.form_submit_button("Submit Feedback")

# Process submission
if submit_button:
    if not review.strip():
        review = "No written feedback provided."
    
    with st.spinner("Generating AI response..."):
        # Get AI analysis
        ai_result = llm.analyze_review(rating, review)
        
        # Get sentiment
        sentiment = llm.get_sentiment(rating, review)
        
        # Store in database
        submission_id = db.add_submission(
            user_rating=rating,
            user_review=review,
            ai_response=ai_result["user_response"],
            ai_summary=ai_result["summary"],
            ai_actions=ai_result["actions"],
            sentiment=sentiment
        )
    
    if submission_id:
        # Success message
        st.success("Thank you for your feedback!")
        
        # Display AI response
        st.subheader("Our Response to You")
        st.info(ai_result["user_response"])
        
        # Submission details
        with st.expander("Submission Details", expanded=False):
            st.write(f"**Submission ID:** {submission_id}")
            st.write(f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Your Rating:** {rating}/5")
            st.write(f"**Your Review:** {review}")
    else:
        st.error("Failed to save your feedback. Please try again.")
    
    # Reset option
    if st.button("Submit Another Review"):
        st.rerun()
