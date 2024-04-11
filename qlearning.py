import numpy as np
from blackjack import BlackjackGame

class BlackjackQLearning:
    """
    A Q-Learning agent for playing Blackjack.
    
    Attributes:
        alpha (float): Learning rate.
        gamma (float): Discount factor for future rewards.
        epsilon (float): Probability of choosing a random action to ensure exploration.
        Q (numpy.ndarray): The Q-table for storing state-action values.
    """
    
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Initializes the Q-Learning agent with specified parameters and an empty Q-table.
        
        Parameters:
            alpha (float): Learning rate.
            gamma (float): Discount factor for future rewards.
            epsilon (float): Exploration rate.
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # Initialize Q-table: dimensions for player sum (0-32), dealer card (1-11), usable ace (0, 1), and actions (hit=0, stay=1)
        self.Q = np.zeros((33, 12, 2, 2))

    def choose_action(self, player_sum, dealer_card, usable_ace):
        """
        Chooses an action (hit or stay) based on the current state and the Q-table.
        
        Parameters:
            player_sum (int): The total value of the player's hand.
            dealer_card (int): The value of the dealer's visible card.
            usable_ace (int): Whether the player has a usable ace (0 or 1).
            
        Returns:
            str: The chosen action ('hit' or 'stay').
        """
        # Explore: choose a random action
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(["hit", "stay"])
        # Exploit: choose the best action based on the current Q-table
        else:
            return "hit" if self.Q[player_sum, dealer_card, usable_ace, 0] > self.Q[player_sum, dealer_card, usable_ace, 1] else "stay"

    def update(self, player_sum, dealer_card, usable_ace, action, reward, new_player_sum, new_dealer_card, new_usable_ace):
        """
        Updates the Q-table based on the agent's experience.
        
        Parameters:
            player_sum (int): The total value of the player's hand before taking the action.
            dealer_card (int): The value of the dealer's visible card.
            usable_ace (int): Whether the player had a usable ace before taking the action.
            action (str): The action taken ('hit' or 'stay').
            reward (int): The reward received after taking the action.
            new_player_sum (int): The total value of the player's hand after taking the action.
            new_dealer_card (int): The value of the dealer's visible card after taking the action.
            new_usable_ace (int): Whether the player has a usable ace after taking the action.
        """
        action_idx = 0 if action == "hit" else 1
        old_value = self.Q[player_sum, dealer_card, usable_ace, action_idx]
        future_max = np.max(self.Q[new_player_sum, new_dealer_card, new_usable_ace])
        self.Q[player_sum, dealer_card, usable_ace, action_idx] = old_value + self.alpha * (reward + self.gamma * future_max - old_value)

    @staticmethod
    def has_usable_ace(hand):
        """
        Checks if the hand has a usable ace (an ace that can be valued as 11 without busting the hand).
        
        Parameters:
            hand (list): A list of cards in the hand.
            
        Returns:
            int: 1 if there is a usable ace, otherwise 0.
        """
        value, ace = 0, False
        for card in hand:
            card_number = card['number']
            value += min(10, int(card_number) if card_number not in ['J', 'Q', 'K', 'A'] else 11)
            ace |= (card_number == 'A')
        return int(ace and value + 10 <= 21)

    def train(self, episodes):
        """
        Trains the Q-Learning agent on a specified number of Blackjack games.
        
        Parameters:
            episodes (int): The number of games to play for training.
        """
        one_percent = round(episodes / 100)

        for ep in range(episodes):
            game = BlackjackGame()
            game.start_game()

            if ep % one_percent == 0:
                progress = (ep/episodes) * 100
                print(f"Training progress: {progress:.2f}%")

            # Main training loop
            # Convert dealer card to numerical value
            dealer_card = int(game.dealer_hand[0]['number']) if game.dealer_hand[0]['number'] not in ['J', 'Q', 'K', 'A'] else (10 if game.dealer_hand[0]['number'] != 'A' else 11)
            status = "continue"

            while status == "continue":
                player_sum = game.hand_value(game.player_hand)
                usable_ace = self.has_usable_ace(game.player_hand)
                action = self.choose_action(player_sum, dealer_card, usable_ace)
                status = game.player_action(action)
                new_player_sum = game.hand_value(game.player_hand)
                new_usable_ace = self.has_usable_ace(game.player_hand)

                reward = 0  # Intermediate rewards are not considered; focus on final outcome

                # Update rewards for special cases: blackjack or bust
                if status == "player_blackjack":
                    reward = 1
                elif status == "player_bust":
                    reward = -1

                # Update the Q-table
                if reward != 0:
                    self.update(player_sum, dealer_card, usable_ace, action, reward, new_player_sum, dealer_card, new_usable_ace)

                if action == "stay":
                    break

            # Final game outcome and reward
            final_result = game.game_result()
            final_reward = 1 if final_result == "win" else (-1 if final_result == "loss" else 0)
            self.update(player_sum, dealer_card, usable_ace, action, final_reward, new_player_sum, dealer_card, new_usable_ace)

    def play(self):
        """
        Plays a game of Blackjack using the trained Q-table to make decisions.
        
        Returns:
            str: The final result of the game ('win', 'loss', or 'draw').
        """
        game = BlackjackGame()
        game.start_game()

        print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))

        status = "continue"
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        while status == "continue":
            player_sum = game.hand_value(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = int(game.dealer_hand[0]['number']) if game.dealer_hand[0]['number'] not in ['J', 'Q', 'K', 'A'] else (10 if game.dealer_hand[0]['number'] != 'A' else 11)
            action = self.choose_action(player_sum, dealer_card, usable_ace)  # Decision based on Q-table
            status = game.player_action(action)
            
            if action == "stay":
                break
                
            print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        
        # Final game outcome
        if status == "continue":
            print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
            game.dealer_action(output=True)

        final_result = game.game_result()
        return final_result
