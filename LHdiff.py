import sys
import string
import math
from simhash import Simhash # python-Simhash; might be 128-bit?? [add dependency] 
import heapq
import tkinter as tk
import os.path as path
import subprocess
import threading
import re

# REMINDER: TRY TO REFACTOR ALL INSTANCES OF LEVENSHTEIN AT SOME POINT

# LHDiff paper: https://www.cs.usask.ca/~croy/papers/2013/LHDiffFullPaper-preprint.pdf
# very useful paper: http://www.xmailserver.org/diff2.pdf

def InputGUI(frame, message, col):
    tk.Label(frame, text=message).grid(row=0, column=col, pady=(0,5))
    entry = tk.Entry(frame, width=30)
    entry.grid(row=1, column=col, padx=10)
    return entry

def ButtonGUI(oldEntry, newEntry, oldText, newText, error, map_widget):
    global fpOld, fpNew
    fpOld = oldEntry.get().strip()
    fpNew = newEntry.get().strip()
    # Clears the previous message
    error.config(text="")

    if fpOld == "" or fpNew == "":
        error.config(text="Please enter both files") 
        return

    oldFile = File("old", fpOld)
    newFile = File("new", fpNew)

    if not(oldFile) and not(newFile):
        error.config(text="Old and new files not found, please try again")
        return
    elif not(oldFile):
        error.config(text="Old file not found, please try again")
        return
    elif not(newFile):
        error.config(text="New file not found, please try again")
        return

    oldText.delete("1.0", tk.END)
    oldText.insert("1.0", oldFile)

    newText.delete("1.0", tk.END)
    newText.insert("1.0", newFile)

    file1 = Normalize(oldFile)
    file2 = Normalize(newFile)
    # Pass full file paths so git blame can work in the GUI
    old_full_path = path.join(path.dirname(path.abspath(__file__)), "Old_File_Versions", fpOld)
    new_full_path = path.join(path.dirname(path.abspath(__file__)), "New_File_Versions", fpNew)
    
    # run expensive diff+blame in a background thread to keep UI responsive
    def worker():
        maps, lefts, rights = LHDiff(file1, file2, old_path=old_full_path, new_path=new_full_path)
        # update UI on main thread
        def on_done():
            # populate the results map widget and highlights
            map_widget.delete("1.0", tk.END)
            MappingResults(map_widget, oldFile, newFile, oldText, newText, maps, lefts, rights)
            # re-enable entries
            oldEntry.config(state='normal')
            newEntry.config(state='normal')
        root = tk._get_default_root()
        if root:
            root.after(0, on_done)
    
    # disable entries while working
    oldEntry.config(state='disabled')
    newEntry.config(state='disabled')
    threading.Thread(target=worker, daemon=True).start()

def MappingResults(map, oldFile, newFile, oldText, newText, mappings, deletions, insertions):
    splitFile1 = oldFile.splitlines()
    splitFile2 = newFile.splitlines()

    # Setting up Highlights
    oldText.tag_configure("del", background ="#ffb3b3")  # Red
    oldText.tag_configure("move", background ="#b3d9ff") # Blue
    newText.tag_configure("move", background ="#b3d9ff") # Blue, again
    newText.tag_configure("ins", background ="#b8ffb8") # Green

    # Clearing any prior highlights
    for i in ("del", "move"):
        oldText.tag_remove(i, "1.0", "end")
    for i in ("ins", "move"):
        newText.tag_remove(i, "1.0", "end")

    # Swaps and moves
    map.insert("end", "Moved or swapped lines:\n")
    moves = False
    for i, j in mappings:
        if isinstance(j, list):
            moves = True

            oldText.tag_add("move", f"{i}.0", f"{i}.end")
            if (i-1) < len(splitFile1):
                oldData = splitFile1[i-1]
            else:
                oldData = ""
            map.insert("end", f"old line {i} moved to new line {j}\n")
            map.insert("end", f"\t- {oldData}\n")
            for k in j:
                newText.tag_add("move", f"{k}.0", f"{k}.end")
                if (k-1) < len(splitFile2):
                    newData = splitFile2[k-1].lstrip()
                else:
                    newData = ""
                map.insert("end", f"\t+ old line {i} moved to new {j}\n")
            map.insert("end", "\n")
        else:
            if i != j:
                moves = True
                oldText.tag_add("move", f"{i}.0", f"{i}.end")
                newText.tag_add("move", f"{j}.0", f"{j}.end")
                if (i-1) < len(splitFile1):
                    oldData = splitFile1[i-1].lstrip()
                else:
                    oldData = ""
                if (j-1) < len(splitFile2):
                    newData = splitFile2[j-1].lstrip()
                else:
                    newData = ""

                if (oldData == newData):
                    map.insert("end", f"old line {i} swapped with new line {j}\n")
                    map.insert("end", f"\t-/+ {oldData}\n")
                else:
                    map.insert("end", f"old line {i} swapped with new line {j}\n")
                    map.insert("end", f"\t- {oldData}\n")
                    map.insert("end", f"\t+ {newData}\n\n")
    if not(moves):
        map.insert("end", "N/A\n")
    else:
        map.insert("end", "\n")
    
    # Insertions
    map.insert("end", "Inserted lines:\n")
    if insertions:
        for i, k in insertions:
            newText.tag_add("ins", f"{i}.0", f"{i}.end")
            if (i-1) < len(splitFile2):
                data = splitFile2[i-1].lstrip()
            else:
                data = ""
            map.insert("end", f"+ {i}: {data}\n")
        map.insert("end", "\n")
    else:
        map.insert("end", "N/A\n\n")
    
    # Deletions
    map.insert("end", "Deleted lines:\n")
    if deletions:
        for i, j in deletions:
            oldText.tag_add("del", f"{i}.0", f"{i}.end")
            if (i-1) < len(splitFile1):
                data = splitFile1[i-1].lstrip()
            else:
                data = ""
            map.insert("end", f"+ {i}: {data}\n")
        map.insert("end", "\n")
    else:
        map.insert("end", "N/A\n\n")
    
    # Print the mappings.
    map.insert("end", f"Mappings:\n{mappings}")
    
