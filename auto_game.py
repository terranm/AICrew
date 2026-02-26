import random


class NumberGuessingGame:
    """
    1부터 100 사이의 숫자를 맞추는 게임 클래스
    """

    def __init__(self):
        """
        게임 초기화:
        - 컴퓨터가 1부터 100 사이의 임의의 숫자를 선택
        - 시도 횟수 초기화
        - 게임 종료 상태 초기화
        """
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False

    def start_game(self):
        """
        게임 시작 메시지를 출력하고, 게임 상태를 초기화한 뒤 본 게임을 시작합니다.
        """
        print("1부터 100 사이의 숫자를 맞춰보세요.")
        self.attempts = 0
        self.game_over = False
        self.play_game()

    def get_user_guess(self):
        """
        사용자로부터 숫자를 입력받고, 유효한 값인지 검사합니다.
        잘못된 입력(숫자가 아님, 범위 밖)은 다시 입력을 요구합니다.
        """
        while True:
            try:
                guess = input("숫자를 입력하세요: ")
                guess = int(guess)
                if 1 <= guess <= 100:
                    return guess
                else:
                    print("1부터 100 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("유효하지 않은 입력입니다. 숫자를 입력해주세요.")

    def check_guess(self, guess: int) -> bool:
        """
        사용자의 추측값을 정답과 비교하고, 힌트를 제공합니다.
        정답이면 시도 횟수를 포함한 메시지를 출력하고 게임을 종료합니다.
        """
        self.attempts += 1
        if guess == self.secret_number:
            print(f"정답입니다! {self.attempts}번 만에 맞추셨습니다.")
            self.game_over = True
            return True
        elif guess > self.secret_number:
            print("다운")
        else:
            print("업")
        return False

    def play_game(self):
        """
        게임이 끝날 때까지(정답을 맞출 때까지) 반복해서 숫자를 입력받고 검사합니다.
        """
        while not self.game_over:
            guess = self.get_user_guess()
            if self.check_guess(guess):
                self.end_game()

    def end_game(self):
        """
        게임 종료 후 다시 플레이할지 여부를 묻고, 원하면 새 게임을 시작합니다.
        """
        play_again = input("다시 플레이하시겠습니까? (y/n): ")
        if play_again.lower() == "y":
            self.__init__()
            self.start_game()
        else:
            print("게임을 종료합니다.")


if __name__ == "__main__":
    game = NumberGuessingGame()
    game.start_game()

