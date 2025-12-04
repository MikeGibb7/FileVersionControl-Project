A Python implementation of the LHDiff algorithm. This tool detects line-level changes between two text files (source code or plain text) by using a hybrid approach that combines context similarity, content similarity, and hashing.

Reference: Based on the paper LHDiff: A Language-Independent Hybrid Approach for Code Differencing (Asaduzzaman et al., 2013).

Features of the Project:
Context Awareness: Uses Cosine Similarity to check the surrounding lines (context) of a change, ensuring identical lines in different locations aren't mismatched.

Hybrid Matching: Combines Simhash (for fast candidate generation) with Levenshtein Distance (for precise content matching).

Move Detection: Capable of detecting when lines have been moved within a file.


Prerequisites
Python 3.x
Simhash library

Installation
Install the required dependency using pip:

pip install simhash

Usage
Run the script from the command line, providing the paths to the two files you want to compare.

Syntax

python LHdiff.py <path_to_file_A> <path_to_file_B>

Example
python LHdiff.py New_File_Versions/NewFile1.txt Old_File_Versions/OldFile1.txt

Example Output:

[(1, 1), (2, 3), (3, 2), (4, 4), (5, 5), (6, 6)]

Interpretation:

(1, 1): Line 1 in File A corresponds to Line 1 in File B (Match).

(2, 3): Line 2 in File A corresponds to Line 3 in File B (Moved).

(3, 2): Line 3 in File A corresponds to Line 2 in File B (Moved).