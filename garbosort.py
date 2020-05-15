
import random,math,itertools
import numpy as np

class Action:
    def __init__(self, i1=0, i2=0):
        self.i1 = i1
        self.i2 = i2
    def __eq__(self, other):
        return ((self.i1 == other.i1 and self.i2 == other.i2) or (self.i1 == other.i2 and self.i2 == other.i1))

    def __hash__(self):
        tmp = str(max(self.i1, self.i2)) + " " + str((min(self.i1, self.i2))); 
        return hash(tmp)

class State:
    def __init__(self, arr):
        self.arr = arr.copy()
    def __eq__(self, other):
        return np.array_equal(self.arr, other.arr)

    def __hash__(self):
        return hash(self.arr.tostring())

    def do_rand_swap(self):
        s1_index = random.randint(0, len(self.arr)-1)
        s2_index = random.randint(0, len(self.arr)-1)
        tmp = self.arr[s1_index]
        self.arr[s1_index] = self.arr[s2_index]
        self.arr[s2_index] = tmp

    def do_swap(self, action):
        tmp = self.arr[action.i1]
        self.arr[action.i1] = self.arr[action.i2]
        self.arr[action.i2] = tmp
def isSorted(arr):
    for i in range(arr.size-1):
         if arr[i+1] < arr[i] :
               return False
    return True

class Environment():
    def __init__(self, arr):
        #self.arr = arr.copy()
        self.state = State(arr)

    def getNextState(action):
        nextState = State(self.state.arr)
        nextState.do_swap(action) #agent swap
        #nextState.do_rand_swap() #env swap
        return nextState
    
    def update(self, action):
        nextState = State(self.state.arr)
        nextState.do_swap(action)
        #nextState.do_rand_swap()
        self.state = nextState #update environment state

    def getReward(self):
        arr = self.state.arr
        n = len(arr)
        # Create two arrays and use 
        # as pairs where first array 
        # is element and second array 
        # is position of first element 
        arrpos = [*enumerate(arr)]
    
        # Sort the array by array element 
        # values to get right position of 
        # every element as the elements 
        # of second array. 
        arrpos.sort(key = lambda it:it[1]) 
    
        # To keep track of visited elements. 
        # Initialize all elements as not 
        # visited or false. 
        vis = {k:False for k in range(n)} 
    
        # Initialize result 
        ans = 0
        for i in range(n): 
        
            # alreadt swapped or 
            # alreadt present at 
            # correct position 
            if vis[i] or arrpos[i][0] == i: 
                continue
            
            # find number of nodes 
            # in this cycle and 
            # add it to ans 
            cycle_size = 0
            j = i 
            while not vis[j]: 
            
                # mark node as visited 
                vis[j] = True
            
                # move to next node 
                j = arrpos[j][0] 
                cycle_size += 1
            
            # update answer by adding 
            # current cycle 
            if cycle_size > 0: 
                ans += (cycle_size - 1) 
        # return answer 
        return -(ans) + 5
        #should also factor in if the nums are in sorted position?
        # 6274

class Agent(): #and environment
    def __init__(self, epsilon=0.05, discount=0.3, alpha=0.9):
        self.q_values = dict()
        self.epsilon = epsilon
        self.discount = discount
        self.alpha = alpha

    def getLegalActions(self, state):
        #if (np.array_equal(state.arr, [1,2,3,4])):
        #    print("no actions possible")
        #    return []
        index_arr = [0,1,2,3]
        actions_list = []
        actions = list(itertools.combinations(index_arr, 2))
        for i in range(len(actions)): #4 choose 2
            actions_list.append(Action(actions[i][0], actions[i][1]))
        return actions_list

    def getQValue(self, state, action):
        if (isSorted(state.arr)):
            tmp = self.q_values.setdefault(tuple([state,action]), 30)
            return tmp
        else:
            tmp = self.q_values.setdefault(tuple([state,action]), 0)
            return tmp

    def computeValueFromQValues(self, state):
        values = [self.getQValue(state, action) for action in self.getLegalActions(state)]
        if (values):
            return max(values)
        else:
            return 0.0

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def computeActionFromQValues(self, state):
        legal_actions = self.getLegalActions(state) #all the legal actions
        if (len(legal_actions) == 0):
            return None
        value = self.getValue(state)
        for action in legal_actions:
            if (value == self.getQValue(state, action)): #get action which corresponds to max q
                return action

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        if (len(legalActions) == 0):
            return action

        r = random.random()
        if (r < (self.epsilon)):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state)

        return action

    def update(self, state, action, nextState, reward):
        newQValue = (1 - self.alpha) * self.getQValue(state, action) #new Qvalue
        newQValue += self.alpha * (reward + (self.discount * self.getValue(nextState)))
        self.q_values[state, action] = newQValue

if __name__ == '__main__':
    agent = Agent()
    #get agent action
    #get new state based on agent action and calculate reward
    #update environment
    #update agent

    #termState = State(np.array([1,2,3,4]))


    #generate random 4 digit arr
    #do this 1000 times until it gets it
    for i in range(0, 10000):
        if (i == 9999):
            print("last iteration:", flush=True)
        env = Environment(np.array(random.sample(range(1,9),4)))
        while True:
            #print("current env arr: " + str(env.state.arr))
            agent_action = agent.getAction(env.state)
            if (agent_action is None):
                print("already sorted" , flush=True)
                break
            cur_state = State(env.state.arr) #copy state
            env.update(agent_action)
            reward = env.getReward()
            if (i == 9999):
                print("-----------", flush=True)
                print("current env arr: " + str(cur_state.arr), flush=True)
                print("agent action: " + str(agent_action.i1) + str(agent_action.i2), flush=True)
                print("env arr after action: " + str(env.state.arr), flush=True)
                print("agent's reward: " + str(reward), flush=True)
            #print("-----------")
            #print("agent action: " + str(agent_action.i1) + str(agent_action.i2))
            #print("env arr after action: " + str(env.state.arr))
            #print("agent's reward: " + str(reward))
            
            #print("action: {}{}".format(agent_action.i1,agent_action.i2))
            #print(env.state.arr)
            #print(reward)
            agent.update(cur_state, agent_action, env.state, reward)
            if (isSorted(env.state.arr)):
                #print("found-----------------------------")   
                #print("qvalue table -------------:")
                #for key, value in agent.q_values.items():
                #    print("key:{} [{},{}], value:{}".format(key[0].arr,key[1].i1, key[1].i2,value))
                #print("qvalue table end-----------")
                break
            #print("qvalue table -------------:")
            #for key, value in agent.q_values.items():
            #    print("key:{} [{},{}], value:{}".format(key[0].arr,key[1].i1, key[1].i2,value))
            #print("qvalue table end-----------")
    #arr = np.array([5,1,2,4])

   

