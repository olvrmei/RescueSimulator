from queue import PriorityQueue
# import queue
import random

class AlgoritmoGenetico:
    def __init__(self, graph, maxRows, maxCols, dists, victims, time, initialState):
        self.graph = graph
        # print("Graph: ", self.graph)
        self.maxRows = maxRows
        self.maxCols = maxCols
        self.dists = dists
        self.victims = victims # index, position, vital signs
        print("vitimas: ", self.victims)
        self.time = time
        self.initialState = initialState

        # Inicia parametros do algoritmo
        self.mutationC = 0.2 # 20% de chance de mutação
        self.crossoverC = 0.6 # 60% de chance de crossover
        self.popSize = len(self.victims) * 3 # Tamanho da população
        self.swap = 0.15 # 15% de chance de swap
        self.add_rm = 0.50 # 50% de chance de adicionar ou remover um gene
        self.max_it = 5 # Número máximo de iterações sem melhoria

        # Calcula o fitness
        self.fit = 1
        self.fit = self.fitness(self.victims)
        if self.fit != 0:
            self.fit = 1/self.fit
        # print("Fit: ", self.fit)

        # Cria população inicial
        self.population = []
        while len(self.population) < self.popSize:
            chromosome = self.generateChromosome()
            self.population.append(chromosome)

        # print("População inicial: ", self.population)

    def fitness(self, victims):
        # Gravidades %  [25, 50, 75, 100]
        victimsGrav = [0,0,0,0]
        for v in victims:
            sv = victims[v][1] # sinal vital da vítima
    
            gravidade = int(sv[len(sv)-1]) - 1

            victimsGrav[gravidade] += 1

        x = 0
        for i,valor in enumerate(victimsGrav):
            x += (i+1) * valor

        return x*self.fit

    def randomSampleDict(self, dict, count):
        keys = list(dict.keys())
        randomSample = random.sample(keys, count)
        newDict = {}
        for k in randomSample: 
            newDict[k] = dict[k]
        return (newDict)
    
    def randomChoiceDictKey(self, dict):
        keys = list(dict.keys())
        randomChoice = random.choice(keys)

        return randomChoice

    def crossover(self, i1, i2, newFit):
        if random.uniform(0,1) > self.crossoverC:
            if random.uniform(0,1) > 0.5:
                return self.mutation(i1)
            else:
                return self.mutation(i2)

        v1 = self.randomSampleDict(i1.victims.copy(), random.randint(0, len(i1.victims)))

        v2 = self.randomSampleDict(i2.victims.copy(), random.randint(0, len(i2.victims)))

        newVictims = v1
        for i in v2:
            exits = False
            # print("i: ", i)
            for j in newVictims:
                # print("j: ", j)
                if i == j:
                    exits = True
                else:
                    exits = False
            
            if not exits:
                newVictims[i] = v2[i]

        res = self.calculateChromosomeCost(newVictims)
        while res[0] > self.time:
            newVictims = self.randomSampleDict(newVictims, len(newVictims)-1)
            res = self.calculateChromosomeCost(newVictims)
        
        fit = self.fitness(newVictims)
        chromosome = Chromosome(newVictims, res[0], res[1], fit)
        
        return self.mutation(chromosome)

    def mutation(self, chromosome):
        if random.uniform(0,1) > self.mutationC:
            return chromosome
        newVictims = chromosome.victims.copy()

        # Swap dos genes
        if random.uniform(0,1) <= self.swap:
            newVictims = self.swapGenes(newVictims)
        
        # Adiciona ou remove mutação
        if random.uniform(0,1) <= self.add_rm:
            newVictims = self.addRemoveGene1(newVictims, 0.5)
        
        res = self.calculateChromosomeCost(newVictims)
        while res[0] > self.time:
            # Swap
            if random.uniform(0,1) <= self.swap:
                newVictims = self.swapGenes(newVictims)
            # Add ou Remove
            if random.uniform(0,1) <= self.add_rm:
                newVictims = self.addRemoveGene1(newVictims, 0.75)
            
            newVictims = self.randomSampleDict(newVictims, len(newVictims)-1)
            res = self.calculateChromosomeCost(newVictims)
        fit = self.fitness(newVictims)
        chromosome = Chromosome(newVictims, res[0], res[1], fit)
        return self.mutation(chromosome)
        
    def swapGenes(self, victims):
        # i = victims.index(random.choice(victims))
        i = self.randomChoiceDictKey(victims)
        # print("swap i: ", i)
        # j = victims.index(random.choice(victims))
        j = self.randomChoiceDictKey(victims)
        # print("swap j: ", j)
        
        newVictims = victims.copy()
        newVictims[i], newVictims[j] = newVictims[j], newVictims[i]
        return newVictims

    def addRemoveGene1(self, victims, chance):
        if random.uniform(0,1) <= chance:
            # Adiciona um gene
            randomChoice = self.randomChoiceDictKey(self.victims)
            victims[randomChoice] = self.victims[randomChoice]
            
            # victims.append(random.choice(self.victims))
        else:
            # Remove um gene
            victims.pop(self.randomChoiceDictKey(victims))
            # victims.pop(random.randint(0, len(victims)-1))
        return victims

    # def addRemoveGene(self, victims, chance):
    #     if random.uniform(0,1) <= chance:
    #         # Adiciona um gene
    #         if len(victims) == len(self.victims):
    #             return victims
    #         randomChoice = self.randomChoiceDictKey(self.victims)
    #         newVictim = random.choice(self.victims)
    #         x = [v for v in victims if v[0] == newVictim[0]]
    #         while len(x) > 0:
    #             newVictim = random.choice(self.victims)
    #             x = [v for v in victims if v[0] == newVictim[0]]
    #         newVictims = victims.copy()
    #         newVictims.append(newVictim)
    #         return newVictims
    #     else:
    #         # Remove um gene
    #         if len(victims) < 2:
    #             return victims
    #         newVictims = random.sample(victims, len(victims)-1).copy()            
    #         return newVictims

    def sortPopulation(self):
        self.population.sort(key=lambda x: x.fit, reverse=True)

    def evolution(self):
        # Seleção
        middleIndex = len(self.population) // 2
        newPop = self.population[:middleIndex]
        max_fit = newPop[0].fit

        # Enquanto a população não estiver completa
        i=0
        while len(newPop) < self.popSize:
            if i+1 < len(newPop):
                # Seleciona um índice aleatório
                j = i + random.randint(i+1, len(newPop)-1) 
                newFit = newPop[j].fit/(max_fit)

                # print("newPop[i]: ", newPop[i])
                # print("newPop[j]: ", newPop[j])

                # Crossover
                x = self.crossover(newPop[i], newPop[j], newFit)
                newPop.append(x)
            else:
                # Mutação
                x = self.mutation(newPop[i])
                newPop.append(x)

        self.population = newPop

    def generateChromosome(self):
        victims = self.victims.copy()
        flag = False
        chromosome = None
        victimsKeys = list(victims.keys())
        # print("pre shuffle: ", victimsKeys)
        random.shuffle(victimsKeys)
        # print("post shuffle: ",victimsKeys)
        while not flag:
            victims.pop(victimsKeys[len(victimsKeys)-1])
            victimsKeys.pop()
            # print("victims post pop: ", victims)
            res = self.calculateChromosomeCost(victims)
            if res[0] <= self.time:
                flag = True
                fit = self.fitness(victims)
                chromosome = Chromosome(victims, res[0], res[1], fit)
        return chromosome

    def calculateChromosomeCost(self, victims):
        cost = 0
        path = []
        prevVictim = None

        if len(victims) < 1:
            return (cost, path)
        
        for v in victims:
            v1 = victims[v]
            # print(v1[0])
            if prevVictim:
                v2 = prevVictim
                # Calcula saindo da vítima anterior para a próxima
                res = self.calculatePath(v2[0], v1[0])
                cost += res[0]
                path += res[1]
            else:
                # Calcula saindo da posição inicial até a vítima
                res = self.calculatePath((self.initialState.row, self.initialState.col), v1[0])
                cost += res[0]
                path += res[1]
            prevVictim = v1
        
        # Calcula saindo da última vítima até a posição inicial
        res = self.calculatePath(prevVictim[0], (self.initialState.row, self.initialState.col))
        cost += res[0]
        path += res[1]
        return cost, path

    def calculatePath(self, initialPos, finalPos):
        states = []
        for row in range(self.maxRows):
            cols = []
            for col in range(self.maxCols):
                cols.append(None)
            states.append(cols)
        states[0][0] = PathState(initialPos, 0, 0, None)
        stateSet = {}
        stateSet[initialPos] = states[0][0]
        stateQueue = PriorityQueue()
        stateQueue.put(states[0][0], 0)

        while not stateQueue.empty():
            state = stateQueue.get()
            # print("state: ", state)
            # print(state.pos)
            if state.pos == finalPos:
                # print(state.pos, state.parent, state.reverseAction, finalPos)
                break
            for action in self.graph[state.pos[0]][state.pos[1]]:
                nextPos = self.getNextPosition(state.pos, action)
                # custo sempre 1 pq nao se move na diagonal
                nextPosCost = state.cost + 1
                if nextPos not in stateSet or nextPosCost < stateSet[nextPos].cost:
                    if nextPos not in stateSet:
                        stateSet[nextPos] = PathState(nextPos, 0, 0, None)
                    stateSet[nextPos].cost = nextPosCost
                    stateSet[nextPos].parent = state
                    stateSet[nextPos].reverseAction = self.getReverseAction(action)
                    stateSet[nextPos].priority = nextPosCost + self.heuristic(nextPos, finalPos)
                    stateQueue.put(PathState(nextPos, stateSet[nextPos].priority, stateSet[nextPos].cost, stateSet[nextPos].parent, stateSet[nextPos].reverseAction), stateSet[nextPos].priority)
        
        # construção do caminho
        path = []
        # print("stateSet: ", stateSet)
        pathState = stateSet[finalPos]
        while pathState.parent != None and pathState.pos != initialPos:
            path.append(pathState.reverseAction)
            # print(path)
            # print(pathState.parent.pos)
            pathState = stateSet[pathState.parent.pos]
        path.reverse()
        # print(path)

        return stateSet[finalPos].cost, path, states
           
    def heuristic(self, pos1, pos2):
        return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

    def getNextPosition(self, currentPos, action):
        if action == 'N':
            return (currentPos[0]-1, currentPos[1])
        elif action == 'S':
            return (currentPos[0]+1, currentPos[1])
        elif action == 'L':
            return (currentPos[0], currentPos[1]+1)
        elif action == 'O':
            return (currentPos[0], currentPos[1]-1)

    def getReverseAction(self, action):
        if action == 'N':
            return 'S'
        elif action == 'S':
            return 'N'
        elif action == 'L':
            return 'O'
        elif action == 'O':
            return 'L'

    def validChromosome(self, chromosome):
        res = self.calculateChromosomeCost(chromosome)
        return res[0] < self.time

    def calculate(self):
        # Ordena população de acordo com o fitness
        self.sortPopulation()

        # print("sorted population: ", self.population)
        # Pega maior fitness
        biggestFit = self.population[0].fit
        # Enquanto não atingir o máximo de iterações e o fitness não for 1
        i = 0
        while i < self.max_it and biggestFit < 1: 
            self.evolution()
            self.sortPopulation()
            if self.population[0].fit > biggestFit:
                biggestFit = self.population[0].fit
                i = 0
            else:
                i += 1

    def getBestSolution(self):
        return self.population[0].path

class Chromosome:
    def __init__(self, victims, cost, path, fit):
        self.victims = victims
        self.fit = fit
        self.cost = cost
        self.path = path

    # Overload less than operator
    def __lt__(self, other):
        return self.fit < other.fit

class PathState: 
    def __init__(self, pos, priority, cost, parent, reverseAction = None):
        self.pos = pos
        self.priority = priority
        self.cost = cost
        self.parent = parent
        self.reverseAction = reverseAction

    def __lt__(self, other):
        return self.priority < other.priority