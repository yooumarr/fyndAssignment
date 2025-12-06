import streamlit as st
from database import db
import plotly.express as px
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title='Feedback System - Admin',
    layout='wide'
)

# Header
st.title("Admin Analytics Dashboard")
st.write("Real-time customer feedback analysis")

# Refresh button
col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Refresh Data"):
        st.rerun()
with col2:
    st.write(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# Get data
df = db.get_all_submissions()
stats = db.get_stats()

# Dashboard metrics
st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Submissions", stats["total_submissions"])

with col2:
    st.metric("Average Rating", 
             f"{stats['average_rating']:.1f}/5",
             delta=None)

with col3:
    positive = stats["sentiment_distribution"].get("positive", 0)
    st.metric("Positive Feedback", positive)

with col4:
    st.metric("Latest Submission", 
             "Now" if not df.empty else "None",
             delta=None)

# Detailed submissions table
st.subheader("All Submissions")

if not df.empty:
    # Show expandable details for each row
    for idx, row in df.iterrows():
        timestamp_str = row.get('timestamp_str', str(row.get('timestamp', 'N/A'))[:16])
        
        with st.expander(f"Submission {row['id'][:8]} - {timestamp_str} - {row['user_rating']}⭐"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**👤 User Feedback**")
                st.write(f"**Rating:** {row['user_rating']}/5")
                st.write(f"**Review:** {row['user_review']}")
                st.write(f"**Sentiment:** {row['sentiment']}")
            
            with col2:
                st.write("**AI Analysis**")
                st.write(f"**AI Response to User:**")
                st.info(row['ai_response'])
                st.write(f"**Internal Summary:**")
                st.success(row['ai_summary'])
                st.write(f"**Recommended Actions:**")
                st.warning(row['ai_actions'])
    
else:
    st.info("No submissions yet. Feedback will appear here when users submit.")

# Charts
if not df.empty:
    st.subheader("Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating distribution
        st.write("**Rating Distribution**")
        rating_counts = df['user_rating'].value_counts().sort_index()
        fig1 = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={'x': 'Stars', 'y': 'Count'},
            color=rating_counts.index,
            color_continuous_scale='viridis'
        )
        fig1.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        st.write("**Sentiment Analysis**")
        sentiment_counts = df['sentiment'].value_counts()
        fig2 = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': 'green',
                'neutral': 'orange',
                'negative': 'red'
            }
        )
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)