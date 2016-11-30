import random
import math

grid_h = 24
grid_w = 24
v_x = 0.05
v_y = 0.05
v_y_zeroThreshold = 0.015
r_Paddle_height = 0.2
l_Paddle_height = 1
r_Paddle_speed = 0.04
l_Paddle_speed = 0


# state = (ball_x, ball_y, velocity_x, velocity_y, RPaddle_y, LPaddle_y)
# QValue_dict = {}
# action_counter = {}     # Using this counter to help control the exploration feature of Q-learning

# func: This func returns the reward of the state tuple
def reward(state):
    ball_x, ball_y, velocity_x, velocity_y, RPaddle_y, LPaddle_y = state
    reward = 0
    if ball_x == 1:
        # win case
        if RPaddle_y <= ball_y <= RPaddle_y + r_Paddle_height:
            reward = 1
        # lose case
        else:
            reward = -1
    if ball_x == 0:
        # win ?
        if LPaddle_y <= ball_y <= LPaddle_y + l_Paddle_height:
            reward = 0

    return reward

# func: This function returns True if given state is a terminate state
def isTerminateState(state):
    ball_x, ball_y, velocity_x, velocity_y, RPaddle_y, LPaddle_y = state
    result = False
    if ball_x > 1 and velocity_x > 0:
        result = True
    if ball_x < 0 and velocity_x < 0:
        result = True
    return result

# func: This function takes a action for current state and it will return the next state
#       action contains (RPaddle_action, LPaddle_action) which have three possible values for each of them: 'up', 'stay', 'down'
def takeAction(state, action):
    ball_x, ball_y, velocity_x, velocity_y, RPaddle_y, LPaddle_y = state
    RPaddle_action, LPaddle_action = action
    # new_ball_x, new_ball_y, new_velocity_x, new_velocity_y, new_RPaddle_y, new_LPaddle_y = (0,0,0,0,0,0)
    new_ball_x = ball_x + velocity_x
    new_ball_y = ball_y + velocity_y
    new_velocity_x = velocity_x
    new_velocity_y = velocity_y
    new_RPaddle_y = 0
    new_LPaddle_y = 0
    #
    if RPaddle_action == 'up':
        new_RPaddle_y = max(RPaddle_y - r_Paddle_speed, 0)
    if RPaddle_action == 'stay':
        new_RPaddle_y = RPaddle_y
    if RPaddle_action == 'down':
        new_RPaddle_y = min(RPaddle_y + r_Paddle_speed, 1 - r_Paddle_height)
    #
    if LPaddle_action == 'up':
        new_LPaddle_y = max(LPaddle_y - l_Paddle_speed, 0)
    if LPaddle_action == 'stay':
        new_LPaddle_y = LPaddle_y
    if LPaddle_action == 'down':
        new_LPaddle_y = min(LPaddle_y + l_Paddle_speed, 1 - l_Paddle_height)
    # Bounce
    if new_ball_y < 0:
        new_ball_y = -new_ball_y
        new_velocity_y = -new_velocity_y
    if new_ball_y > 1:
        new_ball_y = 2 - new_ball_y
        new_velocity_y = -new_velocity_y
    if new_ball_x < 0:
        u = 0
        v = 0
        if new_LPaddle_y <= new_ball_y <= new_LPaddle_y + l_Paddle_height:
            new_ball_x = -new_ball_x
            new_velocity_x = max(-new_velocity_x + u, 0.03)
            new_velocity_y = new_velocity_y + v
    if new_ball_x > 1:
        u = random.random() * 0.03 - 0.015
        v = random.random() * 0.06 - 0.03
        if new_RPaddle_y <= new_ball_y <= new_RPaddle_y + r_Paddle_height:
            new_ball_x = 2 - new_ball_x
            new_velocity_x = min(-new_velocity_x + u, -0.03)
            new_velocity_y = new_velocity_y + v
    new_state = (new_ball_x, new_ball_y, new_velocity_x, new_velocity_y, new_RPaddle_y, new_LPaddle_y)

    return convert_state_ctn2dic(new_state)

