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
    print('Running tinyMazeSearch!')
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
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
    #To get the state where the game starts from
    intialState = problem.getStartState()
    #State of the game along with list of actions
    initialNode = (intialState, [])
    
    #Set of the visited nodes
    nodesVisited = set()
    #Stack of unvisited nodes
    #Using Stack definition from util
    unvisitedNodes = util.Stack()
       
    unvisitedNodes.push(initialNode)
 
    while not unvisitedNodes.isEmpty():
        #print('Unvisited Nodes:{}'.format(unvisitedNodes))
        #The node on the top of the stack
        currentNode = unvisitedNodes.pop()
        #Adding the first node to set of visited nodes
        nodesVisited.add(currentNode[0])
        #print('Nodes Visited: {}'.format (nodesVisited))
        #Checking if the node is the required state
        #currentNode[0] is the node's spatial location
        if problem.isGoalState(currentNode[0]):
            #print('GoalState: {}'.format(currentNode[0]))
            return currentNode[1]
        #Pushing successors if the node is not the goal state
        nodeSuccessors = problem.getSuccessors(currentNode[0])
        #print('Successors: {}'.format(nodeSuccessors))
        for successor in nodeSuccessors:
            #print('Items: {}'.format(item))
            if successor[0] in nodesVisited:
                continue
            #currentNode[1] is list of actions that led to state currentNode[0]
            unvisitedNodes.push((successor[0], currentNode[1] + [successor[1]]))
    return None

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    #To get the state where the game starts from
    intialState = problem.getStartState()   
    #State of the game along with list of actions
    initialNode = (intialState, [])
    
    #Set of visited nodes
    nodesVisited = set()
    #Queue for unvisited nodes
    #Using Queue definition from util
    unvisitedNodes = util.Queue()
       
    unvisitedNodes.push(initialNode)
    #To follow first in first out
    nodesVisited.add(intialState)

    while not unvisitedNodes.isEmpty():
        #The node in the start of the queue
        currentNode = unvisitedNodes.pop()
        
        #currentNode[0] is the node's spatial location
        if problem.isGoalState(currentNode[0]):
            #Returning the goal state
            return currentNode[1]
        
        nodeSuccessors = problem.getSuccessors(currentNode[0])
        for neighbour in nodeSuccessors:
            if neighbour[0] in nodesVisited:
                continue
            #Add to visited if it wasn't earlier
            nodesVisited.add(neighbour[0])
            #currentNode[1] is list of actions that led to state currentNode[0]
            #To find successors in next steps
            unvisitedNodes.push((neighbour[0], currentNode[1] + [neighbour[1]]))

    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""    
    
    #Start state of the problem passed an argument
    initialState = problem.getStartState()
    #[0] is the state, [1] is the sequence of actions, [2] is the priority determined by the path cost
    initialNode = (initialState, [], 0)
    
    #Using definition of PriorityQueue from util
    #Queue to maintain list of unvisited nodes
    unvisitedNodes = util.PriorityQueue()   
    unvisitedNodes.push(initialNode, 0)
    
    #Set of visited nodes
    visitedNodes = set()

    while not unvisitedNodes.isEmpty():
        
        currentNode = unvisitedNodes.pop()
        
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]
        
        #Add to visited nodes if it was unvisited earlier
        if currentNode[0] not in visitedNodes:
            visitedNodes.add(currentNode[0])
            
            for successor in problem.getSuccessors(currentNode[0]):
                if successor[0] not in visitedNodes:
                    #Cost to reach that node and set priority
                    #To be able to choose from multiple successors based on the cost/priority
                    cost = currentNode[2] + successor[2]
                    unvisitedNodes.push((successor[0], currentNode[1] + [successor[1]], cost), cost)

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
   
    #Start state of the problem passed an argument
    initialState = problem.getStartState()
    #[0] is the state, [1] is the sequence of actions, [2] is the priority determined by the path cost
    initialNode = (initialState, [], 0)
    
    #Using definition of PriorityQueue from util
    #Queue to maintain list of unvisited nodes
    unvisitedNodes = util.PriorityQueue()   
    unvisitedNodes.push(initialNode, 0)
    
    #Set of visited nodes
    visitedNodes = set()

    while not unvisitedNodes.isEmpty():
        
        currentNode = unvisitedNodes.pop()
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]
        
        if currentNode[0] not in visitedNodes:
            visitedNodes.add(currentNode[0])
            
            for successor in problem.getSuccessors(currentNode[0]):
                if successor[0] not in visitedNodes:
                    cost = currentNode[2] + successor[2]
                    #To find costs including cost of heuristic function
                    totalCost = cost + heuristic(successor[0], problem)
                    unvisitedNodes.push((successor[0], currentNode[1] + [successor[1]], cost), totalCost)

    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
