# LHDiff — A Hybrid, Language-Independent Line Differencing Tool

# Group #4 Members:
- Michael Gibb (110102732)
- Ronit Mahajan (110036557)
- Charbel Nakhoul (110043150)
- John Ezetah (10469910)
- Nico Bellanger (110138244)

## Introduction

LHDiff is a Python implementation of the algorithm described in **“LHDiff: A Language-Independent Hybrid Approach for Code Differencing”** by Asaduzzaman et al. (2013).

This tool detects line-level changes between two text files (source code or plain text) using a hybrid strategy that combines:
* **Context Similarity** (Cosine Similarity over surrounding lines)
* **Content Similarity** (Levenshtein Distance)
* **Efficient Hashing** (Simhash)

The result is a robust algorithm capable of identifying matches, modified lines, and even moved lines within files.

## Features

Uses tkinter to generate an interactive Graphical User Interface (GUI) in order to input files and access a function that will use simhash  to calculate Hamming distance between the Simhashes and then add them to a list of candidates that will then be output on the GUI and the terminal.

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

Simply run the program and input the old and new files. It will be used to compare changes made between each file.

### Run the GUI script from your terminal:

python LHdiff.py

This is the main project file that will trigger the GUI where you can enter the test files and it will display the highlights of changes made between the files (moves in blue, insertions in green, deletions in red), as well as the overall results in an organized format.

python test.py

This is a purer test file that will trigger the GUI, where you can enter the test files and after clicking the enter button, results will be printed in the terminal.

## Example Output

Terminal:
COMMIT CLASSIFICATION: bug_intro
  Bug fixes: 0
  Bug introductions: 18
  Neutral: 0
  Unknown: 0
  Total mappings: 18
COMMIT CLASSIFICATION: bug_intro
  Bug fixes: 0
  Bug introductions: 18
  Neutral: 0
  Unknown: 0
  Total mappings: 18

GUI:
Moved or swapped lines:
old line 11 swapped with new line 15
	-/+ }
old line 13 swapped with new line 17
	-/+ public static void main(String[] args) {
old line 14 swapped with new line 18
	-/+ double f = 98.6;
old line 15 swapped with new line 19
	-/+ double c = toCelsius(f);
old line 17 swapped with new line 21
	-/+ System.out.println("F to C: " + c);
old line 19 swapped with new line 23
	-/+ double c2 = 37.0;
old line 20 swapped with new line 24
	-/+ double f2 = toFahrenheit(c2);
old line 22 swapped with new line 26
	-/+ System.out.println("C to F: " + f2);
old line 23 swapped with new line 29
	-/+ }
old line 24 swapped with new line 30
	-/+ }

Inserted lines:
+ 13: public static double toKelvin(double celsius) { // added method
+ 14: return celsius + 273.15;

Deleted lines:
N/A

Mappings:
[(1, 1), (3, 3), (4, 4), (5, 5), (6, 6), (8, 8), (9, 9), (10, 10), (11, 15), (13, 17), (14, 18), (15, 19), (17, 21), (19, 23), (20, 24), (22, 26), (23, 29), (24, 30)]

## Interpretation

(1, 1) → Line 1 in File A matches Line 1 in File B



(2, 3) → Line 2 in File A corresponds to Line 3 in File B (moved)



(3, 2) → Line 3 in File A corresponds to Line 2 in File B (moved)



(n, m) pairs show all detected matches, moves, and alignments


##






