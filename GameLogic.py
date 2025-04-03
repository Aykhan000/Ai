class Node:
    def __init__(self, id, string, p1, p2, level, player_turn):
        self.id=id
        self.string=string
        self.p1=p1
        self.p2=p2
        self.level=level
        self.player_turn = player_turn

class Game_tree:
    def __init__(self):
        self.set_of_nodes=dict() 
        self.set_of_arcs=dict()
    
    def adding_node(self, node):
        key = ("".join(node.string),node.p1,node.p2,node.level)
        self.set_of_nodes[key] = node
        
    def adding_arc(self, initial_node_id, end_node_id):
        self.set_of_arcs[initial_node_id]=self.set_of_arcs.get(initial_node_id,[])+[end_node_id]

class Logic():
    def __init__(self,root_node):
        self.node_counter = 2    
        self.gt = Game_tree()
        self.CurrentNode = root_node

    def ReplacePairInNumber(self,number, idx, replace_with):    
        # Replace the digit at idx+1 with replace_with and remove the digit at idx.
        number[idx+1] = replace_with  
        del number[idx]
        return number

    def get_possible_moves(self,node):
        moves = []
        for i in range (0,len(node.string)-1):
            move = self.compute_move(i,node)
            moves.append(move)
        return moves

    def Player_Play(self,selected_pair_id):
        moves = self.get_possible_moves(self.CurrentNode)
        self.CurrentNode = moves[selected_pair_id]

    def AI_Play(self,search_depth,useMinmax):
        moves = self.get_possible_moves(self.CurrentNode)
        best_score = -99999 
        best_move = None
        for move in moves:
            if useMinmax:
                score = self.minmax(move,search_depth,not move.player_turn)
                print(score,move.string,move.p1,move.p2)
            else:
                score = self.alphabeta(move, search_depth, float("-inf"),float("inf"), not move.player_turn)
                print(score,move.string,move.p1,move.p2)

            if score > best_score:
                best_score = score
                best_move = move
        self.CurrentNode = best_move
        return best_move, best_score

    def compute_move(self,pair_id,node):
        if  0 <= pair_id < len(node.string)-1:
            id_new='A'+str(self.node_counter)
            self.node_counter+=1
            changed_string=node.string.copy()
            sum_of_pair = int(changed_string[pair_id]) + int(changed_string[pair_id+1])
            if (sum_of_pair==7):
                self.ReplacePairInNumber(changed_string,pair_id,"2")
                p1_new = node.p1+2
                p2_new = node.p2+2
            elif(sum_of_pair<7):
                self.ReplacePairInNumber(changed_string,pair_id,"3")
                if node.player_turn:
                    p1_new = node.p1-1
                    p2_new = node.p2
                else:
                    p1_new = node.p1
                    p2_new = node.p2-1
            else:
                self.ReplacePairInNumber(changed_string,pair_id,"1")
                if node.player_turn:
                    p1_new = node.p1+1
                    p2_new = node.p2
                else:
                    p1_new = node.p1
                    p2_new = node.p2+1
            level_new=node.level+1
            player_turn_new = not node.player_turn
            new_node=Node(id_new, changed_string, p1_new, p2_new, level_new, player_turn_new)
            
            key = ("".join(new_node.string),new_node.p1,new_node.p2,new_node.level)
            existing_node = self.gt.set_of_nodes.get(key)
            if not existing_node:
                self.gt.adding_node(new_node)
                self.gt.adding_arc(node.id,id_new)
                return new_node
            else:
                self.node_counter-=1
                if(node.id not in self.gt.set_of_arcs):
                    self.gt.set_of_arcs[node.id] = []
                if(existing_node.id not in self.gt.set_of_arcs[node.id]):
                    self.gt.adding_arc(node.id,existing_node.id)
                return existing_node
            
        
    def evaluate(self,node):

        lesscount = 0 # number of pairs in the number, that their sum of are less than 7
        equalcount = 0
        greatercount = 0
        eval = 0
        
        if node.player_turn:
            add = -1
        else:
            add = 1
        for i in range(0, len(node.string)-1):
            if int(node.string[i]) + int(node.string[i+1]) < 7:
                lesscount +=add
            elif node.string[i] + node.string[i+1] == 7:
                equalcount +=add
            else:
                greatercount +=add

        if(greatercount%2 and greatercount >1):
            eval +=add
        if(equalcount%2 and equalcount >1):
            eval +=add*1/3
        if(lesscount%2 and lesscount>1):
            eval -=add/6
        
        return (node.p2-node.p1)+eval/6
    # https://www.geeksforgeeks.org/mini-max-algorithm-in-artificial-intelligence/
    def minmax(self,node, depth, maximizing_player):
        if len(node.string)<=1 or depth == 0:
            return self.evaluate(node)
        
        if maximizing_player:
            max_eval = float("-inf")
            for move in self.get_possible_moves(node):
                eval = self.minmax(move, depth - 1, False)
                max_eval = max(max_eval, eval)

            return max_eval
        else:
            min_eval = float("inf")
            for move in self.get_possible_moves(node):
                eval = self.minmax(move, depth - 1, True)
                min_eval = min(min_eval, eval)

            return min_eval
    #https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    def alphabeta(self,node, depth, alpha, beta, maximizingPlayer):
        if len(node.string)<=1 or depth == 0:
            return self.evaluate(node)
        if maximizingPlayer:
            value = float("-inf")
            for move in self.get_possible_moves(node):
                value = max(value, self.alphabeta(move, depth - 1, alpha, beta, False))
                if value > beta:
                    break # β cutoff 
                alpha = max(alpha, value)
            return value
        else:
            value = float("inf")
            for move in self.get_possible_moves(node):
                value = min(value, self.alphabeta(move, depth - 1, alpha, beta, True))
                if value < alpha:
                    break # α cutoff 
                beta = min(beta, value)
            return value


    def printTree(self):        
        for _,x in self.gt.set_of_nodes.items():
            print(f"{x.id} {''.join(x.string)} {x.p1} {x.p2} lvl: {x.level} {x.player_turn} ")
        for x, y in self.gt.set_of_arcs.items():
            print(f"{x}, {y}") 
