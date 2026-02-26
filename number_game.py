import random


class NumberGuessingGame:
    """
    1부터 100 사이의 숫자를 맞추는 게임 클래스
    """

    def __init__(self):
        """
        게임 초기화:
        - 정답 숫자 생성
        - 시도 횟수 초기화
        """
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.is_game_over = False  # 게임 종료 상태를 나타내는 변수

    def reset_game(self):
        """
        게임을 재시작하는 메서드:
        - 새로운 난수 생성
        - 시도 횟수 초기화
        - 게임 종료 상태 초기화
        """
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.is_game_over = False
        print("게임을 재시작합니다. 새로운 숫자가 생성되었습니다.")

    def get_guess(self):
        """
        사용자로부터 추측 값을 입력받고 유효성을 검사하는 메서드
        :return: 사용자가 입력한 추측 값 (정수)
        """
        while True:
            try:
                guess = int(input("1부터 100 사이의 숫자를 추측해보세요: "))
                if 1 <= guess <= 100:
                    return guess
                else:
                    print("1부터 100 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("유효하지 않은 입력입니다. 숫자를 입력해주세요.")

    def play(self):
        """
        게임 실행 메서드:
        - 사용자 입력을 받고 힌트를 제공하며 정답을 판정
        - 게임 종료 시 결과 표시 및 재시작 옵션 제공
        """
        print("숫자 맞추기 게임을 시작합니다!")

        while not self.is_game_over:
            guess = self.get_guess()

            self.attempts += 1

            if guess < self.secret_number:
                print("업!")
            elif guess > self.secret_number:
                print("다운!")
            else:
                print(f"정답입니다! {self.attempts}번 만에 맞추셨습니다.")
                self.is_game_over = True
                self.play_again()

    def play_again(self):
        """
        게임 종료 후 재시작 여부를 묻고, 재시작하는 메서드
        """
        while True:
            answer = input("다시 플레이하시겠습니까? (y/n): ").lower()
            if answer == "y":
                self.reset_game()
                self.play()
                break
            elif answer == "n":
                print("게임을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. y 또는 n을 입력해주세요.")


if __name__ == "__main__":
    game = NumberGuessingGame()
    game.play()

