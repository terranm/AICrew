import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew
from crewai_tools import FileWriterTool

# 1. API 키 및 두뇌 세팅
load_dotenv() 
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# 2. 아이디어 입력받기
print("==================================================")
print("🤖 AI 개발 팀이 대기 중입니다!")
my_idea = input("💡 만들고 싶은 프로그램 아이디어를 자유롭게 적어주세요:\n👉 ")
print("==================================================")

# 3. 프로젝트 폴더 자동 생성
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
project_folder = f"my_project_{current_time}"
os.makedirs(project_folder, exist_ok=True) 

# 4. 파일 쓰기 도구 (경로 제한을 풀고 프롬프트로 제어합니다)
file_writer_tool = FileWriterTool()

# 5. 에이전트 생성 (족쇄 채우기)
planner = Agent(
    role="시스템 아키텍트",
    goal="아이디어를 바탕으로 완벽한 기획서 및 파일 구조 설계",
    backstory=f"너는 소프트웨어 아키텍트야. 모든 코드는 반드시 '{project_folder}' 폴더 안에만 존재해야 해. [🚨절대 주의] 게임을 실행하는 메인 파일의 이름은 절대 'main.py'로 짓지 마! 기존 시스템과 충돌하니까 무조건 'game_app.py'라는 이름으로 설계해.",
    llm=gemini_llm,
    verbose=True
)

developer = Agent(
    role="파이썬 수석 개발자",
    goal="기획서를 바탕으로 코드를 작성하고 도구를 사용해 실제 파일로 저장",
    backstory=f"너는 코드를 물리적 파일로 저장하는 개발자야. [🚨절대 규칙] FileWriterTool을 사용할 때 `filename` 속성에는 무조건 '{project_folder}/파일명.py' 형태로 앞에 폴더명을 붙여야 해! 그리고 `overwrite=True` 속성도 무조건 같이 넣어줘야 에러가 안 나!",
    llm=gemini_llm,
    tools=[file_writer_tool],
    verbose=True
)

# 6. 작업(Task) 지시서 작성
plan_task = Task(
    description=f"다음 아이디어를 분석해서 기획서와 필요한 파이썬 파일 목록을 작성해: {my_idea}",
    expected_output="상세 기획서와 필요한 .py 파일들의 목록 (메인 실행 파일 이름은 game_app.py)",
    agent=planner
)

code_task = Task(
    description=f"기획안을 바탕으로 파이썬 코드를 작성하고, 제공된 도구를 사용해 파일을 생성해. 도구 사용 예시: filename='{project_folder}/game_app.py', overwrite=True. 모든 파일 생성이 끝나면 완료를 보고해.",
    expected_output="모든 파일 생성이 완료되었다는 메시지와 게임 실행 방법",
    agent=developer
)

# 7. AI 팀(Crew) 결성 및 시작
my_crew = Crew(
    agents=[planner, developer],
    tasks=[plan_task, code_task],
    verbose=True
)

print(f"\n🚀 기획자와 개발자가 작업을 시작합니다! (모든 파일은 '{project_folder}' 폴더에 저장됩니다...)")
result = my_crew.kickoff()

print("\n==================================================")
print(f"✅ 최종 결과물 완료! 좌측 파일 목록에서 '{project_folder}' 폴더를 열어보세요!")
print("==================================================")