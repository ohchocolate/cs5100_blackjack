import random

class BlackjackGame:
    """
    A simple implementation of the card game Blackjack. 
    This class handles the creation of a deck, dealing cards, 
    and calculating the outcome of the game between a player and a dealer.
    """

    # Unicode representations for card suits
    heart = "\u2665"
    spade = "\u2660"
    diamond = "\u2666"
    club = "\u2663"

    # Mapping card suit names to their unicode symbols
    suits = {
        "diamonds": diamond,
        "hearts": heart,
        "spades": spade,
        "clubs": club
    }

    def __init__(self):
        """
        Initializes the game by generating a shuffled deck,
        and setting up empty hands for both the player and the dealer.
        """
        self.deck = self.generate_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []

    @staticmethod
    def generate_deck():
        """
        Generates a standard deck of 52 playing cards.
        
        Returns:
            list: A deck of cards, where each card is represented by a dictionary
                  with 'number' and 'suit' keys.
        """
        numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        deck = [{'number': number, 'suit': suit} for number in numbers for suit in suits]
        return deck

    def deal_card(self):
        """
        Deals (removes and returns) the top card from the deck.
        
        Returns:
            dict: The card dealt from the top of the deck.
        """
        return self.deck.pop()

    def start_game(self):
        """
        Starts a new game by dealing two cards each to the player and the dealer.
        """
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

    @staticmethod
    def hand_value(hand):
        """
        Calculates the value of a hand of cards.
        
        Parameters:
            hand (list): The hand to calculate the value for.
        
        Returns:
            int: The total value of the hand.
        """
        value = 0
        aces = 0
        for card in hand:
            if card['number'] in ['J', 'Q', 'K']:
                value += 10
            elif card['number'] == 'A':
                value += 11
                aces += 1
            else:
                value += int(card['number'])

        # Adjust for aces value
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def player_action(self, action):
        """
        Processes the player's action ('hit' or 'stay').
        
        Parameters:
            action (str): The player's chosen action.
            
        Returns:
            str: The current game status after performing the action.
        """
        if action == "hit":
            self.player_hand.append(self.deal_card())
        return self.game_status()

    def dealer_action(self, output=False):
        """
        Performs the dealer's actions according to Blackjack rules.
        
        Parameters:
            output (bool): If True, prints the dealer's hand after each hit.
        """
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
            if output:
                print("Dealer hits and has:", self.format_cards(self.dealer_hand), self.hand_value(self.dealer_hand))

    def game_status(self):
        """
        Determines the current status of the game based on the player's hand value.
        
        Returns:
            str: The current status of the game ('player_bust', 'player_blackjack', or 'continue').
        """
        player_value = self.hand_value(self.player_hand)
        if player_value > 21:
            return "player_bust"
        elif player_value == 21:
            return "player_blackjack"
        else:
            return "continue"

    def game_result(self):
        """
        Determines the final result of the game after the dealer has finished their actions.
        
        Returns:
            str: The result of the game ('win', 'loss', or 'draw').
        """
        self.dealer_action()
        player_value = self.hand_value(self.player_hand)
        dealer_value = self.hand_value(self.dealer_hand)

        if player_value > 21:
            return "loss"
        elif dealer_value > 21 or player_value > dealer_value:
            return "win"
        elif player_value == dealer_value:
            return "draw"
        else:
            return "loss"
    
    @staticmethod
    def format_cards(cards):
        """
        Formats a list of cards into a string for display.
        
        Parameters:
            cards (list): The cards to format.
        
        Returns:
            str: A string representation of the cards.
        """
        result = ""
        for card in cards:
            suit = BlackjackGame.suits[card["suit"]]
            result += f"{card['number']}{suit} "
        
        return result.strip()

def main():
    """
    Main function to run a simple interactive Blackjack game.
    Allows the player to 'hit' or 'stay' and shows the game result.
    """
    game = BlackjackGame()
    game.start_game()
    print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))

    status = "continue"
    while status == "continue":
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        action = input("Enter an action (hit/stay): ")
        status = game.player_action(action)
        
        if action == "stay" or status != "continue":
            break

    if status == "continue":
        print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
        game.dealer_action(output=True)

    final_result = game.game_result()
    print(f"Game result: {final_result}")

if __name__ == "__main__":
    main()
