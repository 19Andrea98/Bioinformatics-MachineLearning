In the `Notebook` folder you’ll find the code I use to preprocess protein sequences. The examples focus on phage protein sequences from datasets downloadable via **PhageScope**, but the code should be useful for other applications as well.

In the `Class` foleder you'll find the classes I used in some of my notebooks.

!! Note that this directory is not fully completed yet !!

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
Caudovirales is the most abundant phage class across all datasets available on PhageScope. To balance this distribution, I developed this code to specifically collect the Inoviridae and Microviridae classes from all datasets downloadable on PhageScope. This step was performed after the pre-processing stage (Notebook 001). The collected classes were then merged with the PhagesDB dataset - a choice made purely for personal preference.

## Dendrogram Class
The "Dendrogram" class helps retrieve the sample indices for the n clusters obtained by cutting a hierarchical clustering dendrogram. In particular, get_clusters method of the class can be used to create a dictionary of indeces belonging to each cluster. This is useful if you want to plot only the points belonging to a selected cluster.
