import os
import random
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from PIL import Image, ImageDraw # 👈 이미지를 그리기 위한 도구

# 1. API 키 및 두뇌 세팅
load_dotenv()
# gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
#gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
gemini_llm = LLM(
    model="gemini/gemini-1.5-pro-002", # 👈 'gemini/'를 앞에 꼭 붙여주세요!
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7
)
os.environ["OTEL_SDK_DISABLED"] = "true"

# 2. 프로젝트 폴더 생성
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
project_folder = f"my_project_{current_time}"
os.makedirs(project_folder, exist_ok=True)
static_img_folder = os.path.join(project_folder, "static", "images") # 이미지가 저장될 폴더 미리 생성
os.makedirs(static_img_folder, exist_ok=True)


# ---------------------------------------------------------
# 3. 💡 [신규] 금손 '이미지 생성 도구' 만들기
# ---------------------------------------------------------
@tool("Image Generator Tool")
def image_gen_tool(prompt: str, filename: str) -> str:
    """
    설명(prompt)을 입력받아 어울리는 색상의 간단한 placeholder 이미지를 생성하고 저장합니다.
    생성된 이미지는 'static/images/' 폴더에 저장됩니다.
    """
    # 1. 프롬프트 내용에 따라 랜덤한 파스텔톤 색상을 만듭니다. (실제 AI 이미지 생성 대신 간단히 구현)
    random.seed(prompt) # 프롬프트가 같으면 항상 같은 색이 나오도록 고정
    r = random.randint(150, 255)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    color = (r, g, b)

    # 2. 300x300 크기의 단색 이미지를 생성합니다.
    img = Image.new('RGB', (300, 300), color)
    draw = ImageDraw.Draw(img)
    # 이미지 중앙에 프롬프트 텍스트를 살짝 적어줍니다.
    draw.text((10, 140), f"Image for:\n{prompt[:20]}...", fill=(50, 50, 50))

    # 3. 안전한 경로에 파일을 저장합니다.
    safe_filename = os.path.basename(filename) # 경로 조작 방지
    if not safe_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
         safe_filename += ".png" # 확장자 자동 추가

    file_path = os.path.join(static_img_folder, safe_filename)
    img.save(file_path)

    # 4. HTML에서 사용할 수 있는 웹 경로를 반환합니다.
    web_path = f"static/images/{safe_filename}"
    return f"이미지 생성이 완료되었습니다! 웹 경로: '{web_path}' (실제 파일 위치: {file_path})"


# 4. 기존 '파일 저장 도구' (유지)
@tool("File Writer Tool")
def write_file_tool(filename: str, content: str) -> str:
    """완성된 코드를 실제 파일로 저장합니다. 파일명(filename)과 코드 내용(content)을 입력하세요."""
    file_path = os.path.abspath(os.path.join(project_folder, filename))
    if not file_path.startswith(os.path.abspath(project_folder)):
        return "Error: 프로젝트 폴더 외부로는 파일을 생성할 수 없습니다."
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"[{filename}] 파일이 성공적으로 생성/수정되었습니다!"


# ---------------------------------------------------------
# 5. 에이전트 팀 결성 (디자이너 영입!)
# ---------------------------------------------------------
planner = Agent(
    role="시스템 아키텍트",
    goal="요구사항을 분석하여 최적의 파일 구조, 기획안, 디자인 컨셉을 도출",
    backstory=f"너는 베테랑 아키텍트야. 개발자와 디자이너가 모두 이해할 수 있는 상세한 설계도를 그려야 해. 모든 코드는 '{project_folder}' 안에 위치한다.",
    llm=gemini_llm,
    verbose=True
)

# 🌟 [NEW] 디자이너 에이전트 추가
designer = Agent(
    role="UI/UX 수석 디자이너",
    goal="기획안을 바탕으로 아름다운 웹 페이지 레이아웃(HTML/CSS)을 설계하고 필요한 이미지 에셋을 생성",
    backstory="너는 미적 감각이 뛰어난 디자이너야. 'Image Generator Tool'로 필요한 아이콘이나 배경 이미지를 직접 만들고, 그걸 활용해서 'File Writer Tool'로 예쁜 HTML/CSS 파일을 완성해.",
    llm=gemini_llm,
    tools=[image_gen_tool, write_file_tool], # 👈 두 가지 도구를 모두 사용!
    verbose=True
)

