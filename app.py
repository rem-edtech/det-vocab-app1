import streamlit as st
import json
import time
import os
import random

def load_data(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

st.set_page_config(page_title="DET Vocab Practice", layout="centered")

# Sidebar for word list selection
st.sidebar.title("Lesson Selection")
json_files = [f for f in os.listdir('.') if f.endswith('.json')]
selected_file = st.sidebar.selectbox("Choose a week:", json_files)

data = load_data(selected_file)

# --- Session State Initialization ---
if 'active_words' not in st.session_state or st.session_state.file != selected_file:
    all_pool = data['vocabulary']
    random.shuffle(all_pool)
    st.session_state.active_words = all_pool[:20]
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.file = selected_file
    st.session_state.history = [] # NEW: To store results

words = st.session_state.active_words

st.title("DET: Read and Select")
st.caption(f"Currently playing: {data['week_title']}")

# Quiz Section
if st.session_state.index < len(words):
    current = words[st.session_state.index]
    st.markdown(f"<h1 style='text-align: center; font-size: 70px;'>{current['word']}</h1>", unsafe_allow_html=True)
    
    progress_bar = st.progress(100)
    col1, col2 = st.columns(2)
    
    with col1:
        yes = st.button("YES", use_container_width=True)
    with col2:
        no = st.button("NO", use_container_width=True)

    # Timer logic (5 seconds)
    for i in range(50, 0, -1):
        progress_bar.progress(i * 2)
        
        user_choice = None
        if yes: user_choice = True
        if no: user_choice = False
            
        if user_choice is not None:
            # Check if correct
            is_correct = (user_choice == current['is_real'])
            if is_correct: 
                st.session_state.score += 1
            
            # Record in History
            st.session_state.history.append({
                "Word": current['word'],
                "Your Answer": "YES" if user_choice else "NO",
                "Correct?": "✅" if is_correct else "❌",
                "Real Word?": "Yes" if current['is_real'] else "No"
            })
            
            st.session_state.index += 1
            st.rerun()
            
        time.sleep(0.1)

    # Time's Up Logic
    st.session_state.history.append({
        "Word": current['word'],
        "Your Answer": "No Answer (Time Up)",
        "Correct?": "❌",
        "Real Word?": "Yes" if current['is_real'] else "No"
    })
    st.session_state.index += 1
    st.rerun()

else:
    st.success("Lesson Complete!")
    st.metric("Final Score", f"{st.session_state.score} / {len(words)}")
    
    # NEW: Display the Results Table
    st.subheader("Review Your Answers")
    st.table(st.session_state.history)
    
    if st.button("Try Again (New Random 20)"):
        del st.session_state.active_words 
        del st.session_state.history
        st.rerun()
