import sys
import copy
import string
import math
from simhash import Simhash # python-Simhash; might be 128-bit?? [add dependency] 
import heapq

# REMINDER: TRY TO REFACTOR ALL INSTANCES OF LEVENSHTEIN AT SOME POINT

# LHDiff paper: https://www.cs.usask.ca/~croy/papers/2013/LHDiffFullPaper-preprint.pdf
# very useful paper: http://www.xmailserver.org/diff2.pdf

# PREPROCESSING: return each file as a list of normalized lines
def normalize(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()

        normalizedLines = []
        for line in lines:
            cleaned = " ".join(line.split())
            normalized = cleaned.lower().strip()
            normalizedLines.append(normalized)
        return normalizedLines # lowercase, padding removed, redundant internal whitespace removed
    # empty lines are NOT discarded (preserved for line numbering, but practically ignored)

# Operations
MATCH = 'M'
ADD = 'A'
DELETE = 'D'
CHANGE = 'C'

# standard levenshtein function (should factorize out UnixDiff segment later)
def normalLevenshtein(s1, s2): 
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)] # DP TABLE

    # Initialization of table
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1, # DELETE
                dp[i][j - 1] + 1, # ADD
                dp[i - 1][j - 1] + cost # CHANGE
            )
    return dp[m][n] / max(len(s1), len(s2))

# frequency vector construction
def charFrequency(text):
    freq = {char: 0 for char in string.ascii_lowercase} # frequency vector as dictionary
    for char in text:
        if char in freq:
            freq[char] += 1
    return freq

# CONTEXT SCORE = (A DOT B) / (VLEN(A)VLEN(B))
# character based approach in accordance with LHDiff paper (no tokenization)
def cosineSimilarity(s1, s2):
    # make vectors
    freq1 = charFrequency(s1)
    freq2 = charFrequency(s2)

    dotProduct = sum(freq1[char] * freq2[char] for char in string.ascii_lowercase)
    vlen1 = math.sqrt(sum(freq1[char] ** 2 for char in string.ascii_lowercase))
    vlen2 = math.sqrt(sum(freq2[char] ** 2 for char in string.ascii_lowercase))

    if vlen1 == 0 or vlen2 == 0:
        return 0.0
    
    return dotProduct / (vlen1 * vlen2)



