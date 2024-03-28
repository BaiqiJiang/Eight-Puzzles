#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Baiqi Jiang
# email: baiqi@bu.edu
# No partner(s), solo work
# UID: U41213801
# Last Update: 05/03/2023


import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    
    def __init__(self, depth_limit):
        """
        constructs a new Searcher object by initializing 3 attributes.
        """
        
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
    
    def add_state(self, new_state):
         """
         takes a single State object called new_state and 
         adds it to the Searcher‘s list of untested states.
         """
         
         self.states += [new_state]
         
    def should_add(self, state):
        """
        takes a State object called state and 
        returns True if the called Searcher should add state to its list of untested states, 
        and False otherwise.
        """
        
        chkpoint_for_num = (state.num_moves > self.depth_limit)
        if self.depth_limit == -1:
            chkpoint_for_num = False
        chkpoint_for_cyc = (state.creates_cycle())
        
        if chkpoint_for_num == False and chkpoint_for_cyc == False:
            return True
        return False
        
    def __repr__(self):
        """ 
        returns a string representation of the Searcher object
        referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    def add_states(self, new_states):
        """
        takes a list State objects called new_states, 
        and that processes the elements of new_states one at a time 
        """
        
        for state in new_states:
            if self.should_add(state) == True:
                self.add_state(state)
                
    def next_state(self):
        """ 
        chooses the next state to be tested from the list of 
        untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s
    
    def find_solution(self, init_state):
        """
        performs a full state-space search that 
        begins at the specified initial state init_state and 
        ends when the goal state is found or when the Searcher runs out of untested states.
        """
        
        self.add_state(init_state)
        is_empty = (self.states == [])
        
        while is_empty == False:
            self.num_tested += 1
            tst_state_nxt = self.next_state()
            if tst_state_nxt.board.tiles == GOAL_TILES:
                return tst_state_nxt
            successors = tst_state_nxt.generate_successors()
            self.add_states(successors)
        
        return None
        
### Add your BFSeacher and DFSearcher class definitions below. ###

class BFSearcher(Searcher):
    """
    A subclass inherited from Searcher.
    This subclass should perform breadth-first search (BFS) instead of random search.
    """
    
    def next_state(self):
        """
        Overrides (i.e., replaces) the next_state method that is inherited from Searcher. 
        Rather than choosing at random from the list of untested states, 
        this version of next_state should follow FIFO (first-in first-out) ordering 
        – choosing the state that has been in the list the longest.
        """
        
        choice = [[i.num_moves, i] for i in self.states]
        pk = min(choice)
        self.states.remove(pk[1])
        return pk[1]
    
class DFSearcher(Searcher):
    """
    A subclass inherited from Searcher.
    This subclass should perform depth-first search (DFS) instead of random search.
    """
    
    def next_state(self):
        """
        Similar to BFSearcher's method.
        However, follow LIFO (last-in first-out) ordering:
        choosing the state that was most recently added to the list.
        """
        
        choice = [[i.num_moves, i] for i in self.states]
        pk = max(choice)
        self.states.remove(pk[1])
        return pk[1]
        
def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###

def h1(state):
    """ 
    a heuristic function that returns the num_misplaced()
    """
    
    return state.board.num_misplaced()

def h2(state):
    """
    Compared to num_misplaced, a better heuristic function that uses the manhattan distance 
    """
    
    return state.board.manh_dis()
    
class GreedySearcher(Searcher):
    """ 
    A class for objects that perform an informed greedy state-space
    search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ###
    
    def __init__(self, heuristic):
        """
        constructs a new GreedySearcher object by initializing attributes.
        """
        
        super().__init__(-1)
        self.heuristic = heuristic
        
    def priority(self, state):
        """ 
        computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher
        """
        
        return -1 * self.heuristic(state)
    
    def add_state(self, state):
        """
        Overrides (i.e., replaces) the add_state method that is inherited from Searcher. 
        Rather than simply adding the specified state to the list of untested states, 
        the method should add a sublist that is a [priority, state] pair, 
        where priority is the priority of state that is determined by calling the priority method. 
        """
        
        self.states += [[self.priority(state), state]]
        
    def next_state(self):
        """
        Overrides (i.e., replaces) the next_state method that is inherited from Searcher. 
        This version of next_state should choose one of the states with the highest priority.
        """
        
        pk = max(self.states)
        self.states.remove(pk)
        return pk[1]
    
    def __repr__(self):
        """ 
        returns a string representation of the GreedySearcher object
        referred to by self.
        """
        
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s


### Add your AStarSeacher class definition below. ###

class AStarSearcher(GreedySearcher):
    """
    A class for searcher objects that perform A* search.
    Like greedy search, A* is an informed search algorithm 
    that assigns a priority to each state based on a heuristic function, 
    and that selects the next state based on those priorities. 
    However, when A* assigns a priority to a state, 
    it also takes into account the cost that has already been expended to get to that state.
    """
    
    def priority(self, state):
        """ 
        Since priorty changed, this is an overrided method.
        The priority of a state is computed using the following pseudocode:
        priority(state) = -1 * (heuristic(state) + num_moves)
        """
        
        return -1 * (self.heuristic(state) + state.num_moves)
        
        
    
    