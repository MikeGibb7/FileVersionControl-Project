import sys
from simhash import Simhash #python-Simhash; might be 128-bit?? [add dependency] 
import copy

#REMINDER: REFACTOR ALL INSTANCES OF LEVENSHTEIN AT SOME POINT


#LHDiff paper: https://www.cs.usask.ca/~croy/papers/2013/LHDiffFullPaper-preprint.pdf
#very useful paper: http://www.xmailserver.org/diff2.pdf

#PREPROCESSING: return each file as a list of normalized lines
def normalize(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()

        normalized_lines = []
        for line in lines:
            cleaned = " ".join(line.split())
            normalized = cleaned.lower().strip()
            normalized_lines.append(normalized)
        return normalized_lines #lowercase, padding removed, redundant internal whitespace removed
    #empty lines are NOT discarded

#Operations
MATCH = 'M'
ADD = 'A'
DELETE = 'D'
CHANGE = 'C'

#standard levenshtein function (should factorize out UnixDiff segment later)
def normalLevenshtein(s1, s2): 
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)] #DP TABLE

    #Initialization of table
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1, #DELETE
                dp[i][j - 1] + 1, #ADD
                dp[i - 1][j - 1] + cost #CHANGE
            )
    return dp[m][n] / max(len(s1), len(s2))


if __name__ == '__main__':
    program = sys.argv[0] #CLI implementation | IMPORTANT: REPLACE WITH GUI 
    if len(sys.argv) < 3:
        print(f"Command: program <file1> <file2>")
        print(f"ERROR: Invalid arg count: 2 files required")
        exit(1)
    
    #store files as line arrays
    file1 = normalize(sys.argv[1])
    file2 = normalize(sys.argv[2])
    f1 = len(file1)
    f2 = len(file2)

    distances = []
    actions = []

    #TABLE CONSTRUCTION (AND INITIALIZATION)
    for i in range(f1 + 1):
        distances.append([0] * (f2 + 1))
        actions.append(['-'] * (f2 + 1))

    distances[0][0] = 0 #table's top-left entry is "empty" (we'll be iterating through 1 to n instead of 0 to n - 1)
    actions [0][0] = MATCH
   
    #x, y axis setup - horizontal is adding, vertical is deleting
    for n1 in range(1, f1 + 1):
        distances[n1][0] = n1
        actions[n1][0] = DELETE

    for n2 in range(1, f2 + 1):
        distances[0][n2] = n2
        actions[0][n2] = ADD

    #TRAVERSAL    
    #fill in table based of matches or "cheapest" operation
    for n1 in range(1, f1 + 1):
        for n2 in range(1, f2 + 1):
            if file1[n1 - 1] == file2[n2 - 1]:
                distances[n1][n2] = distances[n1 - 1][n2 - 1]
                actions[n1][n2] = MATCH
            else:
                delete = (distances[n1 - 1][n2] + 1, DELETE)
                add = (distances[n1][n2 - 1] + 1, ADD)
                change = (distances[n1 - 1][n2 - 1] + 2, CHANGE) #substitution == delete + insert (cost of 2) | DIAGONAL movement in table

                distances[n1][n2], actions[n1][n2] = min([delete, add, change], key=lambda x: x[0]) #traverse by assigned numeric value
    
    #BACKTRACE
    #edits = [] #list of differences
    leftList = []
    rightList = []
    mappings = [] #1-to-1s
    n1 = f1
    n2 = f2
    while n1 > 0 or n2 > 0:
        action = actions[n1][n2]

        #take most efficient route back to top-left of table, recording mappings and edits along the way
        if action == MATCH:
            if file1[n1 - 1] != "" or file2[n2 - 1] != "": #multiple empty string checks to omit them from being mapped
                mappings.append((n1, n2))
            n1 -= 1
            n2 -= 1 
        elif action == ADD:
            #edits.append((ADD, n2, file2[n2 - 1]))
            if file2[n2 - 1] != "":
                rightList.append((n2, file2[n2 - 1]))
            n2 -= 1
        elif action == DELETE:
            #edits.append((DELETE, n1, file1[n1 - 1]))
            if file1[n1 - 1] != "":
                leftList.append((n1, file1[n1 - 1]))
            n1 -= 1
        elif action == CHANGE:
            #edits.append((CHANGE, n1, file1[n1 - 1], file2[n2 - 1]))
            n1 -= 1
            n2 -= 1
        else: 
            assert False, "unreachable" #fail state
    
    #edits.reverse()
    leftList.reverse()
    rightList.reverse()
    mappings.reverse()

    #DELETE
    '''for e in edits: #diagnostic 
        print(e)'''
    
    '''print("LEFT")
    for l in leftList:
        print(l)

    print("RIGHT")
    for r in rightList:
        print(r)'''

    print(mappings) #test output
    #known behaviour: EMPTY LINES ARE IGNORED, NOT REMOVED 

    #MAKING CANDIDATE LISTS
    hashLeft = []
    hashRight = []
    #convert lines to corresponding hashes
    for i in range(len(leftList)):
        hashLeft.append((leftList[i][0], Simhash(leftList[i][1])))

    for j in range(len(rightList)):
        hashRight.append((rightList[j][0], Simhash(rightList[j][1])))
        #print(f"{hashRight[j]} and {hashRight[j][1].value}") #DELETE

    K = 15 #simhash comparison "constant"

    candidates = []
    for i in range(len(hashLeft)): #compare all lines of left with all lines of right
        bestHashes = []
        for j in range(len(hashRight)):
            a = hashLeft[i][1].value
            b = hashRight[j][1].value
            hammingDistance = bin(a ^ b).count('1') #bit count on XOR of the two hashes
            if len(bestHashes) > K: 
                bestHashes.sort(key=lambda x: x[2]) #sort by simhash score
                if hammingDistance < bestHashes[len(bestHashes) - 1][2]: #if better than worst match 
                    bestHashes.append([hashLeft[i][0], hashRight[j][0], hammingDistance]) #lines + hash similarity
            else:
                bestHashes.append([hashLeft[i][0], hashRight[j][0], hammingDistance])
        
        bestHashes.sort(key=lambda x: x[2]) #final sort
        candidates.append(copy.deepcopy(bestHashes)) #update candidate list

    candidates.sort(key=lambda x: x[0]) 
    #print(candidates) 
    #print(len(candidates))

    #CONTENT SIMILARITY SCORE
    leftMappings = len(candidates) #candidate mappings are grouped into subarrays based on left list lines | this is the number of those subarrays
    for i in range(leftMappings):
        for j in range(len(candidates[i])):
            contentSim = normalLevenshtein(file1[candidates[i][j][0] - 1], file2[candidates[i][j][1] - 1])
            candidates[i][j][2] = contentSim #OVERWRITE SIMHASH HAMMING DISTANCE WITH CONTENT SIMILARITY
            #print(f"{file1[candidates[i][j][0] - 1]} AND {file2[candidates[i][j][1] - 1]} EQUALS {contentSim}")
            