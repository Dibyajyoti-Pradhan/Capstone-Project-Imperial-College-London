# Self-Study Discussion 8.2 – Analysing the Impact of Additional Predictors

## The Dark-Dining Example: Adding Spiciness as a Predictor

### What would happen to the nearest neighbour classifier?

If we add spiciness (measured on the Scoville scale, ranging from 0 to 15,000,000) to the existing predictors of sweetness and crunchiness (both on a 1–10 scale), the KNN classifier would become heavily distorted. Since KNN relies on distance calculations — typically Euclidean distance — the feature with the largest numerical range dominates the metric.

In this case, even a tiny difference in spiciness (say, 1,000 Scoville units) would vastly outweigh any differences in sweetness or crunchiness. The classifier would essentially ignore the original two predictors and base its decisions almost entirely on spiciness. Two foods that are identical in taste and texture but differ slightly in heat would appear "far apart" in the feature space, while foods with similar spiciness but completely different sweetness profiles would be considered "neighbours."

### How might adding this unscaled predictor affect the model's classification?

The model would produce unreliable and often nonsensical classifications. For example:

- A mild tomato might be grouped with bland proteins simply because they share low spiciness values
- A slightly spicy fruit could be misclassified as a vegetable or protein because its Scoville score pushes it away from other fruits
- The meaningful relationships between sweetness, crunchiness, and food categories would be completely overshadowed

In short, the classifier would no longer reflect the true similarities between foods — it would just be sorting by heat level.

### Why would feature scaling or normalisation be important in this case?

Feature scaling ensures that all predictors contribute proportionally to the distance calculation. Common approaches include:

- **Min-max scaling:** Transforms all features to a 0–1 range
- **Standardisation (z-score):** Rescales features to have mean 0 and standard deviation 1

By scaling sweetness, crunchiness, and spiciness to comparable ranges, no single feature dominates. The KNN classifier can then consider all three attributes fairly when determining which foods are truly "nearest" to each other. Without scaling, the algorithm implicitly assumes that spiciness is thousands of times more important than the other features — which clearly isn't the intent.

### Another situation where a new predictor may unintentionally distort a model's decision

A real-world example occurs in **employee performance prediction**. Suppose a model uses features like:

- Years of experience (0–40)
- Performance rating (1–5)
- Number of certifications (0–10)

If we then add **annual salary** (ranging from £20,000 to £200,000) without scaling, salary would completely dominate the distance calculations. The model might cluster employees primarily by pay grade rather than by actual performance indicators. Two employees with identical experience, ratings, and certifications but different salaries would appear very "far apart" — even though their performance profiles are nearly identical.

This illustrates why scaling isn't just a technical nicety — it's essential for ensuring the model captures the relationships we actually care about, rather than being hijacked by whichever feature happens to have the largest numerical range.