developer = Agent(
    role="풀스택 웹게임 개발자",
    goal="고수준의 기술 스택을 사용하여 실제 서비스 가능한 퀄리티의 게임 구현",
    backstory="""너는 현대적인 웹 기술 전문가야. 
    1. 화면은 반드시 'Tailwind CSS'를 써서 세련되게 만들 것.
    2. 카드 움직임이나 효과는 'GSAP' 라이브러리를 써서 애니메이션을 넣을 것.
    3. 모든 데이터 로직은 'Flask'와 'SQLite'를 연동해서 서버가 꺼져도 저장되게 할 것.""",
    llm=gemini_llm, # 여기서 model="gemini-1.5-pro"로 바꿨는지 꼭 확인!
    tools=[write_file_tool],
    verbose=True
    # role="파이썬 수석 개발자",
    # goal="기획안과 디자인을 바탕으로 실제 작동하는 백엔드 로직(Python)을 작성하고 연결",
    # backstory="너는 코드를 짜는 개발자야. 디자이너가 만든 멋진 HTML에 생명을 불어넣는 Python 로직을 작성하고 'File Writer Tool'로 저장해.",
    # llm=gemini_llm,
    # tools=[write_file_tool],
    # verbose=True
)


# ---------------------------------------------------------
# 6. 무한 루프 시작: "기획 -> 디자인 -> 개발" 프로세스
# ---------------------------------------------------------
is_first_run = True

while True:
    if is_first_run:
        print(f"\n{'='*60}")
        print("🎨🤖 AI 개발+디자인 팀이 준비되었습니다! (폴더: {})".format(project_folder))
        print(f"{'='*60}")
        user_input = input("💡 만들고 싶은 프로그램을 디자인 요소와 함께 말해주세요 (종료: exit):\n👉 ")
        is_first_run = False
    else:
        print(f"\n{'='*60}")
        print("✅ 작업 완료! 추가로 수정하거나 업그레이드할 내용이 있나요?")
        print(f"{'='*60}")
        user_input = input("💡 추가 지시사항을 입력하세요 (예: 배경을 숲 속 이미지로 바꿔줘) (종료: exit):\n👉 ")

    if user_input.lower() == 'exit':
        print("👋 AI 팀이 업무를 종료합니다. 멋진 결과물이 나왔기를 바랍니다!")
        break

    # 1단계: 기획 (설계 및 디자인 컨셉 도출)
    plan_task = Task(
        description=f"사용자의 요구사항('{user_input}')을 분석해서 필요한 파일 목록, 기능 명세, 그리고 **디자인 컨셉(색상 팔레트, 필요한 이미지 종류)**을 상세히 기획해.",
        expected_output="상세 기획서와 디자인 지침이 포함된 파일 목록",
        agent=planner
    )

    # 2단계: 디자인 (이미지 생성 및 HTML/CSS 작성)
    design_task = Task(
        description=f"기획안을 바탕으로 웹 페이지의 아름다운 레이아웃(HTML/CSS)을 코딩해. 필요한 경우 **'Image Generator Tool'을 사용해서 로고, 아이콘, 배경 이미지 등을 직접 생성**하고 HTML에 포함시켜. 모든 디자인 파일은 'File Writer Tool'로 저장해.",
        expected_output="이미지 에셋이 포함된 완성도 높은 HTML/CSS 파일 저장 완료 보고",
        agent=designer,
        context=[plan_task] # 기획자의 결과물을 참고
    )

    # 3단계: 개발 (백엔드 로직 연결)
    code_task = Task(
        description=f"디자이너가 만든 HTML 파일에 실제 기능이 작동하도록 파이썬 백엔드 로직(Flask 등)을 작성하고 연결해. 완성된 코드는 'File Writer Tool'로 저장해.",
        expected_output="작동하는 백엔드 코드 저장 완료 및 실행 방법 보고",
        agent=developer,
        context=[plan_task, design_task] # 기획서와 디자인 결과물을 모두 참고
    )

    # 크루 실행 (순차적으로 작업 진행)
    my_crew = Crew(
        agents=[planner, designer, developer],
        tasks=[plan_task, design_task, code_task],
        verbose=True
    )

    print(f"\n🚀 AI 크루가 디자인을 포함한 '{user_input}' 작업을 시작합니다...")
    my_crew.kickoff()

    print(f"\n✨ 결과물은 '{project_folder}' 폴더에서 확인하세요! (웹 서버를 실행해보세요)")