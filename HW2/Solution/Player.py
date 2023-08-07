from Board import BoardUtility
import random
import numpy as np
import copy
# parham rezaei 400108547
#FIXME: USE depth 3 with minimaxprob [must mostly win >=9] and depth 2(obviously faster) or 3 with minimax [must mostly win 10]

class Player:
    def __init__(self, player_piece):
        self.piece = player_piece
        self.opp = 3- self.piece
        self.__3r = 5
        self.__4r = 20
        self.timestep = 0

    def play(self, board):
        return 0
    
    
    def count_consecutive(self,lst, piece):
        counts = []
        count = 0
        for item in lst:
            if item == piece:
                count += 1
            else:
                if count > 0:
                    counts.append(count)
                    count = 0
        if count > 0:
            counts.append(count)
        return counts
        


    def evalboard(self, board):
        
        score = 0
        # row
        for i in range(board.shape[0]):
            row_counts = self.count_consecutive(board[i],self.piece)
            num_threes = row_counts.count(3)
            num_fours = row_counts.count(4)
            score += num_threes * self.__3r + num_fours*self.__4r

        # cln
        for j in range(board.shape[1]):
            col_counts = self.count_consecutive(board[:,j],self.piece)
            num_threes = col_counts.count(3)
            num_fours = col_counts.count(4)
            score += num_threes * self.__3r + num_fours*self.__4r

        # diag
        diag_counts = [self.count_consecutive(np.diag(board, k),self.piece) for k in range(-2, 3)]
        for counts in diag_counts:
            num_threes = counts.count(3)
            num_fours = counts.count(4)
            score += num_threes * self.__3r + num_fours*self.__4r

        # diag2
        flip_arr = np.fliplr(board)
        diag_counts = [self.count_consecutive(np.diag(flip_arr, k),self.piece) for k in range(-2, 3)]
        for counts in diag_counts:
            num_threes = counts.count(3)
            num_fours = counts.count(4)
            score += num_threes * self.__3r + num_fours*self.__4r


        #row
        for i in range(board.shape[0]):
            row_counts = self.count_consecutive(board[i],self.opp)
            num_threes = row_counts.count(3)
            num_fours = row_counts.count(4)
            score -= num_threes * self.__3r + num_fours*self.__4r

        # cln
        for j in range(board.shape[1]):
            col_counts = self.count_consecutive(board[:,j],self.opp)
            num_threes = col_counts.count(3)
            num_fours = col_counts.count(4)
            score -= num_threes * self.__3r + num_fours*self.__4r

        # diag
        diag_counts = [self.count_consecutive(np.diag(board, k),self.opp) for k in range(-2, 3)]
        for counts in diag_counts:
            num_threes = counts.count(3)
            num_fours = counts.count(4)
            score -= num_threes * self.__3r + num_fours*self.__4r

        # diag
        flip_arr = np.fliplr(board)
        diag_counts = [self.count_consecutive(np.diag(flip_arr, k),self.opp) for k in range(-2, 3)]
        for counts in diag_counts:
            num_threes = counts.count(3)
            num_fours = counts.count(4)
            score -= num_threes * self.__3r + num_fours*self.__4r


        return score




