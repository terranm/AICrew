# 설치: pip install crewai langchain-google-genai
import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# 제미나이 설정 (Gemini 2.0 Flash 추천)
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyCC89-Ei5pQtbL5YYGlC9pCYOCBg9eom0Y"
)