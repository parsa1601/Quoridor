from Player import Player


class MiniMaxPlayer(Player):
    MAX_DEPTH = 2
    INFINITY = 9999
    bestAction = None

    """ The written BFS that has been created before"""

    def bfs(self, opponent: Player):
        for player in [self, opponent]:
            destination = (
                self.board.get_white_goal_pieces()

                if player.color == "white"
                else self.board.get_black_goal_pieces()
            )

            visited = {}
            distances = {}

            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for i in self.board.get_piece_neighbors(piece):
                    if visited[i] == False:
                        distances[i] = distances[piece] + 1
                        visited[i] = True
                        queue.append(i)

            min_distance = self.INFINITY

            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance

        return self_distance, opponent_distance

    """ This is a new evaluation function which scores based on enemy's distance from finish line! """

    def minimax_evaluator(self, opponent):
        """ by trying different ways and algorithm, following evaluation was my best possible one!
            until the enemy reaches the middle of the map, the agent acts offensivly
            but when enemy passes the mid, agent's mind changed into deffensive and its periority becomes putting walls
            but the agent checks if its putting walls too much and the opponent has more walls, if that happens, the agent
            decides to moves until the wall_count's difference decreases!
        """
        self_distance, opponent_distance = self.bfs(opponent)
        # print("self color" + self.color)
        # print("opponent color" + opponent.color)
        # danger = False
        # if opponent.y == 5:
        #     danger = True
        if self.color == "white":
            if opponent.y < 5:
                total_score = (0.3*opponent_distance - 0.8*self_distance)
            else:
                total_score = (0.7 * opponent_distance - 0.3*self_distance) * (1 + abs(self.walls_count-opponent.walls_count) / 2)
        if self.color == "black":
            if opponent.y > 4:
                total_score = (0.3 * opponent_distance - 0.8 * self_distance)
            else:
                if self.walls_count - opponent.walls_count > 1:
                    total_score = (0.7 * opponent_distance - 0.3*self_distance) * (1 + abs(self.walls_count - opponent.walls_count) / 2)
                else:
                    total_score = (0.3 * opponent_distance - 0.8 * self_distance)
        return total_score

    """ MINIMAX function as it looks like!!! ':) """

    def minimax(self, opponent: Player, max_player, action_list, alpha, beta, current_depth):

        """ for each max/min player we do following actions:
            I. set value as alpha/beta
            II. get legal action of that player from legal_actions function in Player class
            III. call minimax function again and change player (max/min ---> min/max)
            IV. since we need our actions only as a simulation for calculating min/max scores, so we should undo them
            V. by calling pruning function we prune our graph based on alpha/beta and current value
            VI. after all of these, our minimax function returns max/min of our values (max_value is a representation of
            previous values and we compare it with current value)
            VII. function should return current state when we are in cutoff (the base condition of a recursive function)
        """
        if self.is_winner():
            return self.MAX_DEPTH - current_depth

        if current_depth == 0:
            return self.minimax_evaluator(opponent)

        if max_player:
            max_value = -self.INFINITY

            max_legal_acts = self.get_legal_actions(opponent)
            for act in max_legal_acts:
                self.play(act, is_evaluating=True)

                current_value = self.minimax(opponent, False, action_list, alpha, beta, current_depth - 1)

                self.undo_last_action()

                if current_value > max_value:
                    self.bestAction = act

                max_value = max(current_value, max_value)

                if self.pruning(False, alpha, beta, current_value):
                    break

            return max_value

        else:
            min_value = self.INFINITY

            min_legal_acts = opponent.get_legal_actions(self)
            for act in min_legal_acts:
                opponent.play(act, is_evaluating=True)

                current_value = self.minimax(opponent, True, action_list, alpha, beta, current_depth - 1)

                opponent.undo_last_action()

                min_value = min(current_value, min_value)

                if self.pruning(True, alpha, beta, current_value):
                    break

            return min_value

    def minimax_decider(self, opponent):

        """ when we call this function in main class this function, first of all creates an array for actions,
        then calls minimax and waits for its final output, stores it as a best action
        """

        action_list = {}

        action_value = self.minimax(opponent, True, action_list, -self.INFINITY, self.INFINITY, self.MAX_DEPTH)
        print(action_value)
        print("Best Actions ", self.bestAction)

        return self.bestAction

    def pruning(self, max_player, alpha, beta, current_value):

        """ the alpha beta pruning happens here,
         its simple 3 line function and i don't see any need to describe ':)
        """
        if max_player:
            alpha = max(alpha, current_value)

        else:
            beta = min(beta, current_value)

        if beta <= alpha:
            return True
