# Completed by Joshua Fawcett and Hans Prieto

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
    "*** YOUR CODE HERE ***"
    closed = set()
    stack = util.Stack()
    node = (problem.getStartState(), [])
    stack.push(node)

    while True:
        if stack.isEmpty():
            raise Exception("Stack is empty")
        node = stack.pop()
        state = node[0]
        actions = node[1]
        if problem.isGoalState(state):
            return actions
        if state not in closed:
            closed.add(state)
            for child_node in problem.getSuccessors(state):
                new_state = child_node[0]
                new_actions = actions + [child_node[1]]
                new_node = (new_state, new_actions)
                stack.push(new_node)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    queue = util.Queue()
    node = (problem.getStartState(), [])
    queue.push(node)

    while True:
        if queue.isEmpty():
            raise Exception("Queue is empty")
        node = queue.pop()
        state = node[0]
        actions = node[1]
        if problem.isGoalState(state):
            return actions
        if state not in closed:
            closed.add(state)
            for child_node in problem.getSuccessors(state):
                new_state = child_node[0]
                new_actions = actions + [child_node[1]]
                new_node = (new_state, new_actions)
                queue.push(new_node)               

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    pqueue = util.PriorityQueue()
    node = (problem.getStartState(), [], 0)
    pqueue.push(node, 0)

    while True:
        if pqueue.isEmpty():
            raise Exception("Priority Queue is empty")
        node = pqueue.pop()
        state = node[0]
        path = node[1]
        cost = node[2]
        if problem.isGoalState(state):
            return path
        if state not in closed:
            closed.add(state)
            for child_node in problem.getSuccessors(state):
                new_state = child_node[0]
                new_path = path + [child_node[1]]
                new_cost = cost + child_node[2]
                new_node = (new_state, new_path, new_cost)
                pqueue.push(new_node, new_cost) 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startNode = (problem.getStartState(), [], 0) # State of form: (node, path, pathcost)

    fringe = util.PriorityQueue() # Priority queue for fringe = selects nodes with lowest priority (Based on heuristic)
    fringe.push(startNode, 0) # Start node with initial priority of 0

    closed = set() # Contains all expanded nodes

    while not fringe.isEmpty():
        curState = fringe.pop() # Select node with lowest priority

        node = curState[0] # Store current node
        path = curState[1] # Get path to current node
        pathcost = curState[2] # Get cost of path to current node

        if problem.isGoalState(node): # If current node is the goal
            return path # Return path to current node

        if node not in closed: # If current node has not been expanded
            closed.add(node) # Add current node to closed set, since we will expand it

            # 'children' is a list of the form: [(successor, action, stepCost), (), ...]
            children = problem.getSuccessors(node) # Get children of current node (expand current node)

            for child,action,cost in children: # Iterate through each child 
                if child in closed: # If child has already been expanded, then ignore it
                    continue
                else:
                    hn = heuristic(child, problem) # Heuristic: estimated cost from 'child' to goal node
                    gn = pathcost + cost # Path cost from start node to 'child'
                    newState = (child, path + [action], gn) # newState = (current node, updated path, updated cost)
                    fringe.push(newState, hn + gn) # Add newState to fringe with priority : f(n) = h(n) + g(n)

    raise Exception("Failure") # Did not find goal


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
