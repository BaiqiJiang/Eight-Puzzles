#
# eight_puzzle.py (Final project)
#
# driver/test code for state-space search on Eight Puzzles   
#
# name: Baiqi Jiang
# email: baiqi@bu.edu
# No partner(s), solo work
# UID: U41213801
# Last Update: 05/03/2023

from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * param - a parameter that can be used to specify either
            a depth limit or the name of a heuristic function
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(param)
    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(param)
    elif algorithm == 'A*':
        searcher = AStarSearcher(param)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, param):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * param - a parameter that is used to specify either a depth limit
            or the name of a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()

def process_file(filename, algorithm, param):
    """
    Takes 3 inputs: filename, algorithm, and param
    Should open the file with the specified filename for reading, 
    and it should use a loop to process the file one line at a time.
    Should also perform the cumulative computations needed to report 
    the following summary statistics after processing the entire file:
        number of puzzles solved
        average number of moves in the solutions
        average number of states tested
    """
    
    file = open(filename)
    
    # initialize parameters
    
    num_solved = 0
    sol_num_tot = 0
    state_tot = 0
    
    for line in file:
        line = line[:-1]
        init_board = Board(line)
        state = State(init_board, None, 'init')
        searcher = create_searcher(algorithm, param)
        print(line + ':' + ' ', end = '')
        
        # Using try/except to catch bugs
        
        soln = None
        try:
            soln = searcher.find_solution(state)
        except KeyboardInterrupt:
            print('search terminated, ', end='')
            
        if soln == None:
            print('no solution')
        else:
            num_solved += 1
            sol_num_tot += soln.num_moves
            state_tot += searcher.num_tested
            print(str(soln.num_moves) + ' ' + 'moves,' + ' ' + str(searcher.num_tested) + ' states tested')
            
    file.close()
    print()
    print('solved' + ' ' + str(num_solved) + ' ' + 'puzzles')
    
    if num_solved != 0:
        print('averages: ' + str(sol_num_tot / num_solved) + ' moves, ' \
             + str(state_tot / num_solved) + ' states tested')           
              
           
        
            
            
        
        
        
    