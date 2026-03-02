# Self-Study Discussion 22.2: Measuring the Distance Between Clusters

## Reflection on Linkage Methods and Inter-Cluster Distance Metrics

---

**What is the conceptual difference between measuring distance between two points and measuring distance between two clusters?**

Point-to-point distance is unambiguous: given two coordinates, Euclidean or Manhattan distance returns a single scalar. Cluster-to-cluster distance is inherently a design choice, because a cluster is a set of points rather than a single location. The analyst must specify *which representative property of each set* — minimum gap, maximum span, centroid, or average — determines proximity. This design choice is not cosmetic; it encodes an assumption about the geometry of the problem and cascades through the entire dendrogram.

---

**What are the common methods for measuring inter-cluster distance?**

Four linkage criteria dominate practice:

- **Single linkage** (nearest-neighbour): distance between the closest pair of points across clusters. Sensitive to chaining — elongated clusters merge readily.
- **Complete linkage** (furthest-neighbour): distance between the most distant pair. Produces compact, roughly spherical clusters but is sensitive to outliers.
- **Average linkage (UPGMA):** mean pairwise distance across all cross-cluster pairs. Balances compactness and chaining resistance; generally robust.
- **Centroid distance:** Euclidean distance between cluster means. Intuitive and computationally cheap, but can exhibit *inversions* (a merged cluster's centroid distance decreasing relative to pre-merge), producing non-monotone dendrograms that are difficult to interpret.

Ward's method is a fifth common choice, minimising total within-cluster variance at each merge step rather than operating on pairwise distances directly.

---

**How does the choice of linkage method impact clustering decisions?**

Linkage governs which structures can be discovered. Single linkage recovers elongated, irregular shapes and is useful for contour-following but prone to chaining noise. Complete linkage imposes spherical regularity. In my BBO capstone, functions F5 and F8 exhibited behaviour concentrated in narrow boundary regions — single linkage would have merged these regions into broader clusters prematurely, whereas complete linkage would have kept the concentrated high-performance subspace correctly isolated. The choice of linkage is therefore a prior belief about cluster geometry, not a neutral technical parameter.

---

**What are the practical considerations of using centroid distance?**

Centroid distance is interpretable — a business analyst can visualise the mean customer of each segment and compare them directly. However, the inversion problem is a serious operational concern: if successive merges produce a centroid distance that *decreases*, the dendrogram no longer reads as a clean hierarchy, and automated cut-point selection algorithms break down. Centroid distance also conflates within-cluster spread with between-cluster separation, making it unreliable when clusters have very different variances.

---

**How do you justify cluster groupings to non-technical stakeholders?**

The most effective approach is to narrate each cluster in concrete terms rather than statistical ones. Average linkage with five clusters might produce segments best described as "high-income urban early adopters" and "price-sensitive suburban families" — labels that connect directly to business decisions around pricing, channel and messaging. Supplementing this with a dendrogram showing where the natural breaks in dissimilarity occur (the longest vertical jumps before merging) gives stakeholders intuitive evidence that the chosen number of clusters reflects genuine structure rather than an arbitrary analyst preference.
