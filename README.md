# Multilingual Natural Language Processing Social Advertising Recommendation System

This is a student Term Project in `Information Retrieval and Text Mining` by Prof. Chien Chin Chen, National Taiwan University.

## Quick Links

- [IRTM Term Project](https://github.com/brianCHUCHU/Social_Advertisement_Recommendation_System/blob/main/IRTM%20Term%20Project.pdf): For detailed documentation in formal PDF format.

## Brief Description
### Abstract
The paper presents a Social Advertising Recommendation System model trained on diverse datasets containing user purchase records and social relationships. The training process involves trustworthiness scoring, an information retrieval system, and evaluation of model success.

### Data Description
- Dataset: Real-world dataset from LibraryThing comprising reviews and user connections.
- Data Format: Descriptions of columns in the `reviews.txt` and `edges.txt` files.
- Data Statistics: Summary of dataset size and file sizes, highlighting potential hardware limitations.

### Data Preprocessing
- Network Graph Construction: Utilization of Dijkstra's Shortest Path algorithm to create subnetworks based on user connections.
- Time Threshold Determination: Methodology for splitting the dataset into training and validation sets based on a time threshold.

### Trustworthiness Scoring
- Transform: Usage of a sentence-transformers model to convert text data into fixed-length vectors.
- Cosine Similarity: Calculation of trustworthiness scores based on cosine similarity between comments from different users.

### Model Construction & Optimization
- Ranking Items: Formula for scoring recommended products based on various factors like user ratings, helpfulness, trustworthiness, and degree within subgraphs.
- Formula Parameters Optimization: Maximization problem to identify optimal parameter values for the scoring formula.

### System Outcome & Performance Evaluation
- Ranking Items: Presentation of top-scored recommendations and identification of purchased items within top recommendations. 
- Unveiling Potential: Discussion on the effectiveness of the system and potential improvements.

### Conclusion & Recommendations
- Limitations & Assumptions: Discussion on memory and time complexity limitations, and assumptions made in the model.
- Potential Improvements: Suggestions for backtesting, addressing time complexity, flexibility improvements, and addressing imbalanced effectiveness.