def File(x, fp):
    # Folder with the GUI's directory. 
    dirRoot = path.dirname(path.abspath(__file__))

    #fp = input("Enter the "+x+" file: ")

    if (x == "old"):
        #New_File_Versions Folder.
        dirData = path.join(dirRoot, "Old_File_Versions")
        dirPath = path.join(dirData, fp)
    elif (x == "new"):
        #Old_File_Versions Folder.
        dirData = path.join(dirRoot, "New_File_Versions")
        dirPath = path.join(dirData, fp)

    try:
        file = open(dirPath, "r")
        return file.read()
    except FileNotFoundError:
        return 0
    
# PREPROCESSING: stream normalized lines from file with lazy evaluation
def Normalize(text: str):
    #Generator that yields normalized lines one at a time
    f = text.splitlines()
    normalizedLines = []
    for i in f:
        cleaned = " ".join(i.split())
        normalized = cleaned.lower().strip()
        normalizedLines.append(normalized)
    return normalizedLines

# add a compact on-demand line cache to avoid materializing all lines
class LineCache:
    def __init__(self, path, encoding='utf-8'):
        self.path = path
        self.encoding = encoding
        # open file in binary mode and build offsets (small memory: 8 bytes * #lines)
        self._f = open(path, 'rb')
        self._offsets = []
        pos = self._f.tell()
        line = self._f.readline()
        while line:
            self._offsets.append(pos)
            pos = self._f.tell()
            line = self._f.readline()
        self._len = len(self._offsets)

    def __len__(self):
        return self._len

    def __getitem__(self, idx):
        if idx < 0:
            idx += self._len
        if idx < 0 or idx >= self._len:
            raise IndexError("LineCache index out of range")
        self._f.seek(self._offsets[idx])
        bline = self._f.readline()
        try:
            line = bline.decode(self.encoding, errors='replace')
        except Exception:
            line = bline.decode('latin-1', errors='replace')
        cleaned = " ".join(line.split())
        return cleaned.lower().strip()

    def close(self):
        try:
            self._f.close()
        except Exception:
            pass

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

# Cache structures to avoid repeated subprocess calls
_GIT_BLAME_LINE_CACHE = {}   # filepath -> { line_num: commit_hash }
_GIT_BLAME_MSG_CACHE = {}    # commit_hash -> commit_message

#Run a single `git blame --porcelain` for filepath and populate line->commit_hash cache.
def _populate_blame_cache(filepath):
    if filepath in _GIT_BLAME_LINE_CACHE:
        return
    line_to_hash = {}
    try:
        result = subprocess.run(
            ['git', 'blame', '--porcelain', filepath],
            cwd=path.dirname(path.abspath(filepath)) or '.',
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            _GIT_BLAME_LINE_CACHE[filepath] = {}
            return

        lines = result.stdout.splitlines()
        i = 0
        while i < len(lines):
            m = re.match(r'^([0-9a-f]+) (\d+) (\d+)', lines[i])
            if m:
                commit_hash = m.group(1)
                final_lineno = int(m.group(3))
                line_to_hash[final_lineno] = commit_hash
                # skip headers until the source line (starts with a tab)
                i += 1
                while i < len(lines) and not lines[i].startswith('\t'):
                    i += 1
                i += 1
            else:
                i += 1
        _GIT_BLAME_LINE_CACHE[filepath] = line_to_hash
    except Exception:
        _GIT_BLAME_LINE_CACHE[filepath] = {}

#Return commit message for a commit hash, caching results.
def _get_commit_message_for_hash(commit_hash, repo_dir):
    if not commit_hash:
        return None
    if commit_hash in _GIT_BLAME_MSG_CACHE:
        return _GIT_BLAME_MSG_CACHE[commit_hash]
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B', commit_hash],
            cwd=repo_dir or '.',
            capture_output=True,
            text=True,
            timeout=10
        )
        msg = result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        msg = None
    _GIT_BLAME_MSG_CACHE[commit_hash] = msg
    return msg

