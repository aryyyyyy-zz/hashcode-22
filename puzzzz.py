import copy
import random
import math

#this is the objective function, we're looking for a minima
def simulator(final_list):
    count = 0
    cust = []
    for i in range(t):
        flag = True
        like_list = list(like_lines[i].strip().split())
        for ing in like_list:
            if ing not in final_list:
                flag = False
        dislike_list = list(dislike_lines[i].strip().split())
        for ing in dislike_list:
            if ing in final_list:
                flag = False

        if flag:
            count+=1

        cust.append(flag)

    customerBool(cust)

    return t-count  #number of customers left out

def customerBool(cust):
    global customers
    customers = cust

def simulated_annealing(temp, best):
    iterations = 20
    best_eval = simulator(best)
    curr, curr_eval = best, best_eval
    for j in range(iterations):
        for i in range(t):  
            like_list = list(like_lines[i].strip().split())
            dislike_list = list(dislike_lines[i].strip().split())
            if not customers[i]:
                candidate = list(set(curr + like_list))
                candidate = [item for item in candidate if item not in dislike_list]
                candidate_eval = simulator(candidate)
                if (candidate_eval<best_eval):
                    best, best_eval = candidate, candidate_eval
                    #print('>%d f(%s) = %.2f' % (i, str(best), best_eval))
                diff = candidate_eval - curr_eval
                n = temp / float(j + i + 1)
                prob = math.exp(-diff / n)
                if diff < 0 or random.random() < prob:
                    curr, curr_eval = candidate, candidate_eval
    count = len(best)
    ans = " ".join(best)
    print(count, end = " ")
    print(ans)
    #print("Score: " + str(best_eval))
	
t = int(input())

like = dict()
dislike = dict()

like_lines = []
dislike_lines = []

for i in range(t):

    line = input()
    like_lines.append(line[2:])
    lineArr = list(line.strip().split())

    n = int(lineArr[0])

    for i in range(n):
        ingredient = lineArr[i + 1]

        if like.get(ingredient):
            like[ingredient] += 1
        else:
            like[ingredient] = 1

    line2 = input()
    dislike_lines.append(line2[2:])
    lineArr2 = list(line2.strip().split())

    n2 = int(lineArr2[0])

    for i in range(n2):
        ingredient = lineArr2[i + 1]

        if dislike.get(ingredient):
            dislike[ingredient] += 1
        else:
            dislike[ingredient] = 1

# print(like)
# print(dislike)

score = dict()

for key in like:
    score[key] = like[key]

for key in dislike:
    if (score.get(key)):
        score[key] -= dislike[key]
    else:
        score[key] = -1 * dislike[key]

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