import copy
import random
import math

#this is the objective function, we're looking for a minima
def simulator(final_list):
    global customers
    customers = []
    for i in range(test):
        flag = True
        like_list = list(like_lines[i].strip().split())
        for ing in like_list:
            if ing not in final_list:
                flag = False
        dislike_list = list(dislike_lines[i].strip().split())
        for ing in dislike_list:
            if ing in final_list:
                flag = False

        if not flag:
            customers.append(i)

def isSatisfied(index, candidate):
    like_list = like_lines[index].strip().split()
    dislike_list = dislike_lines[index].strip().split()
    for ing in like_list:
        if ing not in candidate:
            return False
    for ing in dislike_list:
        if ing in candidate:
            return False
    return True

def objective(index, candidate):
    global customers
    like_list = like_lines[index].strip().split()
    dislike_list = dislike_lines[index].strip().split()
    customers.remove(index)
    for ing in like_list:
        if ing in dislike.keys():
            for i in dislike[ing]:
                if i not in customers:
                    #print(str(i) + " not satisfied because " + ing + " is present")
                    customers.append(i)
                
        for i in like[ing]:
            if i in customers:
                if isSatisfied(i, candidate):
                    #print(str(i) + " is satisfied")
                    customers.remove(i)

    for ing in dislike_list:
        if ing in like.keys():
            for i in like[ing]:
                if i not in customers:
                    #print(str(i) + " not satisfied because " + ing + " is present")
                    customers.append(i)

        for i in dislike[ing]:
            if i in customers:
                if isSatisfied(i, candidate):
                    #print(str(i) + " is satisfied ")
                    customers.remove(i)
    
    customers = list(set(customers))

def simulated_annealing(temp, best):
    global customers
    iterations = 1000
    simulator(best)
    best_eval = len(customers)
    print("Through simulator: " + str(test - best_eval))
    curr, curr_eval = best, best_eval
    for j in range(iterations):
        i = customers[random.randint(0, len(customers)-1)]
        like_list = list(like_lines[i].strip().split())
        dislike_list = list(dislike_lines[i].strip().split())
        candidate = list(set(curr + like_list))
        candidate = [item for item in candidate if item not in dislike_list]
        objective(i, candidate)
        candidate_eval = len(customers)
        if (candidate_eval<best_eval):
            best, best_eval = candidate, candidate_eval
            score = test - best_eval
            print('-->%d = %.2f' % (j, score))
        diff = candidate_eval - curr_eval
        n = temp / float(j + 1)
        try:
            prob = math.exp(-diff / n)
        except OverflowError:
            prob = float('inf')
        if diff < 0 or random.random() < prob or candidate_eval<curr_eval :
            curr, curr_eval = candidate, candidate_eval
    count = len(best)
    print(count, end = " ")
    for ing in best:
        print(ing, end= " ")
    print("Score: " + str(test-best_eval))
    simulator(best)
    print("through sim: " + str(test - len(customers)))
    print("best eval: " + str(test - best_eval))
	
file1 = open("C:\\Users\\tarun\\Downloads\\hashcode\\hashcode-22\\d.txt", "r")
lines = []
for line in file1:
    lines.append(line)

file1.close()

test = int(lines[0][:-1])
like = dict()
dislike = dict()

like_lines = []
dislike_lines = []

j = 1
for i  in range(test):

    line = lines[j][:-1]
    like_lines.append(line[2:])
    lineArr = list(line.strip().split())

    n = int(lineArr[0])

    for ingredient in lineArr[1:]:
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
        if dislike.get(ingredient):
            dislike[ingredient].append(i)
        else:
            dislike[ingredient] = [i]

    j += 1
# print(like)
# print(dislike)

score = dict()

for key in like:
    score[key] = len(like[key])

for key in dislike:
    if (score.get(key)):
        score[key] -= len(dislike[key])
    else:
        score[key] = -1 * len(dislike[key])

ans = ""
count = 0

for key in score:
    if score[key] > 0:
        ans += key
        ans += " "
        count += 1

final_ingredients = list(ans.strip().split())
customers = []
simulated_annealing(10, final_ingredients)
#simulator(final_ingredients)
#print("Score: " + str(test - len(customers)))