#Get the commit message that last modified a specific line using a cached git blame result.
def get_commit_message_for_line(filepath, line_num):
    _populate_blame_cache(filepath)
    line_map = _GIT_BLAME_LINE_CACHE.get(filepath, {})
    commit_hash = line_map.get(line_num)
    repo_dir = path.dirname(path.abspath(filepath)) or '.'
    return _get_commit_message_for_hash(commit_hash, repo_dir)

#Classify change based on commit message keywords.
def classify_change_by_commit_message(commit_msg):
    if not commit_msg:
        return 'unknown'
    
    msg_lower = commit_msg.lower()
    
    fix_keywords = ['fix', 'bug', 'patch', 'hotfix', 'resolve', 'issue', 'crash', 'error', 'revert', 'optimization']
    intro_keywords = ['feature', 'add', 'new', 'implement', 'refactor', 'wip', 'todo', 'draft']
    
    fix_score = sum(1 for kw in fix_keywords if kw in msg_lower)
    intro_score = sum(1 for kw in intro_keywords if kw in msg_lower)
    
    if fix_score > intro_score:
        return 'bug_fix'
    elif intro_score > fix_score:
        return 'bug_intro'
    return 'neutral'

def LHDiff(file1, file2, old_path=None, new_path=None):
    # Materialize only when needed (DP requires indexing)
    # use on-demand file-backed cache (much smaller peak memory than storing all lines)
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
    
    # Classify each mapping by commit message using git blame
    classifications = []
    # Use provided new_path if available, otherwise fall back to CLI arg
    blame_file = new_path if new_path else (sys.argv[2] if len(sys.argv) > 2 else None)
    
    for m in mappings:
        if blame_file is None:
            commit_msg = None
        else:
            if isinstance(m[1], list):
                # Line split: check first line in the split
                commit_msg = get_commit_message_for_line(blame_file, m[1][0])
            else:
                # Single line: check the mapped line in file2
                commit_msg = get_commit_message_for_line(blame_file, m[1])
        
        ctype = classify_change_by_commit_message(commit_msg)
        classifications.append(ctype)
    
    # Aggregate classifications to determine overall commit type
    bug_fixes = classifications.count('bug_fix')
    bug_intros = classifications.count('bug_intro')
    neutrals = classifications.count('neutral')
    unknowns = classifications.count('unknown')
    
    # Determine overall commit classification
    if bug_fixes > bug_intros:
        overall_type = 'bug_fix'
    elif bug_intros > bug_fixes:
        overall_type = 'bug_intro'
    else:
        overall_type = 'neutral'
    
    # Print summary
    print(f"COMMIT CLASSIFICATION: {overall_type}")
    print(f"  Bug fixes: {bug_fixes}")
    print(f"  Bug introductions: {bug_intros}")
    print(f"  Neutral: {neutrals}")
    print(f"  Unknown: {unknowns}")
    print(f"  Total mappings: {len(mappings)}")
    
    # close file handles held by caches
    try:
        file1.close()
        file2.close()
    except Exception:
        pass
    
    mappings.sort()
    return mappings, leftList, rightList

if __name__ == '__main__':
    root = tk.Tk()
    root.title("LHdiff")

    top = tk.Frame(root)
    top.pack(fill="x", padx=10, pady=10)
    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=1)

    oldEntry = InputGUI(top, "Enter the old file: ", 0)
    newEntry = InputGUI(top, "Enter the new file: ", 1)

    error = tk.Label(top, text="", fg="red")
    error.grid(row=3, column=0, columnspan=2)

    middle = tk.Frame(root)
    middle.pack(fill="both", expand=True)

    left = tk.Frame(middle)
    right = tk.Frame(middle)
    left.pack(side="left", fill="both", expand=True)
    right.pack(side="right", fill="both", expand=True)

    tk.Label(left, text="Old File:", font=("Arial", 16, "bold")).pack(anchor="w")
    tk.Label(right, text="New File:", font=("Arial", 16, "bold")).pack(anchor="w")

    oldText = tk.Text(left, wrap="word")
    oldText.pack(side="left", fill="both", expand=True)

    newText = tk.Text(right, wrap="word")
    newText.pack(side="right", fill="both", expand=True)


    bottom = tk.Frame(root)
    bottom.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    tk.Label(bottom, text="Result: ", font=("Arial", 16, "bold")).pack(anchor="w")
    map = tk.Text(bottom, wrap="word")
    map.pack(fill="both", expand=True)

    tk.Button(
        top, 
        text="Enter", 
        command=lambda:ButtonGUI(oldEntry, newEntry, oldText, newText, error, map)
    ).grid(row=2, column=0, columnspan=2, pady=10)
    
    root.mainloop()