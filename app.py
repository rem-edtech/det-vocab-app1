import streamlit as st
import json
import time
import os
import random

def load_data(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

st.set_page_config(page_title="DET Vocab Practice", layout="centered")

# --- Initialize Global State ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

# Sidebar Logic
st.sidebar.title("Navigation")

# Show "Start Over" button in sidebar if quiz is active
if st.session_state.quiz_started:
    if st.sidebar.button("Quit & Start Over"):
        st.session_state.quiz_started = False
        if 'active_words' in st.session_state:
            del st.session_state.active_words
        st.rerun()

# --- LOBBY / START SCREEN ---
if not st.session_state.quiz_started:
    if not st.session_state.quiz_started:
        st.title("DET Readiness: Academic Vocabulary Practice Lab")
    
    # Using triple quotes for line breaks and bullets
        st.write("""
        **Welcome!** Select a vocabulary list to begin. Each list has a slightly different focus.
        Each list contains 50 real & 50 'fake' English words. 
        Each time you begin a practice session, a **random** set of 20 words will be shown.
        * **Week1.json:** Core academic words and common phonetic patterns.
        * **Week3.json:** Advanced suffixes and morphological "trap" words.
    
        Click **START PRACTICE SESSION** when you have chosen a list.
        """)
    
    json_files = sorted([f for f in os.listdir('.') if f.endswith('.json')])
    selected_file = st.selectbox("Choose your word list:", json_files)
    
    # Preview title
    temp_data = load_data(selected_file)
    st.info(f"Target Lesson: {temp_data['week_title']}")
    
    if st.button("START PRACTICE SESSION", use_container_width=True, type="primary"):
        st.session_state.file = selected_file
        st.session_state.quiz_started = True
        st.rerun()

# --- QUIZ ENGINE ---
else:
    data = load_data(st.session_state.file)

    # Initialize current round if needed
    if 'active_words' not in st.session_state or st.session_state.file != st.session_state.get('last_file'):
        all_pool = data['vocabulary']
        random.shuffle(all_pool)
        st.session_state.active_words = all_pool[:20]
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.history = []
        st.session_state.last_file = st.session_state.file

    words = st.session_state.active_words

    st.title("DET Practice")
    st.caption(f"Playing: {data['week_title']}")

    if st.session_state.index < len(words):
        current = words[st.session_state.index]
        st.markdown(f"<h1 style='text-align: center; font-size: 70px;'>{current['word']}</h1>", unsafe_allow_html=True)
        
        progress_bar = st.progress(100)
        col1, col2 = st.columns(2)
        
        with col1:
            yes = st.button("YES", use_container_width=True)
        with col2:
            no = st.button("NO", use_container_width=True)

        # 5-second countdown
        for i in range(50, 0, -1):
            progress_bar.progress(i * 2)
            user_choice = None
            if yes: user_choice = True
            if no: user_choice = False
                
            if user_choice is not None:
                is_correct = (user_choice == current['is_real'])
                if is_correct: 
                    st.session_state.score += 1
                
                st.session_state.history.append({
                    "Word": current['word'],
                    "Your Answer": "YES" if user_choice else "NO",
                    "Correct?": "✅" if is_correct else "❌",
                    "Real Word?": "Yes" if current['is_real'] else "No"
                })
                st.session_state.index += 1
                st.rerun()
            time.sleep(0.1)

        # Timeout logic
        st.session_state.history.append({
            "Word": current['word'],
            "Your Answer": "Time Up",
            "Correct?": "❌",
            "Real Word?": "Yes" if current['is_real'] else "No"
        })
        st.session_state.index += 1
        st.rerun()

    else:
        # RESULT SCREEN
        st.success("Lesson Complete!")
        st.metric("Final Score", f"{st.session_state.score} / {len(words)}")
        st.subheader("Review Your Answers")
        st.table(st.session_state.history)
        
        if st.button("Return to Lobby"):
            st.session_state.quiz_started = False
            del st.session_state.active_words
            st.rerun()
