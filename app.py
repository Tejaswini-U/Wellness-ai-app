import streamlit as pd  # Matches your original import aliases
import streamlit as st
from groq import Groq
import os
import pandas as pd_real
import plotly.express as px
from datetime import datetime

# # 1. Set up the Streamlit page style
st.set_page_config(page_title="Wellness AI Workspace", page_icon="🧘", layout="wide")

# # 2. Safely get your Groq API key
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] # Put your working gsk_ key here!

# Create a Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Mindful AI Chat", "Mood Analytics Dashboard", "Guided Exercises"])

# ==========================================
# PAGE 1: YOUR EXISTING CHAT CODE
# ==========================================
if page == "Mindful AI Chat":
    st.title("🧎 Personal Wellness & Mindful AI")
    st.write("Welcome to your safe, private space. How are you feeling today?")
    
    # # 3. Initialize the Groq client
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # # 4. Initialize chat history in browser memory
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I am your wellness companion. I'm here to listen, offer mindfulness exercises, or just chat."}
            ]
            
        # # 5. Display past chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # # 6. Handle user input
        if user_input := st.chat_input("Type your message here..."):
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Request response from Groq
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                ai_response = response.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error connecting to Groq: {e}")
                
    except Exception as e:
        st.error("Please provide a valid Groq API key to start.")

# ==========================================
# PAGE 2: MOOD ANALYTICS DASHBOARD
# ==========================================
elif page == "Mood Analytics Dashboard":
    st.title("📊 Mood Analytics Dashboard")
    st.write("Log your mental state to track visual wellness trends over time.")
    
    # Initialize a mock tracking file if it doesn't exist
    if "mood_data" not in st.session_state:
        st.session_state.mood_data = pd_real.DataFrame({
            "Date": ["2026-07-10", "2026-07-11", "2026-07-12", "2026-07-13"],
            "Mood Score": [3, 4, 2, 5],
            "Energy Level": [4, 3, 3, 4]
        })
        
    # Input panel
    st.subheader("Log Your State for Today")
    col1, col2 = st.columns(2)
    with col1:
        mood = st.slider("Rate your mood (1 = Low, 5 = Excellent)", 1, 5, 3)
    with col2:
        energy = st.slider("Rate your energy level (1 = Exhausted, 5 = High)", 1, 5, 3)
        
    if st.button("Save Daily Log Entry"):
        new_entry = pd_real.DataFrame({
            "Date": [datetime.now().strftime("%Y-%m-%d")], 
            "Mood Score": [mood], 
            "Energy Level": [energy]
        })
        st.session_state.mood_data = pd_real.concat([st.session_state.mood_data, new_entry], ignore_index=True)
        st.success("Entry added to local session ledger!")

    # Render Visual Chart
    st.subheader("Your Analytics Trends")
    fig = px.line(st.session_state.mood_data, x="Date", y=["Mood Score", "Energy Level"], title="Mental Health Metrics Tracking Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 3: GUIDED EXERCISES
# ==========================================
elif page == "Guided Exercises":
    st.title("🧘 Immersive Mindfulness Modules")
    st.write("Interactive tools for real-time stress relief and focus tuning.")
    
    st.subheader("Box Breathing Assistant")
    st.write("Follow the baseline visual count instructions below:")
    
    # Visual layout blocks
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Step 1", "Inhale (4s)")
    b2.metric("Step 2", "Hold (4s)")
    b3.metric("Step 3", "Exhale (4s)")
    b4.metric("Step 4", "Hold (4s)")
    
    st.info("Tip: Close your eyes, sit up straight, and run through 4 complete cycles of this breathing sequence.")