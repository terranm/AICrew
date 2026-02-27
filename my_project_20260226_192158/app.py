from flask import Flask, render_template, url_for, send_from_directory, request
import time

app = Flask(__name__)

# 게임 데이터를 정의합니다.
cards = [
    {
        'name': '백설공주',
        'description': '사과를 사용하여 적을 약화시킵니다.',
        'image': 'snow_white.png'
    },
    {
        'name': '신데렐라',
        'description': '유리 구두로 아군을 강화합니다.',
        'image': 'cinderella.png'
    },
    {
        'name': '빨간망토',
        'description': '늑대를 물리치고 강력한 공격을 합니다.',
        'image': 'red_riding_hood.png'
    }
]

# 더블 클릭 방지 및 로딩 상태 관리를 위한 변수
loading = False

@app.route('/')
def index():
    return render_template('index.html', cards=cards, loading=loading)

@app.route('/start_game', methods=['POST'])
def start_game():
    global loading
    if not loading:
        loading = True
        print("게임 시작 버튼 클릭됨")
        # time.sleep(2)  # 오래 걸리는 작업 시뮬레이션 (에셋 로딩 등)
        loading = False  # 로딩 완료 후 상태 변경
        return render_template('index.html', cards=cards, loading=loading)
    else:
        return 'Loading... Please wait.'

# 이미지 파일 제공을 위한 route
@app.route('/<path:filename>')
def get_file(filename):
    return send_from_directory('.', filename)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

if __name__ == '__main__':
    app.run(debug=True)