import numpy as np
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

class Dendrogram:
    def __init__(self, model):
        """
        Wrapper class for building a linkage matrix and visualizing dendrograms
        from a fitted AgglomerativeClustering model (scikit-learn).
        """
        self.model = model

    def linkage_matrix(self):
        """
        Build the linkage matrix from the scikit-learn AgglomerativeClustering model.
        
        Returns
        -------
        linkage_matrix : np.ndarray
            Array of shape (n_samples - 1, 4) containing:
            - the indices of the merged children
            - the distance of the merge
            - the number of original samples in the newly formed cluster
        """
        children = self.model.children_
        labels = self.model.labels_
        distances = self.model.distances_

        n_samples = len(labels)
        counts = np.zeros(children.shape[0])

        # Count how many original samples are contained in each non-leaf node
        for i, merge in enumerate(children):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        # Build linkage matrix in the same format as SciPy
        linkage_matrix = np.column_stack([children, distances, counts]).astype(float)
        return linkage_matrix

    def plot_dendogram(self, **kwargs):
        """
        Plot the dendrogram using SciPy's dendrogram function.
        
        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments passed to scipy.cluster.hierarchy.dendrogram
        """
        linkage_matrix = self.linkage_matrix()
        dendrogram(linkage_matrix, **kwargs)
        plt.show()

    def _get_leaves(self, node, n_samples, linkage_matrix):
        """
        Recursive helper function to get all leaf indices under a given node.
        
        Parameters
        ----------
        node : int
            Index of the node (either a leaf < n_samples, or a merged cluster >= n_samples)
        n_samples : int
            Number of original samples
        linkage_matrix : np.ndarray
            Linkage matrix computed from the model
        
        Returns
        -------
        leaves : list[int]
            Indices of samples under the given node
        """
        if node < n_samples:
            return [node]  # leaf node → return sample index
        else:
            node_id = node - n_samples
            left = int(linkage_matrix[node_id, 0])
            right = int(linkage_matrix[node_id, 1])
            return (self._get_leaves(left, n_samples, linkage_matrix) +
                    self._get_leaves(right, n_samples, linkage_matrix))

    def get_clusters(self, n_clusters):
        """
        Extract the indices of samples belonging to the last `n_clusters` merges.
        
        Parameters
        ----------
        n_clusters : int
            Number of clusters to retrieve from the bottom of the dendrogram.
        
        Returns
        -------
        cluster_index : list of lists
            Each sublist contains the indices of samples belonging to a cluster.
        """
        linkage_matrix = self.linkage_matrix()
        n_samples = len(self.model.labels_)

        cluster_index = []

        # Iterate over the last n_clusters merges
        for k, i in enumerate(range(len(linkage_matrix)-1,
                                    len(linkage_matrix)-n_clusters-1, -1)):
            cluster_index.append([])
            for j in range(2):  # two children per node
                child = int(linkage_matrix[i, j])
                leaves = self._get_leaves(child, n_samples, linkage_matrix)
                cluster_index[k].extend(leaves)

        return cluster_index