class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        #print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth


        

    def minValue(self, board, alpha, beta, depth):
        if(BoardUtility.has_player_won(board,self.opp)):
            return -999999 * (self.depth+1-depth)
        if(BoardUtility.has_player_won(board,self.piece)):
            return 999999 * (self.depth+1-depth)
        
        if depth == self.depth:
            return self.evalboard(board)
        
        val = float('inf')
        
        for quarter in [1, 2, 3, 4]:
            for rotation in ["skip","clockwise", "anticlockwise"]:
                if rotation=="skip" and quarter>1:
                    continue
                vl = BoardUtility.get_valid_locations(board)
                random.shuffle(vl)
                for pos in vl:
                    successor = np.array(board)
                    BoardUtility.make_move(successor,pos[0],pos[1],quarter, rotation, self.opp)
                    val = min(val, self.maxValue(successor,alpha,beta,depth+1))
                    if val <= alpha:
                        return val
                    beta = min(val,beta)
        return val

    def maxValue(self, board, alpha, beta, depth):
        if(BoardUtility.has_player_won(board,self.piece)):
            return 999999 * (self.depth+1-depth)
        if(BoardUtility.has_player_won(board,self.opp)):
            return -999999 * (self.depth+1-depth)
        if depth == self.depth:
            return self.evalboard(board)
        
        val = float('-inf')
       
        for quarter in [1, 2, 3, 4]:
            for rotation in ["skip","clockwise", "anticlockwise"]:
                if rotation=="skip" and quarter>1:
                    continue
                vl = BoardUtility.get_valid_locations(board)
                random.shuffle(vl)
                for pos in vl:
                    successor = np.array(board)
                    BoardUtility.make_move(successor,pos[0],pos[1],quarter,rotation,self.piece)
                    val = max(val,self.minValue(successor,alpha,beta,depth+1))
                    if val >= beta:
                        return val
                    alpha = max(val, alpha)
        return val



        
    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        alpha = float('-inf')
        beta = float('+inf')
        val = float('-inf')
        
        for quarter in [1,2,3,4]:
            for rotation in ["skip","clockwise", "anticlockwise"]:
                if rotation=="skip" and quarter>1:
                    continue
                vl = BoardUtility.get_valid_locations(board)
                random.shuffle(vl)
                for pos in vl:
                    successor = np.array(board)
                    BoardUtility.make_move(successor,pos[0],pos[1],quarter,rotation,self.piece)
                    t = self.minValue(successor,alpha,beta,1)
                    if t >= val:
                        val = t
                        next = [pos,quarter,rotation]
                    if val >= beta:
                        return next
                    alpha = max(val, alpha)
        return next


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def minValue(self, board, alpha, beta, depth):
        
        if(BoardUtility.has_player_won(board,3-self.piece)):
            return -999999*(self.depth+1-depth)
        if(BoardUtility.has_player_won(board,self.piece)):
            return 999999*(self.depth+1-depth)
        if depth == self.depth:
            return self.evalboard(board)
        val = float('inf')
        
        for quarter in [1, 2, 3, 4]:
            for rotation in ["clockwise", "anticlockwise","skip"]:
                if rotation == "skip" and quarter > 1:
                    continue
                vl = BoardUtility.get_valid_locations(board)
                random.shuffle(vl)
                for pos in vl:
                    successor = np.array(board)
                    BoardUtility.make_move(successor,pos[0],pos[1],quarter, rotation, self.opp)
                    val = min(val, self.maxValue(successor,alpha,beta,depth+1))
                    if val <= alpha:
                        return val
                    beta = min(val,beta)
        return val


    def maxValue(self, board, alpha, beta, depth):
        if(BoardUtility.has_player_won(board,self.piece)):
            return 999999*(self.depth+1-depth)
        if(BoardUtility.has_player_won(board,3-self.piece)):
            return -999999*(self.depth+1-depth)
        if depth == self.depth:
            return self.evalboard(board)
        
        val = float('-inf')
        v=[]
        for i in range(7):
            mov = [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]
            succ = np.array(board)
            BoardUtility.make_move(succ,mov[0][0],mov[0][1],mov[1],mov[2],self.piece)
            v.append(self.minValue(succ,alpha,beta,depth+1))
        v = np.mean(v)
        
        for quarter in [1, 2, 3, 4]:
            for rotation in ["clockwise", "anticlockwise","skip"]:
                if rotation == "skip" and quarter > 1:
                    continue
                vl = BoardUtility.get_valid_locations(board)
                random.shuffle(vl)
                for pos in vl:
                    successor = np.array(board)
                    BoardUtility.make_move(successor,pos[0],pos[1],quarter,rotation,self.piece)
                    val = max(val,self.minValue(successor,alpha,beta,depth+1))
                    if val >= beta:
                        return val*(1-self.prob_stochastic) + self.prob_stochastic*v
                    alpha = max(val, alpha)
        return val*(1-self.prob_stochastic) + self.prob_stochastic*v
    
    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        alpha = float('-Inf')
        beta = float('+inf')
        val = float('-Inf')
        if np.random.binomial(1,self.prob_stochastic) == 1:
            move = [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["clockwise", "anticlockwise"])]
            return move
        for quarter in [1,2,3,4]:
            for rotation in ["clockwise", "anticlockwise","skip"]:
                if rotation == "skip" and quarter > 1:
                    continue
                vl = BoardUtility.get_valid_locations(board)
                random.shuffle(vl)
                for pos in vl:
                    successor = np.array(board)
                    BoardUtility.make_move(successor,pos[0],pos[1],quarter,rotation,self.piece)
                    t = self.minValue(successor,alpha,beta,1)
                    if t >= val:
                        val = t
                        next = [pos,quarter,rotation]
                    if val >= beta:
                        return next
                    alpha = max(val, alpha)
        return next



