import copy
import random
import math

#this is the objective function, we're looking for a minima
def simulator(final_list):
    count = 0
    cust = []
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

        if flag:
            count+=1
        else:
            cust.append(i)

    customerBool(cust)

    return test-count  #number of customers left out

def customerBool(cust):
    global customers
    customers = cust

def simulated_annealing(temp, best):
    iterations = 10
    best_eval = simulator(best)
    curr, curr_eval = best, best_eval
    for j in range(iterations):
        i = customers[random.randint(0, len(customers)-1)]
        like_list = list(like_lines[i].strip().split())
        dislike_list = list(dislike_lines[i].strip().split())
        candidate = list(set(curr + like_list))
        candidate = [item for item in candidate if item not in dislike_list]
        candidate_eval = simulator(candidate)
        if (candidate_eval<best_eval):
            best, best_eval = candidate, candidate_eval
            #print('-->%d f(%s) = %.2f' % (i, str(best), best_eval))
        diff = candidate_eval - curr_eval
        n = temp / float(j  + 1)
        try:
            prob = math.exp(-diff / n)
        except OverflowError:
            prob = float('inf')
        if diff < 0 or random.random() < prob or candidate_eval<curr_eval :
            curr, curr_eval = candidate, candidate_eval
        #print("Iteration: " + str(j) + "done")
    count = len(best)
    ans = " ".join(best)
    print(count, end = " ")
    print(ans)
    print("Score: " + str(test-best_eval))
	
test = int(input())

like = dict()
dislike = dict()

like_lines = []
dislike_lines = []

for i in range(test):

    line = input()
    like_lines.append(line[2:])
    lineArr = list(line.strip().split())

    n = int(lineArr[0])

    for ingredient in lineArr[1:]:
        if ingredient in like.keys():
            like[ingredient].append(i)
        else:
            like[ingredient] = []
            like[ingredient].append(i)

    line2 = input()
    dislike_lines.append(line2[2:])
    lineArr2 = list(line2.strip().split())

    n2 = int(lineArr2[0])

    for ingredient in lineArr2[1:]:
        if ingredient in dislike.keys():
            dislike[ingredient].append(i)
        else:
            dislike[ingredient] = []
            dislike[ingredient].append(i)

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
simulated_annealing(1, final_ingredients)