# func: This function convert the continuous state into discrete state
def convert_state_ctn2dic(state):
    ball_x, ball_y, velocity_x, velocity_y, RPaddle_y, LPaddle_y = state
    new_ball_x = math.floor(grid_w * ball_x / 1) / grid_w
    new_ball_y = math.floor(grid_h * ball_y / 1) / grid_h
    new_velocity_x = v_x
    new_velocity_y = v_y
    if velocity_x < 0:
        new_velocity_x = -v_x
    if abs(velocity_y) < v_y_zeroThreshold:
        new_velocity_y = 0
    elif velocity_y < 0:
        new_velocity_y = -v_y
    #
    # print(ball_x, ball_y)
    # print(RPaddle_y)
    new_RPaddle_y = math.floor(grid_h * RPaddle_y / (1 - r_Paddle_height)) * ((1 - r_Paddle_height) / grid_h)
    if l_Paddle_height == 1:
        new_LPaddle_y = 0
    else:
        new_LPaddle_y = math.floor(grid_h * LPaddle_y / (1-l_Paddle_height)) / grid_h

    return (new_ball_x, new_ball_y, new_velocity_x, new_velocity_y, new_RPaddle_y, new_LPaddle_y)

# func: Given a state, this function determine the action of the Left Paddle
def LPaddleAction(state):
    return 'up'

# Q-learning and decision-making

# func: This function will take the state and QLearning dictionary as input then
#       returns the best action based on this state.
#       Assuming the state is always a valid state, Assuming that the prev_state has already have value in the dictionary
def QLearning(QLearning_dict, action_counter, state, prev_state, prev_action):
    # RP_action = ''
    if isTerminateState(prev_state):
        QLearning_dict[prev_state] = reward(prev_state)
        RP_action = 'terminate'
    else:
        action_counter[prev_state][prev_action] += 1
        c = 1
        alpha = c / (c + action_counter[prev_state][prev_action])
        gamma = 0.5
        # Update Q for prev_state
        if state not in QLearning_dict:     # Initilize state
            QLearning_dict[state] = {'up':0, 'stay':0, 'down':0}
            action_counter[state] = {'up':0, 'stay':0, 'down':0}
        #
        prev_QValue = QLearning_dict[prev_state][prev_action]
        QLearning_dict[prev_state][prev_action] = prev_QValue + alpha * (
            reward(prev_state) + gamma * findStateUtility(QLearning_dict, state) - prev_QValue)
        # Select the action
        RP_action = fExploration(action_counter[state], QLearning_dict[state])

    return RP_action

# func: This function finds the utility of a given state, which is maximum Q value in its action set
def findStateUtility(QLearning_dict, state):
    if isTerminateState(state):
        return reward(state)
    actionSet = QLearning_dict[state]
    return actionSet[max(actionSet, key = actionSet.get)]

# func: This is the exploration function, it will evaluate the number of times the action executed
#       and return 1, if there is action has been executed less than the threshold, it return the action
#       that has been executed least amount of times. OR 2, if all the action has been executed more than the threshold,
#       it returns the action that has the maximum Q value
def fExploration(counter_set, action_set):
    threshold = 2
    return_action = min(counter_set, key = counter_set.get)
    if counter_set[return_action] > threshold:
        return_action = max(action_set, key = action_set.get)
    return return_action


def gameplay(trainingTime):
    QLearning_dict = {}
    action_counter = {}
    # Initial state
    prev_state = (0.5, 0.5, 0.03, 0.01, 0.5 - r_Paddle_height/2, 0.5 - l_Paddle_height/2)
    QLearning_dict[prev_state] = {'up':0, 'stay':0, 'down':0}
    action_counter[prev_state] = {'up':0, 'stay':0, 'down':0}
    R_action = 'up'     # Just random assign an action
    L_action = LPaddleAction(prev_state)
    action = (R_action, L_action)
    state = takeAction(prev_state, action)
    # Game play
    sum = 0
    for i in range(trainingTime):
        averageAction = 0
        while True:
            R_action = QLearning(QLearning_dict, action_counter, state, prev_state, R_action)
            if R_action == 'terminate':
                sum += averageAction
                break
            prev_state = state
            action = (R_action, LPaddleAction(state))
            state = takeAction(state, action)
            #
            averageAction += 1
        #
        if i % 100 == 0 and i != 0:
            print(sum/100)
            sum = 0
            print("Debug")
        # Reset
        prev_state = (0.5, 0.5, 0.03, 0.01, 0.5 - r_Paddle_height / 2, 0.5 - l_Paddle_height / 2)
        R_action = max(QLearning_dict[prev_state], key = QLearning_dict[prev_state].get)
        L_action = LPaddleAction(prev_state)
        action = (R_action, L_action)
        state = takeAction(prev_state, action)




trainingTime = 10000
gameplay(trainingTime)