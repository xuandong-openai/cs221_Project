def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = scoreEvaluationFunction
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        def recurse(state, index, depth):
            # check if it's the terminal state
            if state.isWin() or state.isLose() or len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP
            
            nextIndex = 0 if index == state.getNumAgents() - 1 else index + 1
            nextDepth = depth - 1 if nextIndex == state.getNumAgents() - 1 else depth
            # compute the recursion
            legalActions = state.getLegalActions(index)
            if Directions.STOP in legalActions and len(legalActions) > 1:
                legalActions.remove(Directions.STOP)
            choices = []
            for legalAction in legalActions:
                choices.append((recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth)[0], legalAction))
            # return max value if it's agent otherwise min if it's opponent
            return max(choices) if index == 0 else min(choices)
        
        value, action = recurse(gameState, self.index, self.depth)
        return action
