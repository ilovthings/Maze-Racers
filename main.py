
import random
import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils.env_checker import check_env
import numpy as np
import math 

#/////MAZE GENERATOR PART OF THE CODE/////
def remove_wall(CuCe, neig):
    if CuCe["position"][0] > neig["position"][0]:
        CuCe['walls'].update({'left': False})
        neig['walls'].update({'right': False})
    elif CuCe["position"][0] < neig["position"][0]:
        CuCe['walls'].update({'right': False})
        neig['walls'].update({'left': False})
    elif CuCe["position"][1] > neig["position"][1]:
        CuCe['walls'].update({'top': False})
        neig['walls'].update({'bottom': False})
    elif CuCe["position"][1] < neig["position"][1]:
        CuCe['walls'].update({'bottom': False})
        neig['walls'].update({'top': False})


def neighbors():#    X Axis↴             Y Axis↴
    positions = [[0, 1, 2, 3, 4,] , [0, 1, 2, 3, 4,] ] # index positions in X and Y
    path = [] # The path the algorithm have taken
    visitedPositons = [] 
    abPositions = [] # Abalible postions (abalible neighbors)
    X = random.choice(positions[0]) #random start point
    Y = random.choice(positions[1]) #random start point
    visitedPositons.append({"position": [X, Y], "walls": {"top": True, "bottom": True, "left": True, "right": True}})
    path.append([X, Y])
    while True:
        if(len(path) == 0): # End function
            return visitedPositons
        if (path[-1][0] in positions[0]) == True and (path[-1][1] in positions[1]) == True: #Check if the coordinates are correct 
            if (path[-1][0]-1 in positions[0]) == True: #Check if there is a neighbor to the of LEFT the current cell
                abPositions.append([path[-1][0]-1,path[-1][1]])
            
            if (path[-1][0]+1 in positions[0]) == True: #Check if there is a neighbor to the RIGHT of the current cell
                abPositions.append([path[-1][0]+1,path[-1][1]])
            
            if (path[-1][1]-1 in positions[1]) == True: #Check if there is a neighbor in TOP of the current cell
                abPositions.append([path[-1][0],path[-1][1]-1])
            
            if (path[-1][1]+1 in positions[1]) == True: #Check if there is a neighbor in BOTTOM of the current cell
                abPositions.append([path[-1][0],path[-1][1]+1])
            for x in visitedPositons: #Discart all the already visited positions from the current abalible neighbors list
                if x["position"] in abPositions:
                    abPositions.remove(x["position"])
            if(len(abPositions) == 0): #If there is not any abalible neighbor go back (Backtracking)
                path.pop()
                abPositions.clear()
                continue
            if ((len(abPositions) == 0) == False): #If there is one or more abalible neighbors move to one randomly and beguin again.
                choice = random.choice(abPositions)
                X = choice[0]
                Y = choice[1]
                visitedPositons.append({"position": [X, Y], "walls": {"top": True, "bottom": True, "left": True, "right": True}})
                for x in visitedPositons:
                    if path[-1] == x['position']:
                        remove_wall(x,visitedPositons[-1])
                path.append([X, Y])
                abPositions.clear()
        else:
            print('ERROR')

# ///ENVIROMENT SETTING PART///
class MazeEnv(gym.Env):
    def __init__(self):
        self.width = 5
        self.height = 5
        self.maze = neighbors()
        self.start = [0, 0]
        self.goal = [4, 4]
        self.agent_position = self.start.copy()
        self.action_space = spaces.Discrete(4)
        self.actions = {
            0: ('top', [0, -1]),
            1: ('bottom', [0, 1]),
            2: ('left', [-1, 0]),
            3: ('right', [1, 0 ])
        }
        self.observation_space = spaces.Discrete(25)
        self.maxSteps = 100
        self.elapsedSteps = 0
    def get_obs(self): # This fuction changes the [X, Y] cordinates to a number between 0-24
        x, y = self.agent_position
        return x * self.height + y
    def reset(self, *, seed = None, options = None): # This fuction let me reset the agent to its original position ([0, 0])
        super().reset(seed=seed)
        self.agent_position = self.start.copy()
        observation = self.get_obs()
        info = {} # also we reset its info
        self.elapsedSteps = 0
        return observation, info
    def get_cell(self, position): # This fuction let me know in which cell its currently are 
        for cell in self.maze:
            if cell['position'] == position:
                return cell
    def step(self, action):
        wall, movement = self.actions[action]
        current_cell = self.get_cell(self.agent_position)
        reward = -0.1
        if not current_cell['walls'][wall]:
            self.agent_position = [
                self.agent_position[0] + movement[0],
                self.agent_position[1] + movement[1]
            ]
        else:
            reward = -1.0
        self.elapsedSteps += 1
        terminated = self.agent_position == self.goal
        truncated = self.elapsedSteps >= self.maxSteps and not terminated
        if terminated:
            reward = 10.0
        observation = self.get_obs()
        info = {"position": self.agent_position.copy()}
        return observation, reward, terminated, truncated, info

env = MazeEnv()
# Random agent/test
"""
for episode in range (100):
    observation, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0
    while not terminated and not truncated:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
    print(f"Episode: {episode + 1}")
    print("Reached goal: ", terminated)
    print("Steps: ", env.elapsedSteps)
    print("Total reward: ", total_reward)
"""
table = np.zeros((
    env.observation_space.n,
    env.action_space.n
))

eps = 1.0
learningRate = 0.1
discountFactor = 0.99

def choose_action(state, eps, table):
    x = random.random()
    if x < eps:
        action = random.choice(range(4))
    else:
        action = np.argmax(table[state])
    return action



def update_table(state, action, reward, nextState, terminated):
        if terminated:
            return ('The agent reached the end')
        value = table[state][action]
        target = reward + (np.argmax(table[nextState]) * discountFactor)
        difference = target - value
        updt_data = value + (learningRate * difference)
        table[state][action] = updt_data
