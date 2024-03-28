#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Baiqi Jiang
# email: baiqi@bu.edu
# No partner(s), solo work
# UID: U41213801
# Last Update: 05/03/2023


# a 2-D list that corresponds to the tiles in the goal state

GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        
        assert(len(digitstr) == 9)
        
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1
        self.digitstr = digitstr

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                self.tiles[row][col] = self.digitstr[3 * row + col]
        
        # Replace blank_r and blank_c by finding blank's position
        
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                if self.tiles[row][col] == '0':
                    self.blank_r = row
                    self.blank_c = col
                
    ### Add your other method definitions below. ###
    
    def __repr__(self):
        
        """
        returns a string representation of a Board object.
        """
        
        # No idea why rep_tiles = self.tiles[:] is not working. 
        # Use list comprehension instead.
        
        rep_tiles = [['_' if col == '0' else col for col in row] for row in self.tiles]
          
        s = str(rep_tiles[0][0]) + ' ' + str(rep_tiles[0][1]) + ' ' \
            + str(rep_tiles[0][2]) + ' ' + '\n' + str(rep_tiles[1][0]) \
            + ' ' + str(rep_tiles[1][1]) + ' ' + str(rep_tiles[1][2]) \
            + ' ' + '\n' + str(rep_tiles[2][0]) + ' ' + str(rep_tiles[2][1]) \
            + ' ' + str(rep_tiles[2][2]) + ' ' + '\n'
            
        return s
    
    def move_blank(self, direction):
        
        """
        takes as input a string direction 
        that specifies the direction in which the blank should move, 
        and that attempts to modify the contents of the called Board object accordingly. 
        Not all moves are possible on a given Board; for example, 
        it isn’t possible to move the blank down if it is already in the bottom row. 
        The method should return True or False to indicate 
        whether the requested move was possible.
        """
        
        direction_list = ['up', 'down', 'left', 'right']
        
        if direction not in direction_list:
            return False
        
        # Block Alpha: Determine the initial blank location.
    
        blank_loc_ini = [0, 0]
        
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                if self.tiles[row][col] == '0':
                    blank_loc_ini[0] = row
                    blank_loc_ini[1] = col
                    
        # Block Beta: Make a deep copy of initial blank location first, called blank_loc
        # Then change the index of blank_loc by the value of direction
        # Use if-else to determine if location index out of range, return False in this case
        # Finally, change the val of self.tiles and then self.blank_r and _c
                    
        blank_loc = blank_loc_ini[:]
                    
        pos_loc = [[0, 0], [0, 1], [0, 2],
                   [1, 0], [1, 1], [1, 2],
                   [2, 0], [2, 1], [2, 2]]    # All possible locations
        
        if direction == 'up':
            blank_loc[0] -= 1
        elif direction == 'down':
            blank_loc[0] += 1
        elif direction == 'left':
            blank_loc[1] -= 1
        else:
            blank_loc[1] += 1   
    
        if blank_loc not in pos_loc:
            return False
        else:
            self.tiles[blank_loc_ini[0]][blank_loc_ini[1]] = self.tiles[blank_loc[0]][blank_loc[1]]
            self.tiles[blank_loc[0]][blank_loc[1]] = '0'
            self.blank_r = blank_loc[0]
            self.blank_c = blank_loc[1]
            return True
        
    def digit_string(self):
        
        """
        creates and returns a string of digits that corresponds to the 
        current contents of the called Board object’s tiles attribute.  
        """
        
        s = ''
        
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                s += self.tiles[row][col]
        
        return s
    
    def copy(self):
        
        """
        returns a newly-constructed Board object that is a deep copy of the called object
        """
        
        copy_tiles = [[col for col in row] for row in self.tiles] # Make a deep copy of self.tiles
        s = ''
        
        for row in range(len(copy_tiles)):
            for col in range(len(copy_tiles[0])):
                s += copy_tiles[row][col]
            
        return Board(s)
    
    def num_misplaced(self):
        
        """
        counts and returns the number of tiles 
        in the called Board object that are not where they should be in the goal state.        
        """
        
        count = 0
        
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                if self.tiles[row][col] != '0' and self.tiles[row][col] != GOAL_TILES[row][col]:
                    count += 1
        
        return count
    
    def __eq__(self, other):
        
        """
        return True if the called object (self) and the argument (other) 
        have the same values for the tiles attribute, and False otherwise.    
        """
        
        if self.tiles == other.tiles:
            return True
        else:
            return False
        
    def manh_dis(self):
        
        """
        A method that used to calculate the manhattan distance, which is useful for
        searcher's herustic function
        """
        
        manh_dis = 0    # initilaize the distance
        
        for row in range(3):
            for col in range(3):
                current_digit = self.tiles[row][col]
                if current_digit != '0':
                    target_row_chk = None       # Set a None checker, meaningless loc
                    target_col_chk = None       # Set a None checker, meaningless loc
                    
                    # Process the calc
                    
                    for target_row in range(3):
                        
                        for target_col in range(3):
                            
                            if GOAL_TILES[target_row][target_col] == current_digit:
                                target_row_chk = target_row    # Checker update, res found
                                target_col_chk= target_col     # Checker update, res found
                                break
                            
                        if target_row_chk != None and target_col_chk != None:
                            break
                    
                    manh_dis += abs(row - target_row_chk) + abs(col - target_col_chk)
                    
        return manh_dis
                            
                            
                            
                            
                            
                                
                    
                