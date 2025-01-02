import streamlit as st
import time
from model import transcribeVoiceContentToText
from st_copy_to_clipboard import st_copy_to_clipboard

def main():    
    st.title("Speech2Text transcriber")

    # Custom CSS for ChatGPT-like response
    st.markdown("""
        <style>        
        .st-emotion-cache-1gulkj5 {
            width: 100%;
            padding: 5em 2em;
        }
        </style>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(label="", accept_multiple_files=False, type=["mpeg", "mp4", "mpga", "m4a", "wav", "webm"])

    if uploaded_file is not None:
        audio_content = transcribeVoiceContentToText(uploaded_file)
        st.session_state.file_contents = audio_content

    st.header("Transcription:")
    if 'file_contents' in st.session_state:
        full_text = st.session_state.file_contents
        words = full_text.split()
        output_text = ""
        placeholder = st.empty()
        
        for word in words:
            output_text += word + " "
            placeholder.markdown(f"<div class='chat-response'>{output_text}</div>", unsafe_allow_html=True)
            time.sleep(0.05)
        st_copy_to_clipboard(full_text)
        
    else:
        st.write("No audio uploaded yet.")

if __name__ == "__main__":
    main()