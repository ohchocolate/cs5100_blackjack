import random
from collections import defaultdict
from blackjack import BlackjackGame


class MonteCarloWithExploringStarts:
    def __init__(self):
        # 初始化状态-动作值函数和返回值列表
        self.Q = defaultdict(lambda: defaultdict(float))
        self.returns = defaultdict(list)
        # 策略初始化为None，将在训练中更新
        self.policy = defaultdict(lambda: None)

    def generate_episode(self, game):
        episode = []
        game.start_game()
        state = (game.hand_value(game.player_hand), game.dealer_hand[0]['number'], 'A' in [card['number'] for card in game.player_hand])
        action = random.choice(["hit", "stay"])
        episode.append((state, action))
        while game.game_status() == "continue":
            if action == "hit":
                game.player_action("hit")
            else:
                break
            state = (game.hand_value(game.player_hand), game.dealer_hand[0]['number'], 'A' in [card['number'] for card in game.player_hand])
            if self.policy[state] is not None:
                action = self.policy[state]
            episode.append((state, action))
        return episode, game.game_result()

    @staticmethod
    def has_usable_ace(hand):
        """Check if the hand has a usable ace."""
        value, ace = 0, False
        for card in hand:
            card_number = card['number']
            value += min(10, int(card_number) if card_number not in ['J', 'Q', 'K', 'A'] else 11)
            ace |= (card_number == 'A')
        return int(ace and value + 10 <= 21)

    def train(self, episodes):
        one_percent = round(episodes / 100)
        for ep in range(episodes):
            game = BlackjackGame()
            game.start_game()
            if ep % one_percent == 0:
                progress = (ep/episodes) * 100
                print(f"Training progress: {progress:.2f}%")
            episode, result = self.generate_episode(game)
            G = 1 if result == "win" else -1
            for state, action in episode:
                self.returns[(state, action)].append(G)
                self.Q[state][action] = sum(self.returns[(state, action)]) / len(self.returns[(state, action)])
                # 策略更新为使Q值最大化的动作
                self.policy[state] = max(self.Q[state], key=self.Q[state].get)

    def print_policy(self):
        for state, action in self.policy.items():
            print(f"State: {state}, Action: {action}")

    def play(self):
        game = BlackjackGame()
        game.start_game()

        print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))

        status = "continue"
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        while status == "continue":
            player_sum = game.hand_value(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = game.dealer_hand[0]['number']
            if dealer_card in ['J', 'Q', 'K']:
                dealer_card = 10
            elif dealer_card == 'A':
                dealer_card = 11
            else:
                dealer_card = int(dealer_card)

            # 获取当前状态的动作价值
            hit_value = self.Q.get((player_sum, dealer_card, int(usable_ace), 0), 0.0)
            stay_value = self.Q.get((player_sum, dealer_card, int(usable_ace), 1), 0.0)

            # 选择价值更高的动作
            action = "hit" if hit_value > stay_value else "stay"
            status = game.player_action(action)

            if action == "stay" or status != "continue":
                break

            print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))

        if status == "continue":
            print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
            game.dealer_action(output=True)

        final_result = game.game_result()
        print(f"Game result: {final_result}")
        return final_result

