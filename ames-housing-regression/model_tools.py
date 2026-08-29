import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate



def format_model_result(result):
    """
    Summarizes cross_validate results by calculating mean and std for all metrics.
    Converts NumPy types to Python floats and rounds to 5 decimal places.
    """
    summary = {}

    for key, value in result.items():
        summary[f'{key}_std'] = round(np.std(value).item(), 5)
        summary[f'{key}_mean'] = round(np.mean(value).item(), 5)

    return summary


def cross_validate_models(models, X, y, preprocessor, cv, version):
    """
    Fits and cross-validates multiple models using a shared preprocessing pipeline.

    Args:
        models: Dictionary mapping model names to estimators.
        X: The feature matrix (pd.DataFrame).
        y: The target vector (pd.Series).
        preprocessor: A ColumnTransformer or Pipeline.
        version: String suffix to identify this specific run in the results.
        cv_folds: Number of cross-validation folds (defaults to 5).

    Returns:
        A DataFrame where each row is a model's performance metrics.
    """
    results = {}
    
    for name, model in models.items():
        reg = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])

        result = cross_validate(reg, X, y,
                                scoring='neg_root_mean_squared_error',
                                cv=cv, n_jobs=-1, return_train_score=True)

        results[name + version] = format_model_result(result)

    return pd.DataFrame.from_dict(results, orient='index')