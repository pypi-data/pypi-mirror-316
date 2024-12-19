import numpy as np
from sklearn.cluster import DBSCAN
from tqdm import tqdm

class veczip:
    """
    A core utility for compressing embeddings by reducing dimensionality based on holistic dimension analysis.

    It offers two modes of analysis: DBSCAN clustering for commonality and variance-based selection.

    It takes as input a numpy array of embeddings and returns the indices of the dimensions to retain,
    allowing the caller to then apply this selection to any column it wants.
    """

    def __init__(self, target_dims=16, mode="dbscan", quantize=False):
        """
        Initialize veczip for compressing embeddings.

        Args:
            target_dims (int): Number of dimensions to retain after pruning. Default is 16.
            mode (str): The mode of dimension analysis. Either 'dbscan' or 'variance'. Default is 'dbscan'.
            quantize (bool): Whether to quantize the embeddings into integers. Default is False
        """
        self.target_dims = target_dims
        self.mode = mode
        self.quantize = quantize
        if mode not in ["dbscan", "variance"]:
            raise ValueError("Invalid mode. Choose either 'dbscan' or 'variance'.")

    def analyze_dimensions(self, embeddings):
        """
        Analyzes dimensions in bulk to identify which to prune, based on the selected mode.

        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Scores for each dimension.
        """
        print(f"Analyzing dimensions using {self.mode} mode...")
        if self.mode == "dbscan":
            return self._analyze_dimensions_dbscan(embeddings)
        elif self.mode == "variance":
            return self._analyze_dimensions_variance(embeddings)

    def _analyze_dimensions_dbscan(self, embeddings):
        """
        Analyzes dimensions using DBSCAN clustering to identify commonality.

        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Commonality scores for each dimension.
        """
        n_samples, n_dims = embeddings.shape
        commonality_scores = []

        for dim in tqdm(range(n_dims), desc="Analyzing Dimensions (DBSCAN)"):
            dim_values = embeddings[:, dim].reshape(-1, 1)
            dbscan = DBSCAN(eps=0.01, min_samples=2)  # Fixed DBSCAN parameters
            labels = dbscan.fit_predict(dim_values)
            max_cluster_size = max((labels == l).sum() for l in set(labels) if l != -1)
            commonality_scores.append(max_cluster_size)
        return np.array(commonality_scores)

    def _analyze_dimensions_variance(self, embeddings):
      """
        Analyzes dimensions by calculating the variance for each dimension.
        
        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Variance scores for each dimension.
        """
      
      n_dims = embeddings.shape[1]
      variance_scores = np.var(embeddings, axis=0)
      return variance_scores
        

    def compress(self, embeddings):
        """
        Compresses embeddings to the target dimensions.

        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Indices of the dimensions to retain.
        """
        n_dims = embeddings.shape[1]
        effective_target_dims = min(self.target_dims, n_dims)
        print(f"Pruning embeddings to {effective_target_dims} dimensions...")

        scores = self.analyze_dimensions(embeddings)

        if self.mode == "dbscan":
            sorted_indices = np.argsort(scores)
            top_indices = sorted_indices[:effective_target_dims]
        elif self.mode == "variance":
            sorted_indices = np.argsort(scores)[::-1] # Descending order
            top_indices = sorted_indices[:effective_target_dims]
        
        print("Compression completed.")
        return top_indices
    
    def quantize_embeddings(self, embeddings):
        """
        Quantizes the embeddings to integers using rounding to nearest integer.

        Args:
            embeddings (np.ndarray): Numpy array of embeddings (N x D).

        Returns:
            np.ndarray: Quantized embeddings as integers.
        """
        if not self.quantize:
            return embeddings

        print("Quantizing embeddings to integers (rounding to nearest)...")
        quantized = np.rint(embeddings).astype(int)
        print("Quantization completed.")
        return quantized
    
    def dequantize_embeddings(self, quantized_embeddings):
        """
        Dequantizes the embeddings back to float values.
        In this case, since rounding-based quantization is used, this is simply a type conversion.

        Args:
            quantized_embeddings (np.ndarray): Quantized embeddings (N x D).

        Returns:
            np.ndarray: Dequantized float embeddings (N x D).
        """
        if not self.quantize:
            return quantized_embeddings

        print("Dequantizing embeddings to floats...")
        float_embeddings = quantized_embeddings.astype(float)
        print("Dequantization completed.")
        return float_embeddings


