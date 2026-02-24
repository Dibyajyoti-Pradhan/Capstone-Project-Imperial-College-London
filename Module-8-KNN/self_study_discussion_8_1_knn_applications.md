# Self-Study Discussion 8.1 – Analysing Applications of KNN Methods

## KNN for Music Recommendation and Song Similarity

### Application Overview

A practical application of K-Nearest Neighbors is in music recommendation systems — specifically, finding songs that sound similar to one you already enjoy. Platforms like Spotify use similarity-based algorithms to power features like "Discover Weekly" and "Radio" playlists. While production systems often use more complex models, KNN provides an intuitive foundation for content-based music recommendation.

The problem KNN solves here is: given a song you like, find the k most similar songs in a library based on audio characteristics.

### How KNN Was Applied

**Data used:**
Music datasets like the Spotify Audio Features dataset (available on Kaggle) contain numerical descriptors for each track, including:
- **Danceability:** How suitable a track is for dancing (0.0 to 1.0)
- **Energy:** Intensity and activity level (0.0 to 1.0)
- **Tempo:** Beats per minute (BPM)
- **Valence:** Musical positiveness — happy vs sad (0.0 to 1.0)
- **Acousticness:** Whether the track is acoustic (0.0 to 1.0)
- **Instrumentalness:** Likelihood of no vocals (0.0 to 1.0)
- **Loudness:** Overall loudness in decibels

Each song becomes a point in a multi-dimensional feature space.

**Method:**
When a user selects a song, KNN calculates the distance (typically Euclidean or cosine similarity) between that song's feature vector and all other songs in the dataset. The k nearest neighbors — songs with the smallest distances — are returned as recommendations. Since features have different scales (tempo might range from 60–200 BPM while valence is 0–1), normalization is essential before computing distances.

**Outcome:**
KNN-based recommendation systems can surface genuinely similar-sounding tracks. For example, if you input an upbeat pop song with high danceability and energy, the algorithm returns other high-energy tracks rather than slow ballads. This creates coherent playlists that match the listener's mood.

A Kaggle project using this approach on Spotify data demonstrated that KNN could effectively cluster songs by audio features, producing recommendations that made intuitive sense when listened to.

### Strengths and Limitations

**Why KNN is a good fit:**
- **Intuitive:** The concept of "find songs that sound like this one" maps directly to KNN's core logic of finding nearest neighbors in feature space.
- **No training required:** KNN is a lazy learner — it simply stores the dataset and computes distances at query time. This makes it easy to add new songs without retraining.
- **Transparent:** You can explain why a song was recommended by showing which features made it similar (e.g., "both tracks have high energy and similar tempo").

**Drawbacks:**
- **Scalability:** Spotify has over 100 million tracks. Computing distances against the entire library for every query is computationally prohibitive. Production systems use approximate nearest neighbor methods (like Annoy or FAISS) to speed this up.
- **Cold start for new songs:** If a song lacks audio feature data, it cannot be placed in the feature space and won't appear in recommendations.
- **Ignores user context:** Pure content-based KNN doesn't consider listening history, user preferences, or collaborative signals (what similar users enjoyed). Hybrid systems combining KNN with collaborative filtering perform better.
- **Feature selection matters:** If irrelevant features are included or important ones are missing, the "nearest" songs may not actually sound similar to human ears.

### Reflection

KNN provides a clean, interpretable starting point for music recommendation. It works well for building playlist features where audio similarity is the primary goal. However, for large-scale production systems, it's typically combined with collaborative filtering and enhanced with approximate nearest neighbor algorithms to handle millions of tracks efficiently.

**Reference:**
- Spotify Audio Features Dataset on Kaggle: https://www.kaggle.com/datasets/tomigelo/spotify-audio-features
