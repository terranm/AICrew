
import battle
import deck
import game_logic
import stage
import user
import ui
import character
import monster
import card

class Main:
    def __init__(self):
        self.user = user.User()
        self.deck = deck.Deck()
        self.deck.add_card(card.Card("�⺻ ����", 10, 0))
        self.deck.add_card(card.Card("�⺻ ���", 0, 5))
        self.stage = stage.Stage()
        self.battle = battle.Battle(self.user, self.deck, self.stage)
        self.game_logic = game_logic.GameLogic()
        self.ui = ui.UI()

    def run(self):
        while True:
            self.ui.display_main_menu()
            choice = self.ui.get_user_input("�޴��� �����ϼ���: ")

            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.view_deck()
            elif choice == "3":
                self.exit_game()
            else:
                self.ui.display_message("�߸��� �����Դϴ�.")

    def start_game(self):
        self.ui.display_message("������ �����մϴ�!")
        self.stage.load_stage(1)  # �������� 1�� �ε��մϴ�.
        result = self.battle.start_battle()
        if result == "win":
            self.ui.display_message("�¸�!")
        else:
            self.ui.display_message("�й�!")

    def view_deck(self):
        self.ui.display_message("���� Ȯ���մϴ�.")
        self.deck.display_deck()

    def exit_game(self):
        self.ui.display_message("������ �����մϴ�.")
        exit()


if __name__ == "__main__":
    main = Main()
    main.run()
