import numpy as np
import pandas as pd
import os
import json

from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate, KFold
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from sklearn.svm import LinearSVR
from sklearn.linear_model import LinearRegression


class ModelEvaluator():

    def __init__(self, X:pd.DataFrame, y:pd.Series, results_path:str='models_results.JSON'):
        """
        A tool to evaluate estimators through cross validation and keep track of each version.

        This class provides methods to:
            - cross validate models.
            - show models previous results.
        
        Attributes:
            - X: features dataframe.
            - y: target/label.
            - cv: a 5 fold KFold instance to use in all ronds.
            - results_path: the path to the models results json file.
            - models_results: dictionary with the results of all models.
            - tree/linear/distance models: dictionaries mapping model name to model instance (one dictionary per type of algorithm)
        """

        # set the data
        self._X = X
        self._y = y

        # instantiate a k fold
        self.cv = KFold(n_splits=5, shuffle=True, random_state=42)

        # path for the dictionary with the models results
        self.results_path = results_path

        # load models results dictionary
        self._models_results = self._load_model_results()

        # create a dictionary of estimators per algorithm type to fit to the data 
        self.tree_models = {
            'RandomForest':RandomForestRegressor(random_state=42),
            'ExtraTree':ExtraTreesRegressor(random_state=42),
            'HistGradientBoosting':HistGradientBoostingRegressor(random_state=42),
            'XGB':XGBRegressor(booster='gblinear', device='cuda'),
            'CatBoost':CatBoostRegressor(random_state=42, verbose=0)
        }

        self.linear_models = {
            'OLS':LinearRegression(),
            'Ridge':KernelRidge(),
            'Lasso':Lasso(random_state=42),
            'ElasticNet':ElasticNet(random_state=42)
        }

        self.distance_models = {
            'KNN':KNeighborsRegressor(),
            'SVR':LinearSVR(random_state=42)
        }

        # combine all three dictionary of models/estimators into one dictionary
        self.all_models = self.tree_models | self.linear_models | self.distance_models

    def _load_model_results(self):
        """Loads the models results from JSON if it already exists, otherwise returns empty dict."""
        if os.path.exists(self.results_path):
            with open(self.results_path, 'r') as f:                
                return json.load(f)
        return {}

    def _save_models_results(self):
        """Saves models results to the models results json file."""   
        with open(self.results_path, 'w') as f:
            json.dump(self._models_results, f, indent=4)
        

    def show_models_results(self):
        """Displays the saved models results as a DataFrame"""
        if self._models_results:
            return pd.DataFrame.from_dict(self._models_results, orient='index')    
        return 'There is no information to display, models_results is empty.'


    def format_model_result(self, result):
        """
        Summarizes cross_validate results by calculating mean and std for all metrics.
        Converts NumPy types to Python floats and rounds to 5 decimal places.
        """
        summary = {}

        for key, value in result.items():
            summary[f'{key}_std'] = round(np.std(value).item(), 5)
            summary[f'{key}_mean'] = round(np.mean(value).item(), 5)

        return summary


    def cross_validate_models(self, preprocessor, version):
        """
        Fits and cross-validates multiple models using a shared preprocessing pipeline.
        Formats and saves models results to the 
        Args:
            preprocessor: A ColumnTransformer or Pipeline.
            version: String suffix to identify this specific run in the results.
        """        
        
        for name, model in self.all_models.items():
            reg = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', model)
            ])

            result = cross_validate(reg, self._X, self._y,
                                    scoring='neg_root_mean_squared_error',
                                    cv=self.cv, n_jobs=-1, return_train_score=True)

            self._models_results[name + version] = self.format_model_result(result)

            self._save_models_results()

        