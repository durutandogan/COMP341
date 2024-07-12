# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    ### Got help from the Psuedocode from book and the slide 4 (58)
    
    frontier = util.Stack()
    frontier.push((problem.getStartState(), [])) #frontier holds two things : the state and the path

    explored = set() #to not to check visited nodes
    ###solution = [] 

    while not (frontier.isEmpty()) :
        
        current, solution = frontier.pop() 
        ####solution.append(current)

        if not (current in explored): 
            explored.add(current) 
            if problem.isGoalState(current):
                return solution #found solution if it is the goal state

        
        
        for successor_state, successor_action, successor_cost in problem.getSuccessors(current) :
            if not (successor_state in explored):
                frontier.push((successor_state, solution + [successor_action]))

    return [] #return failure

      
    
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    ### Got help from the Psuedocode from book (page 82)

    if problem.isGoalState(problem.getStartState() ):
        return [] ##checks whether the initial goal is the goal state

    frontier = util.Queue()
    frontier.push((problem.getStartState(), [])) #frontier holds two things : the state and the path
    
    explored = set() #to not to check visited nodes
    

    while not (frontier.isEmpty()) :
        current, solution = frontier.pop()
    
        if not (current in explored):
            explored.add(current)

            if (problem.isGoalState(current)):
              return solution #found solution if it is the goal state
        
        for successor_state, successor_action, successor_cost in problem.getSuccessors(current) :
            if not (successor_state in explored) and not (successor_state in (node[0] for node in frontier.list)):
                frontier.push((successor_state, solution + [successor_action]))
                

    return [] #return failure 
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
     ### Got help from the Psuedocode from book (page 84)
    
    node = (problem.getStartState(), [], 0) #holds the state, path and cost(0)
    frontier = util.PriorityQueue()
    frontier.push(node, 0) #frontier holds two things : the state and the path

    explored = set()

    while not frontier.isEmpty():
      
        current, solution, cost = frontier.pop() #chooses the lowest-cost node in the frontier

        if not (current in explored):
            explored.add(current)

            if problem.isGoalState(current):
              return solution

            for successor_state, successor_action, successor_cost in problem.getSuccessors(current) :
                  # for node in frontier.heap:
                   if not (successor_state in explored) :
                       #    if not (successor_state in frontier.heap):
                     
                        updated_cost = cost + successor_cost
                        frontier.push((successor_state, solution + [successor_action], updated_cost), updated_cost)
      
    return []
    util.raiseNotDefined()
 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"     
    node = (problem.getStartState(), [], 0) #holds the state, path and cost(0)
    frontier = util.PriorityQueue()
    frontier.push(node, 0) #frontier holds two things : the state and the path

    explored = set()

    while not frontier.isEmpty():
      
        current, solution, cost = frontier.pop() #chooses the lowest-cost node in the frontier

        if not (current in explored):
            explored.add(current)

            if problem.isGoalState(current):
              return solution

            for successor_state, successor_action, successor_cost in problem.getSuccessors(current) :
                    if not (successor_state in explored):
                        h = heuristic(successor_state, problem) #calculates heuristic
                        frontier.push((successor_state, solution + [successor_action], cost + successor_cost), cost + successor_cost + h)
                    
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
