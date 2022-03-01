from cmath import inf
import numpy as np
import itertools as itt
import os, sys

class Robot:
    def __init__(self, piece):
        self.piece = piece
        self.last_state = np.full((int(os.environ['N']),int(os.environ['N'])),0)
        self.current_state = np.full((int(os.environ['N']),int(os.environ['N'])),0)
        self.hypothetical_state = np.full((int(os.environ['N']),int(os.environ['N'])),0)

    def addPiece(self, col, grid):
        if grid is None:
          temp = self.hypothetical_state.T
        else:
          temp = grid.T
        if np.count_nonzero(temp[col]) == int(os.environ['N']):
            return -1
        for i,x in enumerate(temp[col]):
            if(int(x) != 0):
                temp[col][i-1] = self.piece
                return (col, i-1)
        temp[col][-1] = self.piece
        return (col, int(os.environ['N'])-1)


    # generate a recurrence tree, traverse bottom-up, with a-b pruning

    def nextState(self, grid=None, depth=1, ab=None, locs=None):
      if(depth == 0):
        return None
      loc = ([0,0] if locs==None else locs)
      t_ab = ([-inf,inf] if ab==None else ab)
      for i in range(int(os.environ['N'])):
        if(depth == 1):
          t_loc = self.addPiece(i,grid)
          t_grid = np.copy(grid)
          if(t_loc != -1):
            # don't forget to alternate pieces
            #hueristic ignores piece type - sim does not
            t_grid[t_loc[1]][t_loc[0]] = (self.piece+(depth%2))
            if(self.validMove(t_loc)):
                star = self.strata(t_loc, t_grid)
                if (star > t_ab[0]): #if better alpha swap for best
                    t_ab[0] = star
                    loc[0] = t_loc
                if(star < t_ab[1]): #if better beta swap for best
                    t_ab[1] = star
                    loc[1] = t_loc
        else:
          ns = self.nextState(np.copy(grid), depth-1, t_ab, loc)
          if(t_ab == None):
            t_ab = ns[0]
          else:
            if t_ab[0] > ns[0][0]: #if better alpha swap for best
                t_ab[0] = ns[0][0]
                loc[0] = ns[1][0]
            if t_ab[1] < ns[0][1]: #if better beta swap for best
                t_ab[1] = ns[0][1]
                loc[1] = ns[1][1]
      return (t_ab, loc)
    
    def validMove(self,coord):
      x = coord[0]
      y = coord[1]
      if(x < 0 or x > int(os.environ['N'])-1):
        return False
      if(y < 0 or y > int(os.environ['N'])-1):
        return False
      return True

    # for following functions
    # h is hueristic value

    def diag_dr(self, coord, grid=None):
      h = 1
      if(coord[0]+1 >= int(os.environ['N']) or coord[1]+1 >= int(os.environ['N'])):
        return
      t = grid[coord[1]+1][coord[0]+1]
      if t > 0:
        cnt = 1
        while(((coord[0] + cnt) < int(os.environ['N']) and (coord[1] + cnt) < int(os.environ['N'])) and grid[coord[1]+cnt][coord[0]+cnt] == t):
          cnt += 1
          h += h
        return (h, t)
    
    def diag_dl(self, coord, grid=None):
      h = 1
      if(coord[0]-1 < 0 or coord[1]+1 >= int(os.environ['N'])):
        return
      t = grid[coord[1]+1][coord[0]-1]
      if t > 0:
        cnt = 1
        while(((coord[0] - cnt) > -1 and (coord[1] + cnt) < int(os.environ['N'])) and grid[coord[1]+cnt][coord[0]-cnt] == t):
          cnt += 1
          h += h
        return (h, t)
    
    def diag_ul(self, coord, grid=None):
      h = 1
      if(coord[0]-1 < 0 or coord[1]-1 < 0):
        return
      t = grid[coord[1]-1][coord[0]-1]
      if t > 0:
        cnt = 1
        while(((coord[0] - cnt) > -1 and (coord[1] - cnt) > -1) and grid[coord[1]-cnt][coord[0]-cnt] == t):
          cnt += 1
          h += h
        return (h, t)

    def diag_ur(self, coord, grid=None):
      h = 1
      if(coord[1]-1 < 0 or coord[0]+1 >= int(os.environ['N'])):
        return
      t = grid[coord[1]-1][coord[0]+1]
      if t > 0:
        cnt = 1
        while(((coord[1] - cnt) > -1 and (coord[0] + cnt) < int(os.environ['N'])) and grid[coord[1]-cnt][coord[0]+cnt] == t):
          cnt += 1
          h += h
        return (h, t)

    def left(self, coord, grid=None):
      h = 1
      if(coord[0]-1 < 0):
        return
      t = grid[coord[1]][coord[0]-1]
      if t > 0:
        cnt = 1
        while((coord[0] - cnt) >= 0 and grid[coord[1]][coord[0]-cnt] == t):
          cnt += 1
          h += h
        return (h, t)

    def right(self, coord, grid=None):
      h = 1
      if(coord[0]+1 >= int(os.environ['N'])):
        return
      t = grid[coord[1]][coord[0]+1]
      if t > 0:
        cnt = 1
        while((coord[0] + cnt) < int(os.environ['N'])-1 and grid[coord[1]][coord[0]+cnt] == t):
          cnt += 1
          h += h
        return (h, t)

    # don't need to look up because of game physics

    def down(self, coord, grid=None):
      h = 1
      if(coord[1]+1 >= int(os.environ['N'])):
        return
      t = grid[coord[1]+1][coord[0]]
      if t > 0:
        cnt = 1
        while((coord[1] + cnt) < int(os.environ['N'])-1 and grid[coord[1]+cnt][coord[0]] == t):
          cnt += 1
          h += h
        return (h, t)

    #accumulate indiv. h to collective h
    def calc_unitA(self,l):
      if l[1][0] != None:
        l[1][0] = (l[1][0][0]**2, l[1][0][1])
      A = 0
      B = 0
      for a in l:
        A += sum( [i[0]/int(os.environ['M']) for i in a if i != None and i[1] == 1] )
        B += sum( [i[0]/int(os.environ['M']) for i in a if i != None and i[1] == 2] )
      G = [A,B]
      return (sum(G))

    def strata(self, coord, grid=None):
      huer_ray = [[self.left(coord, grid), self.right(coord, grid)],[self.down(coord, grid)],[self.diag_dr(coord, grid),self.diag_ul(coord, grid)],[self.diag_dl(coord, grid), self.diag_ur(coord, grid)]]
      huer = self.calc_unitA(huer_ray)
      return huer

    #check list for group of size M+
    def hasWinner(self, result):
        for player, value in result:
            if player != 0 and value >= int(os.environ['M']):
                return True

    # check hyporthical state for completeness
    def gameComplete(self):
      for y in range(int(os.environ['N'])):
        for x in range(int(os.environ['N'])):
          result = [(n, sum(1 for n in group)) for n, group in itt.groupby(self.hypothetical_state[y,:])]
          result += [(n, sum(1 for n in group)) for n, group in itt.groupby(self.hypothetical_state.T[x,:])]
          submatrixR = self.hypothetical_state[:,x:]
          result += [(n, sum(1 for n in group)) for n, group in itt.groupby(submatrixR.diagonal())]
          result += [(n, sum(1 for n in group)) for n, group in itt.groupby(np.fliplr(submatrixR).diagonal())]
          submatrixD = self.hypothetical_state[y:,:]
          result += [(n, sum(1 for n in group)) for n, group in itt.groupby(submatrixD.diagonal())]
          result += [(n, sum(1 for n in group)) for n, group in itt.groupby(np.fliplr(submatrixD).diagonal())]
          if self.hasWinner(result):
              return True

    # bot runtime
    def run(self, current_state):
        self.current_state = current_state
        #does minmax tree wi a-b pruning
        next_state = self.nextState(current_state.copy(), 4) # do 4 level tree
        return next_state[1][next_state[0].index(max(next_state[0]))][0]