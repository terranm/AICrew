import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew

# 1. 내가 발급받은 제미나이 열쇠(API Key)를 입력하는 곳입니다.
# 아까 복사해둔 API 키를 아래 큰따옴표 안에 붙여넣으세요.
os.environ["GEMINI_API_KEY"] = "AIzaSyC1UqJuaqKEmIP50oU8GNT3wlQgrsyHZXw"

# 2. 어떤 두뇌를 쓸지 결정합니다. (가장 빠르고 가성비 좋은 제미나이 2.0 Flash 모델 사용)
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
# 2. 기획자 AI 만들기
planner = Agent(
    role="서비스 기획자",
    goal="사용자의 아이디어를 바탕으로 완벽한 기획서 작성",
    backstory="너는 실리콘밸리 10년 차 기획자야. 개발자가 바로 코딩할 수 있도록 마크다운 형식으로 논리적이고 깔끔하게 기획서를 작성해.",
    llm=gemini_llm,
    verbose=True,
    max_rpm=3  # 👈 [추가된 부분] 1분에 최대 10번만 질문하도록 속도를 늦춥니다.
)

# 3. 개발자 AI 만들기
developer = Agent(
    role="파이썬 개발자",
    goal="기획서를 바탕으로 에러 없이 실행 가능한 파이썬 코드 작성",
    backstory="너는 꼼꼼한 성격을 가진 천재 파이썬 개발자야. 기획서의 내용을 하나도 빠짐없이 실제 파이썬 코드로 구현해내.",
    llm=gemini_llm,
    verbose=True,
    max_rpm=3  # 👈 [추가된 부분] 개발자도 천천히 일하도록 제한합니다.
)

# 4. 우리가 만들고 싶은 것 (아이디어만 던져주면 됩니다!)
my_idea = "컴퓨터가 1부터 100까지 숫자 중 하나를 무작위로 생각하고, 내가 숫자를 입력하면 '업'인지 '다운'인지 알려주어 정답을 맞추는 게임을 만들어줘."

# 5. 작업(Task) 지시서 작성
plan_task = Task(
    description=f"다음 아이디어를 분석해서 상세한 기능 요구사항 기획서를 작성해: {my_idea}",
    expected_output="마크다운 형식의 상세 기획서",
    agent=planner
)

code_task = Task(
    description="기획자가 작성한 기획서를 바탕으로 완벽하게 동작하는 파이썬 코드를 작성해. 코드 블록 안에 주석을 꼼꼼히 달아줘.",
    expected_output="실행 가능한 파이썬 코드",
    agent=developer
)

# 6. AI 팀(Crew) 결성 및 업무 시작!
my_crew = Crew(
    agents=[planner, developer],
    tasks=[plan_task, code_task],
    verbose=True  # AI들이 서로 협력하며 일하는 과정을 터미널에 실시간으로 중계합니다.
)

print("기획자와 개발자 AI가 작업을 시작합니다! (터미널 창을 지켜보세요...)")
result = my_crew.kickoff()

print("\n==============================================")
print("최종 결과물:")
print(result)