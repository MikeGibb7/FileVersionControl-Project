import sys

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
    edits = [] #list of differences
    mappings = [] #1-to-1s
    n1 = f1
    n2 = f2
    while n1 > 0 or n2 > 0:
        action = actions[n1][n2]

        #take most efficient route back to top-left of table, recording mappings and edits along the way
        if action == MATCH:
            mappings.append((n1, n2))
            n1 -= 1
            n2 -= 1 
        elif action == ADD:
            edits.append((ADD, n2, file2[n2 - 1]))  
            n2 -= 1
        elif action == DELETE:
            edits.append((DELETE, n1, file1[n1 - 1]))
            n1 -= 1
        elif action == CHANGE:
            edits.append((CHANGE, n1, file1[n1 - 1], file2[n2 - 1]))
            n1 -= 1
            n2 -= 1
        else: 
            assert False, "unreachable" #fail state
    
    edits.reverse()
    mappings.reverse()

    for e in edits: #diagnostic 
        print(e)

    print(mappings) #final output
