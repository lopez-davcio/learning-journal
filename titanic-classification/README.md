# Titanic - Machine Learning from Disaster

1. **Project Overview** 
2. **Motivation** 
3. **Installation & Usage** 
4. **Design Decisions & Thought Process**
5. **Challenges & Solutions** 
6. **Key Learnings** 
7. **Future Improvements** 

# Project Overview
This project focuses on the classic Titanic dataset from Kaggle, aimed at predicting passenger survival using binary classification. The analysis involves exploratory data analysis (EDA), data visualization, and an iterative machine learning workflow. I compared various algorithms, including tree-based models (RandomForest, XGBoost, CatBoost) and distance-based models (SVM, Logistic Regression), to find the most robust predictor for this historical event.

# Motivation
Following my previous work on a university management system and a library system, I wanted to transition from object-oriented programming in Python to data science and machine learning. My goal was to move beyond simple model fitting and learn how to build professional, reproducible machine learning workflows. Specifically, I wanted to master:
*   Automating data preprocessing for mixed data types.
*   Ensuring model robustness through testing.
*   Engineering new features from raw string data (like names and cabin numbers).

# Installation & Usage
#### To run the project:
*   Clone the repository.
*   Ensure you have the following libraries installed: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `xgboost`, and `catboost`.
*   Download the `train.csv` and `test.csv` files from the [Kaggle Titanic Competition](https://www.kaggle.com/c/titanic/data).
*   Open and run the `titanic-analysis.ipynb` Jupyter Notebook.

# Design Decisions & Thought Process
The project was designed around a multi-stage pipeline:
*   **EDA & Baseline:** I began with a simple baseline to understand the impact of basic features like `Sex` and `Pclass`.
*   **Modular Preprocessing:** I used **ColumnTransformers** to separate the treatment of numerical features (imputing and scaling) from categorical features (one-hot encoding). 
*   **Feature Engineering:** I created a "Title" feature by extracting prefixes from names and calculated "Family Size" to see if social units impacted survival rates.
*   **Model Comparison:** I tested 12 different algorithms, categorized into tree-based and non tree-based based models, to observe how they reacted to the same data.
*   **Hyperparameter Tuning:** Used `RandomizedSearchCV` to optimize the top-performing models.

# Challenges & Solutions
**Challenge:** Data leakage and repetitive code. 
**Solution:** Implementing **Pipelines**. By wrapping the preprocessing and the estimator into a single object, I ensured that the transformers were fit only on training data, preventing information from the test set from "leaking" into the model.

**Challenge:** Overfitting on the training set.
**Solution:** I utilized **Stratified K-Fold Cross-Validation**. This ensured that every model was tested on different subsets of the data, providing a more realistic accuracy score than a single train/test split.

# Key Learnings
This project was a major technical milestone for me. The three most significant tools I mastered were:
1.  **ColumnTransformers:** These allowed me to apply different transformations to specific columns (e.g., scaling `Age` while one-hot encoding `Embarked`) within a single line of code.
2.  **Pipelines:** I learned that pipelines are essential for clean, production-ready code. They ensure that the entire sequence of data transformation and prediction is bundled together.
3.  **Cross-Validation:** I moved from simple validation to 5-fold cross-validation, which provided a much more reliable metric for comparing different algorithms.

**A Critical Insight on Thresholds:**
I experimented with adjusting the classification threshold to optimize accuracy on the training data. I discovered that while a specific threshold (e.g., 0.66) significantly boosted accuracy on my training set, it actually decreased performance on the hidden test data. This taught me that threshold tuning is a delicate process often more suitable for class inference (balancing precision and recall) than for improving general model accuracy.

# Future Improvements
*   **Documentation of Thought Process:** In future projects, I aim to provide more granular, step-by-step explanations of *why* certain methods were chosen, rather than just presenting the results.
*   **Variable Naming Conventions:** I plan to adopt a more coherent and descriptive variable naming strategy to better reflect the state of the data (e.g., distinguishing clearly between `raw_df`, `processed_df`, and `final_features`).