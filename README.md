# Blackjack Reinforcement Learning
This project applies Reinforcement Learning (RL) techniques, specifically Monte Carlo methods and Q-Learning, to develop agents capable of playing Blackjack. These agents are trained and evaluated against a simulated Blackjack environment to learn optimal strategies.

## Project Structure
blackjack.py: Contains the BlackjackGame class that simulates a simple version of the Blackjack game environment. It includes methods for dealing cards, calculating hand values, and determining game outcomes.

montecarlo.py: Implements the MonteCarloWithExploringStarts class, representing an agent that uses the Monte Carlo method with exploring starts for learning the game strategy.

qlearning.py: Defines the BlackjackQLearning class, which uses the Q-Learning algorithm to learn an optimal policy for playing Blackjack.

main.py: The main script used to train both the Monte Carlo and Q-Learning agents, evaluate their performance, and compare their win rates.

## Algorithms Introduction
### Monte Carlo Method
The Monte Carlo method for reinforcement learning uses experience from playing the game to estimate the value of state-action pairs. It involves playing episodes of the game, at the end of which rewards are observed and used to update the value estimates. One key aspect of this method is the use of exploring starts to ensure that all actions are explored sufficiently.

### Q-Learning
Q-Learning is an off-policy temporal difference learning algorithm that seeks to find the best action to take given the current state. It directly learns the value of taking an action in a state, without requiring a model of the environment. The learning process updates estimates of the Q-values based on the equation Q(s,a) = Q(s,a) + α(R + γ maxQ(s',a') - Q(s,a)), where R is the reward received, s' is the next state, and a' is the next action.

## Training Methods
Both agents were trained over 500,000 episodes of Blackjack, with their policies updated based on the outcomes and rewards of each episode. The Monte Carlo agent used exploring starts to ensure every state-action pair is explored. The Q-Learning agent used an epsilon-greedy policy for exploration, with epsilon set to 0.1.

Monte Carlo Training: Episodes were generated using the policy derived from the Q-values, with the policy updated after each episode to reflect the learned values.

Q-Learning Training: The agent chose actions either randomly (with probability ε) or by following the current best estimate of the Q-table. After each action, the Q-table was updated based on the received reward and the maximum future value estimate.

Results
After training, both agents were evaluated over 100,000 games of Blackjack. The performance metrics considered were the win rates of the agents.

Monte Carlo Agent: Showed a win rate of approximately XX%, with draws and losses accounting for the remaining outcomes.

Q-Learning Agent: Achieved a win rate of approximately YY%, demonstrating the effectiveness of Q-Learning in optimizing the decision-making process.

These results indicate the potential of reinforcement learning techniques in mastering complex strategies required for games like Blackjack. Future work could involve tuning the parameters further or exploring more sophisticated RL algorithms.