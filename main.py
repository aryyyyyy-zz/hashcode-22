# genetic algorithm search of the one max optimization problem
from itertools import repeat

from numpy.random import randint
from numpy.random import rand

file1 = open("e_elaborate.in.txt", "r")
lines = []
for line in file1:
    lines.append(line)

file1.close()

test = int(lines[0][:-1])
like = dict()
dislike = dict()
IngredientToIndex = dict()
IndexToIngredient = dict()
ingredientIndex = 0

like_lines = []
dislike_lines = []

j = 1
for i in range(test):

    line = lines[j][:-1]
    like_lines.append(line[2:])
    lineArr = list(line.strip().split())

    n = int(lineArr[0])

    for ingredient in lineArr[1:]:
        if ingredient not in IngredientToIndex.keys():
            IngredientToIndex[ingredient] = ingredientIndex
            IndexToIngredient[ingredientIndex] = ingredient
            ingredientIndex += 1
        if like.get(ingredient):
            like[ingredient].append(i)
        else:
            like[ingredient] = [i]

    j += 1
    line2 = lines[j][:-1]
    dislike_lines.append(line2[2:])
    lineArr2 = list(line2.strip().split())

    n2 = int(lineArr2[0])

    for ingredient in lineArr2[1:]:
        if ingredient not in IngredientToIndex.keys():
            IngredientToIndex[ingredient] = ingredientIndex
            IndexToIngredient[ingredientIndex] = ingredient
            ingredientIndex += 1
        if dislike.get(ingredient):
            dislike[ingredient].append(i)
        else:
            dislike[ingredient] = [i]

    j += 1

print("like is:")
print(like)                 # ingredient: list of people who like it
print("******************************************************************************************************************************")
print("dislike is:")            # ingredient: list of people who dislike it
print(dislike)
print("******************************************************************************************************************************")
print("like lines is")              # list of list of liked ingredients of customers
print(like_lines)
print("******************************************************************************************************************************")
print("dislike lines is")                # list of list of liked ingredients of customers
print(dislike_lines)
print("******************************************************************************************************************************")
print("all ingredients dict is")            # Ingredient: index
print(IngredientToIndex)
print("******************************************************************************************************************************")
print(IndexToIngredient)                # Index: ingredient
print("******************************************************************************************************************************")
print(len(IndexToIngredient))


# objective function
def onemax(x):
    # return sum(x)
    satisfied_customers = list(repeat(1, test))

    for i in range(len(x)):
        if x[i] == 1 and IndexToIngredient[i] in dislike.keys():
            for cust in dislike[IndexToIngredient[i]]:
                satisfied_customers[cust] = 0

    for i in range(len(like_lines)):
        tempIngredientsList = list(like_lines[i].split())
        for j in tempIngredientsList:
            if x[IngredientToIndex[j]] == 0:
                satisfied_customers[i] = 0

    return sum(satisfied_customers)


# tournament selection
def selection(pop, scores, k=3):
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k - 1):
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def crossover(p1, p2, r_cross):
    c1, c2 = p1.copy(), p2.copy()
    if rand() < r_cross:
        pt = randint(1, len(p1) - 2)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]


# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        if rand() < r_mut:
            bitstring[i] = 1 - bitstring[i]


# genetic algorithm
def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
    pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
    best, best_eval = 0, objective(pop[0])
    for gen in range(n_iter):
        scores = [objective(c) for c in pop]
        for i in range(n_pop):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
        selected = [selection(pop, scores) for _ in range(n_pop)]
        children = list()
        for i in range(0, n_pop, 2):
            p1, p2 = selected[i], selected[i + 1]
            for c in crossover(p1, p2, r_cross):
                mutation(c, r_mut)
                children.append(c)
        pop = children
    return [best, best_eval]


n_iter = 700
n_bits = 10000
n_pop = 100
r_cross = 0.9
r_mut = 1.0 / float(n_bits)
best, score = genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)
print('Done!')
print('f(%s) = %f' % (best, score))

ans = [sum(best)]
for i in range(len(best)):
    if best[i] == 1:
        ans.append(IndexToIngredient[i])
print(*ans)
