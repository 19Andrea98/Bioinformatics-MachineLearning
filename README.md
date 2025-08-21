In the `Notebook` folder you’ll find the code I use to preprocess protein sequences.  
The examples focus on phage protein sequences from datasets downloadable via **PhageScope**, but the code should be useful for other applications as well.

## Notebook 001
This notebook addresses the following tasks:

1. Decompress `.tar.gz` archives to extract `.fasta` files.  
2. If multiple `.fasta` files are produced, merge them into a single consolidated `.fasta`.  
3. Merge the consolidated `.fasta` with the corresponding metadata file (handled by a dedicated helper class).  
4. Perform a descriptive analysis of the resulting dataset.  
5. Filter out low-quality or low-confidence sequences.  
6. Remove invalid sequences (e.g., characters outside the standard amino-acid alphabet).

**Goal:** produce a clean dataset containing `Phage_ID`, protein `Sequence`, and relevant metadata for downstream analysis.

## Notebook 002
Caudovirales is the most abundant phage class across all datasets available on PhagesDB. To balance this distribution, I developed this code to specifically collect the Inoviridae and Microviridae classes from all datasets downloadable on PhagesDB. This step was performed after the pre-processing stage (Notebook 001). The collected classes were then merged with the PhagesDB dataset - a choice made purely for personal preference.
