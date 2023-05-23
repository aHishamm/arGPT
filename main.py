from gtts import gTTS
from mutagen.mp3 import MP3 
import base64 
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import time 
import openai
import whisper
import streamlit as st 
from audiorecorder import audiorecorder
from dotenv import load_dotenv
load_dotenv() 
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
whisper_model = whisper.load_model("medium") 
openai.api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="arGPT - An Arabic ChatGPT Streamlit Conversational Bot")
#Title
st.title(':green[ar]GPT - An :green[Arabic] ChatGPT Streamlit Conversational Bot')
def autoplay_audio(file_path, lenn): 
    with open(file_path,"rb") as f: 
        data = f.read() 
        b64 = base64.b64encode(data).decode() 
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        sound = st.empty() 
        sound.markdown(
            md,
            unsafe_allow_html=True,
        )
        time.sleep(int(lenn)+3)
        sound.empty() 

def audio_to_text(audio): 
    text_response = whisper_model.transcribe(audio.name,language='ar')['text'] 
    return text_response 
chat = ChatOpenAI(temperature=0) 
if "messages" not in st.session_state: 
    st.session_state.messages = [SystemMessage(content="You are a helpful AI assistant, translate your responses to Arabic")] 
user_input = st.text_input("Your message: ",key='user_input')
audio_bytes = audiorecorder("Click to record","Recording...") 
if len(audio_bytes > 0): 
    st.audio(audio_bytes.tobytes())
    wav_file = open("audio.mp3", "wb")
    wav_file.write(audio_bytes.tobytes())
    user_input = whisper_model.transcribe(wav_file.name,language='ar')['text'] 
if user_input: 
    st.session_state.messages.append(HumanMessage(content=user_input)) 
    with st.spinner("Processing..."): 
        response = chat(st.session_state.messages)
        print(response.content) 
        #converting AI output to speech mp3 file 
        tts = gTTS(response.content,lang='ar')  
        tts.save('response.mp3')
        aud = MP3('response.mp3')
        autoplay_audio('response.mp3',aud.info.length)
    st.session_state.messages.append(AIMessage(content=response.content)) 
messages = st.session_state.get('messages',[]) 
for i , msg in enumerate(messages[1:]): 
    if i % 2 == 0: 
        message(msg.content,is_user=True,key=str(i)+'_user') 
    else: 
        message(msg.content,is_user=False,key=str(i)+'_ai')