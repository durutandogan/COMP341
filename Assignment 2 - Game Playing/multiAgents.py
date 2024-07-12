# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        "*** YOUR CODE HERE ***"
        score = 0 #score to return

        #for prioritizing criterias:
        foodWeight = 55
        ghostWeight = -500 #avoid it 
        scaredGhostWeight = 30 #Scared is good encourage to eat
        capsuleWeight = 195

        foodDistances = []
        shortestFood = 0
        for food in newFood.asList(): #add all food distances  
            foodDistances.append(manhattanDistance(newPos, food))
       
        if (len(foodDistances) != 0):
            shortestFood = min(foodDistances) #get the shortest distance

        ghostDistances = []
        shortestGhost = 0
        for ghostPosition in successorGameState.getGhostPositions(): #add all ghost distances 
            
            ghostDistances.append(manhattanDistance(newPos, ghostPosition)) #might give error!!!

        if  (len(ghostDistances) != 0) :
            shortestGhost = min(ghostDistances)

        capsuleDistances = []
        shortestCapsule = 0
        newCapsules = successorGameState.getCapsules()
        for capsule in newCapsules:
            capsuleDistances.append(manhattanDistance(newPos, capsule))
        
        if (len(capsuleDistances) != 0):
            shortestCapsule = min(capsuleDistances)

        
        #including weights
        if (shortestFood != 0):
             score += foodWeight / shortestFood 
        if (shortestGhost != 0):
            score += ghostWeight / shortestGhost 
        if (shortestCapsule!= 0):
            score += capsuleWeight / shortestCapsule 
        

        for ghostState in newGhostStates:
            scaredTimer = ghostState.scaredTimer
            if scaredTimer > 0:
                score += scaredGhostWeight / scaredTimer 
       
        
        return successorGameState.getScore()*100 + score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        bestAction = None
        bestScore = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = self.value(successor, self.depth, 1)   
            
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction
        
       # return self.value(gameState, self.depth, 0)

    def value(self, gameState: GameState, depth, agentIndex):

        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if (agentIndex == 0):
            return self.maxValue(gameState, depth)
        
        else:
            return self.minValue(gameState, depth, agentIndex)
        

    def maxValue(self, gameState: GameState, depth):
        value = float('-inf')

        for action in gameState.getLegalActions(0): 
            successor = gameState.generateSuccessor(0, action)
            value = max(value, self.value(successor, depth , 1))

        return value  
    
    def minValue(self, gameState: GameState, depth, agentIndex):
       
        value = float('inf')
      
        for action in gameState.getLegalActions(agentIndex) :
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex == gameState.getNumAgents() - 1:
                value = min(value, self.value(successor, (depth - 1), 0))
            else:
                 value = min(value, self.value(successor, depth, (agentIndex + 1)))

        return value 
        
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestAction = Directions.STOP
        bestScore = float('-inf')

        alpha = float('-inf')
        beta = float('inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            
            score = self.alphaBeta(successor, self.depth, 1, alpha, beta)   
            
            if score > bestScore:
                bestScore = score
                bestAction = action

            alpha = max(alpha, bestScore)

            if alpha >= beta:
                break

        return bestAction


    def alphaBeta(self, gameState: GameState, depth, agentIndex, alpha, beta):

        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            return self.maxValue(gameState, depth, alpha, beta)
        
        else:
            return self.minValue(gameState, depth, agentIndex, alpha, beta)
        

    def maxValue(self, gameState: GameState, depth, alpha, beta):
        
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        value = float('-inf')

        for action in gameState.getLegalActions(0): 
            successor = gameState.generateSuccessor(0, action)
            value = max(value, self.alphaBeta(successor, depth , 1 , alpha, beta))

            if value > beta:
                return value
            
            alpha = max(alpha, value)


        return value  
    
    def minValue(self, gameState: GameState, depth, agentIndex, alpha, beta):
        
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        value = float('inf')
      
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex == gameState.getNumAgents() - 1:
                value = min(value, self.alphaBeta(successor, (depth - 1), 0, alpha, beta))
            else:
                 value = min(value, self.alphaBeta(successor, depth, agentIndex + 1 , alpha, beta))

            if value < alpha:
                return value
            
            beta = min(beta, value)

        return value
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        maxValue = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            actionValue = self.expectimax(successor, self.depth, 1)  #depth dikkat!!  
            
            if actionValue > maxValue:
                maxValue = actionValue
                bestAction = action

        return bestAction
        

    def expectimax(self, gameState: GameState, depth, agentIndex):

        if (depth == 0) or gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState)
        
        if (agentIndex == 0):
            return self.maxValue(gameState, depth)
        
        else:
            return self.expValue(gameState, depth, agentIndex)
        

    def maxValue(self, gameState: GameState, depth):

        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        maxVal = float('-inf')

        for action in gameState.getLegalActions(0): 
            successor = gameState.generateSuccessor(0, action)
            val =  self.expectimax(successor, depth, 1)
            maxVal = max(val, maxVal)

        return maxVal  
    

    def expValue(self, gameState: GameState, depth, agentIndex):

        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        expVal = 0.0
        numActions = len(gameState.getLegalActions(agentIndex))

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
           
            if agentIndex == gameState.getNumAgents() - 1:
                val = self.expectimax(successor, (depth - 1), 0)
            else:
                val = self.expectimax(successor, depth, (agentIndex + 1))
            expVal += val

        return expVal / numActions
    
        

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I have changed the weights of the features and changed the ghost postions accordingly>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = []

    #for prioritizing criterias:
    foodWeight = 350
    ghostWeight = -550 #avoid it 
    scaredGhostWeight = 40 #Scared is good encourage to eat
    capsuleWeight = 295
    
    for ghostState in newGhostStates:
        newScaredTimes.append(ghostState.scaredTimer)
    
    score = currentGameState.getScore() ###try 0

    foodDistances = []
    shortestFood = 0
    for food in newFood.asList():
        foodDistances.append(manhattanDistance(newPos, food))
    
    if len(foodDistances) != 0:
        shortestFood = min(foodDistances)
    
    ghostDistances = []
    shortestGhost = 0
    for position in currentGameState.getGhostPositions():
        ghostDistances.append(manhattanDistance(newPos, position))

    if len(ghostDistances) != 0:
        shortestGhost = min(ghostDistances)
  
    capsuleDistances = []
    shortestCapsule = 0
    for capsule in currentGameState.getCapsules():
        capsuleDistances.append(manhattanDistance(newPos, capsule))
    
    if len(capsuleDistances) != 0:
        shortestCapsule = min(capsuleDistances)

    #including weights
    if (shortestFood != 0):
        score += foodWeight / shortestFood 
    if (shortestGhost != 0):
        score += ghostWeight / shortestGhost 
    if (shortestCapsule!= 0):
        score += capsuleWeight / shortestCapsule 
        

    for ghostState in newGhostStates:
        scaredTimer = ghostState.scaredTimer
        if scaredTimer > 0:
            score += scaredGhostWeight / scaredTimer   

    return currentGameState.getScore()*100 + score


# Abbreviation
better = betterEvaluationFunction