if __name__ == '__main__':
    program = sys.argv[0] # CLI implementation | IMPORTANT: REPLACE WITH GUI 
    if len(sys.argv) < 3:
        print(f"Command: program <file1> <file2>")
        print(f"ERROR: Invalid arg count: 2 files required")
        exit(1)
    
    # store files as line arrays
    file1 = normalize(sys.argv[1])
    file2 = normalize(sys.argv[2])
    f1 = len(file1)
    f2 = len(file2)

    distances = []
    actions = []

    # TABLE CONSTRUCTION (AND INITIALIZATION)
    for i in range(f1 + 1):
        distances.append([0] * (f2 + 1))
        actions.append(['-'] * (f2 + 1))

    distances[0][0] = 0 # table's top-left entry is "empty" (we'll be iterating through 1 to n instead of 0 to n - 1)
    actions [0][0] = MATCH
   
    # x, y axis setup - horizontal is adding, vertical is deleting
    for n1 in range(1, f1 + 1):
        distances[n1][0] = n1
        actions[n1][0] = DELETE

    for n2 in range(1, f2 + 1):
        distances[0][n2] = n2
        actions[0][n2] = ADD

    # TRAVERSAL    
    # fill in table based of matches or "cheapest" operation
    for n1 in range(1, f1 + 1):
        for n2 in range(1, f2 + 1):
            if file1[n1 - 1] == file2[n2 - 1]:
                distances[n1][n2] = distances[n1 - 1][n2 - 1]
                actions[n1][n2] = MATCH
            else:
                delete = (distances[n1 - 1][n2] + 1, DELETE)
                add = (distances[n1][n2 - 1] + 1, ADD)
                change = (distances[n1 - 1][n2 - 1] + 2, CHANGE) # substitution == delete + insert (cost of 2) | DIAGONAL movement in table

                distances[n1][n2], actions[n1][n2] = min([delete, add, change], key=lambda x: x[0]) # traverse by assigned numeric value
    
    # BACKTRACE
    leftList = []
    rightList = []
    mappings = [] # 1-to-1s
    n1 = f1
    n2 = f2
    while n1 > 0 or n2 > 0:
        action = actions[n1][n2]

        # take most efficient route back to top-left of table, recording mappings and edits along the way
        if action == MATCH:
            if file1[n1 - 1] != "" or file2[n2 - 1] != "": # multiple empty string checks to omit them from being mapped
                mappings.append((n1, n2))
            n1 -= 1
            n2 -= 1 
        elif action == ADD:
            if file2[n2 - 1] != "":
                rightList.append((n2, file2[n2 - 1]))
            n2 -= 1
        elif action == DELETE:
            if file1[n1 - 1] != "":
                leftList.append((n1, file1[n1 - 1]))
            n1 -= 1
        elif action == CHANGE:
            n1 -= 1
            n2 -= 1
        else: 
            assert False, "unreachable" # fail state
    
    leftList.reverse()
    rightList.reverse()
    mappings.reverse()

    # MAKING CANDIDATE LISTS (streamed, keep top-K per left line to save memory)
    # create Simhash tuples for unmapped lines
    hashLeft = [(ln, Simhash(text)) for ln, text in leftList]
    hashRight = [(ln, Simhash(text)) for ln, text in rightList]
    
    K = 15 # simhash comparison "constant"

    finalCandidates = []
    # For each left-line, stream over right-lines and keep K best by hamming distance using heapq.nsmallest
    for left_ln, left_hash in hashLeft:
        pairs_iter = ((left_ln, right_ln, bin(left_hash.value ^ right_hash.value).count('1'))
                      for right_ln, right_hash in hashRight)
        best_hashes = heapq.nsmallest(K, pairs_iter, key=lambda x: x[2])

        # compute combined similarity immediately for the kept candidates (avoid storing huge candidate matrix)
        for leftLine, rightLine, _sim in best_hashes:
            # CONTENT SIMILARITY SCORE
            contentSim = 1 - normalLevenshtein(file1[leftLine - 1], file2[rightLine - 1])
            score = 0.6 * contentSim

            # CONTEXT SIMILARITY SCORE (build context strings using generator + join to be slightly lighter)
            leftContextInterval = range(max(leftLine - 4, 1), min(leftLine + 4, f1) + 1)
            rightContextInterval = range(max(rightLine - 4, 1), min(rightLine + 4, f2) + 1)
            leftContext = "\n".join(file1[n - 1] for n in leftContextInterval if file1[n - 1] != "")
            rightContext = "\n".join(file2[m - 1] for m in rightContextInterval if file2[m - 1] != "")
            
            contextSim = cosineSimilarity(leftContext, rightContext)
            score += 0.4 * contextSim

            if score > 0.45:
                finalCandidates.append([leftLine, rightLine, score])

    #SELECT BEST MAPPINGS (INJECTIVE A -> B with no repeats or overlapping)
    finalCandidates.sort(reverse=True, key=lambda x: x[2]) #IMPORTANT TO SORT THE CANDIDATES IN DESCENDING ORDER
    f = 0
    while f < len(finalCandidates):
        finalCandidates = [map for map in finalCandidates if not (finalCandidates.index(map) != f and map[0] == finalCandidates[f][0])] #removes inferior left to right mappings
        finalCandidates = [map for map in finalCandidates if not (finalCandidates.index(map) != f and finalCandidates[f][1] == map[1])] #removes mappings to same line on right
        f += 1

    for m in range(len(finalCandidates)):
        mappings.append((finalCandidates[m][0], finalCandidates[m][1]))

    # REMOVE NEWLY MAPPED LINES from candidate lists
    l = 0 
    while l < len(leftList):
        for c in range(len(finalCandidates)):
            if leftList[l][0] == finalCandidates[c][0]:
                leftList.pop(l)
                l -= 1
                break
        l += 1

    r = 0
    while r < len(rightList):
        for c in range(len(finalCandidates)):
            if rightList[r][0] == finalCandidates[c][1]:
                rightList.pop(r)
                r -= 1
                break
        r += 1

    #REMOVE NON-CONSECUTIVE RIGHT LIST LINES (Not eligible for line split detection)
    r = 0
    while r < len(rightList):
        current = rightList[r][0]
        hasLeftNeighbour = r > 0 and rightList[r - 1][0] == current - 1
        hasRightNeighbour = r < len(rightList) - 1 and rightList[r + 1][0] == current + 1
        if not (hasLeftNeighbour or hasRightNeighbour):
            rightList.pop(r)
        else:
            r += 1

    # NEXT: LINE SPLIT DETECTION
    # admittedly kind of a mess (most convoluted section): trying to iterate through the unmapped lines from right list, their concatenations
    maxLineSplitSim = 0
    if leftList:
        for l in leftList:
            lineSplitsRight = []
            for i in range(len(rightList) - 1):
                maxLineSplitSim = 0
                concatenate = rightList[i][1]
                hasRightNeighbour = rightList[i][0] == rightList[i+1][0] - 1    
                subLineSplits = [rightList[i][0]]
                for j in range(1, min(8, len(rightList) - i)): # concatenate a maximum of 8 lines
                    if hasRightNeighbour:
                        if rightList[i + j][0] - rightList[i][0] <= 8: # make sure line being concatenated is within the 8 limit
                            concatenate += rightList[i + j][1]
                        else:
                            break

                        distance = 1 - normalLevenshtein(l[1], concatenate)

                        if distance >= maxLineSplitSim: # [swap distance > max with distance >= max]
                            maxLineSplitSim = distance
                        else:
                            break
                        subLineSplits.append(rightList[i + j][0])
                    else:
                        break
                
                subLineSplits.insert(0, maxLineSplitSim) # levenshtein score to front for easy access
                lineSplitsRight.append(subLineSplits)

            if maxLineSplitSim > 0.85: # VERY HIGH THRESHOLD FOR LINE SPLIT MAPPINGS
                lineSplitsRight.sort(reverse=True)
                mappings.append((l[0], lineSplitsRight[0][1:])) #add best multi-line mapping to specific left list line to list

            #might need to consider implementing logic for edge cases where leftlist lines overlap on their mappings to rightlist line splits? (unlikely)

    # From some tests, many line splits are not mapped because parts of them are directly mapped instead (threshold for regular mappings might be too low)
    mappings.sort()
    print(mappings) #FINAL OUTPUT!!!!