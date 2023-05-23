# arGPT 
arGPT is an Arabic LLM-powered conversational bot, the application uses streamlit as a frontend. The LangChain LLM framework is used to create the core of the conversational bot experience, I incorporated OpenAI's Whisper ASR for the speech to text component of the conversational bot. 
#### Prerequisites 
1. Anaconda installed on the system 
2. Create an environment for this project (recommended) and install the packages listed in requirements.txt 
```bash 
conda create -n openai python==3.10 
conda activate openai 
pip install -r requirements.txt 
``` 
3. Add an .env file containing the following environment variables: 
```bash
OPENAI_API_KEY=...
``` 
4. Run the python app main.py from streamlit
```bash
streamlit run main.py
```
#### Containerization 
* To create a docker container, a Dockerfile is provided. Make sure Docker Desktop is installed, and the OpenAI API key is stored in the .env file, the Dockerfile contains the following: 
```bash
FROM python:3.10-slim
ADD . .
RUN pip install -r requirements.txt 
EXPOSE 8500
ENTRYPOINT ["streamlit","run"] 
CMD ["./GPT.py","--server.headless","true","--server.fileWatcherType","none","--browser.gatherUsageStats","false","--server.port=8500","--server.address=0.0.0.0"]
```
* To build the Docker image from the Dockerfile, run the following command: 
```bash
docker build -t argpt . 
```
* To run a Docker container of the application on port 8500: 
```bash
docker run -p 8500:8500 argpt 
```
* The image is available on Docker Hub via the following link:  
https://hub.docker.com/repository/docker/ahishamm/argpt/general 
```bash
docker pull ahishamm/argpt:latest
```