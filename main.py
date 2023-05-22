import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import os
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
whisper_model = whisper.load_model("base") 
openai.api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="arGPT - An Arabic ChatGPT Streamlit Conversational Bot")
#Title
st.title(':green[ar]GPT - An :green[Arabic] ChatGPT Streamlit Conversational Bot')

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
    text_response = whisper_model.transcribe(wav_file.name,language='ar')['text'] 
    print(text_response)
if user_input: 
    st.session_state.messages.append(HumanMessage(content=user_input)) 
    with st.spinner("Processing..."): 
        response = chat(st.session_state.messages) 
    st.session_state.messages.append(AIMessage(content=response.content)) 
messages = st.session_state.get('messages',[]) 
for i , msg in enumerate(messages[1:]): 
    if i % 2 == 0: 
        message(msg.content,is_user=True,key=str(i)+'_user') 
    else: 
        message(msg.content,is_user=False,key=str(i)+'_ai')