# Self-Study Discussion 22.3: Limitations of Hierarchical Clustering

## Reflection on the Myopic Nature and Practical Constraints of Hierarchical Methods

---

**Examples when early merges could lead to suboptimal results**

The irreversibility of hierarchical clustering is its defining weakness. Consider a financial transaction dataset where fraudulent accounts cluster in a narrow region of behavioural space — similar average transaction value but occurring at unusual hours. If the algorithm first merges by transaction value alone (because that distance happens to be smallest at that step), the fraud cluster dissolves into a broader "moderate-spend" grouping and the temporal signal is permanently lost. No later merge step can recover it.

A second example: in genomics, where gene expression profiles may have two orthogonal structures — one driven by tissue type, another by disease state — an early merge on tissue similarity forecloses discovering the disease-state structure entirely. The most scientifically meaningful partition is often not the one discoverable by sequential greedy merges.

In my BBO capstone, analogous myopia appeared when using grid-based search: committing to a region early left high-performing boundary zones permanently undersampled because the search "locked in" around an initially promising centroid.

---

**How other limitations play a role**

**Computational cost** scales as $O(n^2)$ in memory and $O(n^2 \log n)$ or worse in time, making hierarchical methods impractical beyond roughly 10,000–50,000 observations without approximation. For the Hull Tactical S&P 500 dataset with high-frequency features, applying hierarchical clustering directly to the full feature-observation matrix would be prohibitive.

**Noise sensitivity** is particularly acute with single linkage, where a single noisy point bridging two true clusters creates a false chain and merges them prematurely — the "chaining" effect. Complete linkage is more robust here but trades this for outlier sensitivity in the opposite direction.

**High-dimensional data** degrades all distance metrics as dimensions increase (the curse of dimensionality): Euclidean distances concentrate around a common value, making "near" and "far" increasingly indistinguishable. With even 20–30 features, hierarchical clustering routinely produces dendrograms that reflect measurement noise rather than genuine structure.

---

**Comparison to k-means**

K-means is more scalable ($O(nkd)$ per iteration), revisable (reassignment occurs at every step), and better suited to large, roughly spherical clusters. Hierarchical clustering does not require specifying $k$ in advance and produces a full dendrogram enabling post-hoc exploration of different granularities — a meaningful advantage in exploratory settings. Neither method handles elongated or irregular shapes well without pre-processing; DBSCAN is superior for arbitrary geometries.

---

**Strategies to mitigate these limitations**

1. **Dimensionality reduction before clustering:** PCA or UMAP to 5–15 components restores geometric meaningfulness and compresses runtime.
2. **Outlier removal:** IQR or isolation forest pre-processing prevents chaining artefacts in single linkage.
3. **Hybrid approaches:** Use hierarchical clustering on a representative subset (e.g., k-means centroids) to determine cluster count $k$, then apply k-means on the full dataset — combining interpretability with scalability.
4. **Linkage selection:** Average linkage or Ward's method generally outperform single/complete linkage for real-world data with moderate noise.
