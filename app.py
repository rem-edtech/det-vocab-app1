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
words = data['vocabulary']
random.shuffle(words)

if 'index' not in st.session_state or 'file' not in st.session_state or st.session_state.file != selected_file:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.file = selected_file

st.title("DET: Read and Select")
st.caption(f"Currently playing: {data['week_title']}")

if st.session_state.index < len(words):
    current = words[st.session_state.index]
    st.markdown(f"<h1 style='text-align: center; font-size: 70px;'>{current['word']}</h1>", unsafe_allow_html=True)
    
    progress_bar = st.progress(100)
    col1, col2 = st.columns(2)
    with col1:
        yes = st.button("YES", use_container_width=True)
    with col2:
        no = st.button("NO", use_container_width=True)

    for i in range(50, 0, -1):
        progress_bar.progress(i * 2)
        if yes:
            if current['is_real']: st.session_state.score += 1
            st.session_state.index += 1
            st.rerun()
        if no:
            if not current['is_real']: st.session_state.score += 1
            st.session_state.index += 1
            st.rerun()
        time.sleep(0.1)

    st.session_state.index += 1
    st.rerun()
else:
    st.success("Lesson Complete!")
    st.metric("Final Score", f"{st.session_state.score} / {len(words)}")
    if st.button("Try Again"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()
