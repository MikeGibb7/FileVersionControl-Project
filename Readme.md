# LHDiff — A Hybrid, Language-Independent Line Differencing Tool

LHDiff is a Python implementation of the algorithm described in **“LHDiff: A Language-Independent Hybrid Approach for Code Differencing”** by Asaduzzaman et al. (2013).

This tool detects line-level changes between two text files (source code or plain text) using a hybrid strategy that combines:
* **Context Similarity** (Cosine Similarity over surrounding lines)
* **Content Similarity** (Levenshtein Distance)
* **Efficient Hashing** (Simhash)

The result is a robust algorithm capable of identifying matches, modified lines, and even moved lines within files.

## Features

### Context-Aware Matching
Prevents mismatching identical but unrelated lines by analyzing the similarity of surrounding lines using cosine similarity.

### Hybrid Matching Approach
Uses:
* **Simhash** → Generates candidates quickly
* **Levenshtein Distance** → Scores content similarity precisely

This reduces false matches while maintaining fast performance.

### Move Detection
Detects when a line appears in both files but at different locations.

## Prerequisites

* Python 3.x
* `simhash` library

## Installation

Install the required dependency:

```bash
pip install simhash 
```
## Usage



### Run the LHDiff script from your terminal:



python LHdiff.py <path_to_file_A> <path_to_file_B>



## Example

python LHdiff.py New_File_Versions/NewFile1.txt Old_File_Versions/OldFile1.txt



## Example Output

[(1, 1), (2, 3), (3, 2), (4, 4), (5, 5), (6, 6)]



## Interpretation



(1, 1) → Line 1 in File A matches Line 1 in File B



(2, 3) → Line 2 in File A corresponds to Line 3 in File B (moved)



(3, 2) → Line 3 in File A corresponds to Line 2 in File B (moved)



(n, m) pairs show all detected matches, moves, and alignments


##






