import random
import math

def generateRandomPopulation(populationSize, geneLength):
    population = []
    choices = ['0','1']
    
    for i in range(populationSize):
        s = ""
        for j in range(geneLength):
            s += random.choice(choices)
        population.append(s)
    return population

def calculateFitness(gene):
    satisfiedCustomers = {}
    dissatisfiedCustomers = set()

    for i in range(len(gene)):
        if (gene[i] == '1'):
            ingredient = LIST_OF_INGREDIENTS[i]
            if (INGREDIENT_LIKES.get(ingredient)):
                for person in INGREDIENT_LIKES[ingredient]:
                    if satisfiedCustomers.get(person):
                        satisfiedCustomers[person] += 1
                    else:
                        satisfiedCustomers[person] = 1
            if INGREDIENT_DISLIKES.get(ingredient):
                for person in INGREDIENT_DISLIKES[ingredient]:
                    dissatisfiedCustomers.add(person)
    
    for person in dissatisfiedCustomers:
        if satisfiedCustomers.get(person):
            satisfiedCustomers.pop(person)

    numOfSatisfiedCustomers = 0

    for key in satisfiedCustomers.keys():
        if satisfiedCustomers[key] >= len(PEOPLE_LIKES[key]):
            numOfSatisfiedCustomers += 1
    
    return numOfSatisfiedCustomers
    
def getInput():
    #inputFile = open('C:\\Users\\ACER\\Desktop\\code\\hashcode\\c_coarse.in.txt', 'r')
    inputFile = open('C:\\Users\\ACER\\Desktop\\code\\hashcode\\d_difficult.in.txt', 'r')
    NUMBER_OF_CUSTOMERS = int(inputFile.readline())
    # getting in put from file
    for i in range(NUMBER_OF_CUSTOMERS * 2):
        LIKE_LINES_LIST.append(inputFile.readline()[:-1])
        DISLIKE_LINES_LIST.append(inputFile.readline()[:-1])
    inputFile.close()

def extractDataFromInput():
    i = 0
    for line in LIKE_LINES_LIST:
        if len(line) == 0:
            continue
        lineList = list(line.split())
        
        n = int(lineList[0])

        for j in range(n):
            if (PEOPLE_LIKES.get(i)):
                PEOPLE_LIKES[i].append(lineList[j+1])
            else:
                PEOPLE_LIKES[i] = [lineList[j+1]]

            if INGREDIENT_LIKES.get(lineList[j+1]):
                INGREDIENT_LIKES[lineList[j+1]].append(i)
            else:
                INGREDIENT_LIKES[lineList[j+1]] = [i]
        i += 1

    # sets up dislikes dictionaries
    i = 0
    for line in DISLIKE_LINES_LIST:
        if len(line) == 0:
            continue
        lineList = list(line.split())
        
        n = int(lineList[0])

        for j in range(n):
            if (PEOPLE_DISLIKES.get(i)):
                PEOPLE_DISLIKES[i].append(lineList[j+1])
            else:
                PEOPLE_DISLIKES[i] = [lineList[j+1]]

            if INGREDIENT_DISLIKES.get(lineList[j+1]):
                INGREDIENT_DISLIKES[lineList[j+1]].append(i)
            else:
                INGREDIENT_DISLIKES[lineList[j+1]] = [i]
        i += 1

def crossover(gene0, gene1):
    if (random.random() > 0.5):
        return (gene0[:math.floor(len(gene0)/2)] + gene1[math.floor(len(gene0)/2):])
    else:
        return (gene1[:math.floor(len(gene0)/2)] + gene0[math.floor(len(gene0)/2):])

def naturalSelection():
    fitnessList = []
    nextGeneration = []
    GENE_POOL_SIZE  = len(population)
    fittest = 0
    fittestIndex = 0 
    totalFitness = 0
    genePool = []
    
    ii = 0
    for member in population:
        fitness = calculateFitness(member)
        fitnessList.append(fitness)
        if fitness > fittest:
            fittest = fitness
            fittestIndex = ii
        totalFitness += fitness
        ii += 1

    for i in range(len(population)):
        x = math.floor(max(fitnessList[i]/totalFitness * GENE_POOL_SIZE, 1)) # can be improved maybe, discuss with others
        for k in range(x):
            genePool.append(i)
    
    for i in range(len(population) - 1):
        nextGeneration.append(crossover(population[random.choice(genePool)], population[random.choice(genePool)]))

    for gene in nextGeneration:
        mutate(gene)

    nextGeneration.append(population[fittestIndex]) # adding the current best solution to next gen
    global bestSolution
    bestSolution = population[fittestIndex][:]
    print("best solution: " + bestSolution + " of Gen " + str(currentGen) + " ; fitness = " + str(fittest))
    #print(bestSolution)

    return nextGeneration

def mutate(gene):
    if (random.random() < 0.001):
        randomInt = math.floor(random.random() * len(gene))
        if gene[randomInt] == '0':
            gene = gene[:randomInt] + '1' + gene[randomInt + 1: ]
        else:
            gene = gene[:randomInt] + '0' + gene[randomInt + 1: ]

#******************************************************************************************************
#---------------------------------- Program starts here ------------------------------------------------
#******************************************************************************************************

# these are constant variables, they are initialised once in the functions above and NEVER modified
LIKE_LINES_LIST = []
DISLIKE_LINES_LIST = []
NUMBER_OF_CUSTOMERS = 0 # tentative
INGREDIENT_DISLIKES = {} # key = ingredient strind, value = list of people who like it
INGREDIENT_LIKES = {}    # same as above for dislike
PEOPLE_LIKES = {}        # key = people int, value = list of ingredients they like
PEOPLE_DISLIKES = {}     # same as above for dislike

getInput()
extractDataFromInput()

LIST_OF_INGREDIENTS = list(set(list(INGREDIENT_DISLIKES.keys()) + list(INGREDIENT_LIKES.keys())))
LIST_OF_INGREDIENTS.sort()
NUM_OF_INGREDIENTS = len(LIST_OF_INGREDIENTS)


NUM_OF_GENERATIONS = 30
currentGen = 0

bestSolution = ""

population = generateRandomPopulation(10000, NUM_OF_INGREDIENTS)


for i in range(NUM_OF_GENERATIONS):
    population = naturalSelection()
    currentGen += 1
    
print(bestSolution)
print(calculateFitness(bestSolution))

# print(LIST_OF_INGREDIENTS)
# print(calculateFitness('1111001111'))
# print(crossover('11111', '00000'))

# tfeej vxglq byyii akuof luncl xdozp dlust xveqd