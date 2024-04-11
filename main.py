from blackjack import BlackjackGame
from qlearning import BlackjackQLearning
from montecarlo import MonteCarloWithExploringStarts

def main():
    """
    Main function to train and evaluate Monte Carlo and Q-Learning agents
    on a blackjack simulation. It trains each agent for a specified number
    of episodes, then tests them on a set number of games to evaluate
    their performance based on win rate.
    """
    
    # Train the agent with MonteCarlo
    agent = MonteCarloWithExploringStarts()  # Initialize the Monte Carlo agent
    episodes = 500000  # Number of training episodes
    agent.train(episodes)  # Train the agent

    # Test the agent's performance
    test_games = 100000  # Number of games to test the agent
    mc_wins = 0  # Monte Carlo wins
    mc_losses = 0  # Monte Carlo losses
    mc_draws = 0  # Monte Carlo draws

    for _ in range(test_games):  # Test the Monte Carlo agent
        result = agent.play()
        if result == "win":
            mc_wins += 1
        elif result == "loss":
            mc_losses += 1
        else:
            mc_draws += 1

    print(f"Wins: {mc_wins}, Losses: {mc_losses}, Draws: {mc_draws}")
    mc_win_rate = (mc_wins / test_games) * 100  # Calculate win rate
    print(f"Win rate: {mc_win_rate:.2f}%")

    # Train the agent with Q-Learning
    agent = BlackjackQLearning()  # Initialize the Q-Learning agent
    agent.train(episodes)  # Train the agent

    # Test the agent's performance
    ql_wins = 0  # Q-Learning wins
    ql_losses = 0  # Q-Learning losses
    ql_draws = 0  # Q-Learning draws

    for _ in range(test_games):  # Test the Q-Learning agent
        result = agent.play()
        if result == "win":
            ql_wins += 1
        elif result == "loss":
            ql_losses += 1
        else:
            ql_draws += 1

    print(f"Wins: {ql_wins}, Losses: {ql_losses}, Draws: {ql_draws}")
    ql_win_rate = (ql_wins / test_games) * 100  # Calculate win rate
    print(f"Win rate: {ql_win_rate:.2f}%")
    print(f"Monte Carlo Agent win rate: {mc_win_rate:.2f}%, "
          f"Q Learning Agent win rate: {ql_win_rate:.2f}%")

if __name__ == "__main__":
    main()
