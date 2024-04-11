from blackjack import BlackjackGame
from qlearning import BlackjackQLearning
from montecarlo import MonteCarloWithExploringStarts


def main():
    # Train the agent with MonteCarlo
    agent = MonteCarloWithExploringStarts()  # 初始化蒙特卡洛代理
    episodes = 500000  # 训练轮数
    agent.train(episodes)

    # Test the agent's performance
    test_games = 100000
    mc_wins = 0
    mc_losses = 0
    mc_draws = 0

    for _ in range(test_games):
        result = agent.play()
        if result == "win":
            mc_wins += 1
        elif result == "loss":
            mc_losses += 1
        else:
            mc_draws += 1

    print(f"Wins: {mc_wins}, Losses: {mc_losses}, Draws: {mc_draws}")
    mc_win_rate = (mc_wins / test_games) * 100
    print(f"Win rate: {mc_win_rate:.2f}%")

    # Train the agent with q learning
    agent = BlackjackQLearning()  # 初始化蒙特卡洛代理
    agent.train(episodes)

    # Test the agent's performance
    ql_wins = 0
    ql_losses = 0
    ql_draws = 0

    for _ in range(test_games):
        result = agent.play()
        if result == "win":
            ql_wins += 1
        elif result == "loss":
            ql_losses += 1
        else:
            ql_draws += 1

    print(f"Wins: {ql_wins}, Losses: {ql_losses}, Draws: {ql_draws}")
    ql_win_rate = (ql_wins / test_games) * 100
    print(f"Win rate: {ql_win_rate:.2f}%")
    print(f"Monte Carlo Agent win rate: {mc_win_rate:.2f}%, "
          f"Q Learning Agent win rate: {ql_win_rate:.2f}%")


if __name__ == "__main__":
    main()
