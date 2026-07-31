import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype
import json
import os



class FeatureAnalyser:
    """
    A tool for automated Exploratory Data Analysis (EDA).
    
    This class provides methods to:
        - automatically detect feature types.
        - generate descriptive statistics and visualizations relative to a target response variable.
        - keep track of feature engineering decisions.
     
     Attributes:
        - df (pd.DataFrame): The dataset containing features and target.
        - target_feature_name (str): The name of the response variable (y).
        - discrete_threshold (int): The threshold to determine if a feature - should be treated as discrete or continuous.
        - roadmap_path = The path to the json file keeping track of decisions.
        - roadmap = A dictionary tracking feature engineering tasks to perform.
    """

    def __init__(self, df, target_feature_name, discrete_treshold=15, roadmap_path:str='preprocessing_roadmap.JSON'):
        self.df = df
        self.target_feature_name = target_feature_name        
        self.discrete_threshold = discrete_treshold
        self.roadmap_path = roadmap_path
        self.roadmap = self._load_roadmap()


    def _load_roadmap(self):
        """Loads the roadmap from JSON if it already exists, otherwise returns empty dict."""
        if os.path.exists(self.roadmap_path):
            with open(self.roadmap_path, 'r') as f:                
                return json.load(f)
        return {}


    def save_decision(self, feature_x_name, impute=None, encode=None, scale=None, power_transform=None, clip=None, group_cat=None, drop=None, reason=None):
        """Records a preprocessing decision and saves it to roadmap.JSON"""
        self.roadmap[feature_x_name] = {
            'impute': impute,
            'encode': encode,
            'scale': scale,
            'power_transform': power_transform,
            'clip': clip,
            'group_cat': group_cat,
            'drop': drop,
            'reason': reason}        
        with open(self.roadmap_path, 'w') as f:
            json.dump(self.roadmap, f, indent=4)
        print(f"Decision for {feature_x_name} saved to {self.roadmap_path}")

    def show_roadmap(self):
        """Displays the current progress as a DataFrame"""
        if self.roadmap:
            return pd.DataFrame.from_dict(self.roadmap, orient='index')    
        return 'There is no information to display, roadmap is empty.'


#####################################################################


    def print_basic_info(self, feature_x_name:str):
        """
        Print information common to both categorical and numerical features.
        Input: Name of the feature to analyse.
        """
        print(f'\n\n---### Analysing {feature_x_name} ###---')
        self.print_first_values(feature_x_name)
        self.print_missing_values(feature_x_name)


    def print_first_values(self, feature_x_name:str):
        """
        Print the first 5 values of the feature.
        Input: Name of the feature to analyse.
        """    
        print(f"\n{feature_x_name} first values:")
        print(self.df[feature_x_name].head())


    def print_description(self, feature_x_name:str):
        """
        Print description of the feature if dtype is numeric.
        Input: Name of the feature to analyse.
        """    
        if is_numeric_dtype(self.df[feature_x_name]):
            print(f"\n{feature_x_name} numeric description:")
            print(self.df[feature_x_name].describe().astype(int))
        else:
            print(f'{feature_x_name} is not numeric, no description is available.')


    def print_missing_values(self, feature_x_name:str):
        """
        Print number of missing values and percentage if there are missing values.
        Input: Name of the feature to analyse.
        """    
        if self.df[feature_x_name].isna().any():
            print(f'\n{feature_x_name} missing values:     {self.df[feature_x_name].isna().sum()}')
            print(f'{feature_x_name} missing values %:   {self.df[feature_x_name].isna().sum() / self.df[feature_x_name].size}')
        else:
            print(f'\n{feature_x_name} does not have missing values.')


    def print_number_unique_values(self, feature_x_name:str):
        """
        Input: Name of the feature to analyse.
        """
        print(f'\n{feature_x_name} number of unique values:')
        print(self.df[feature_x_name].nunique())


    def print_unique_values(self, feature_x_name:str):
        """    
        Input: Name of the feature to analyse.
        """
        print(f'\n{feature_x_name} unique values:')
        print(sorted(self.df[feature_x_name].unique()))


    def print_value_counts(self, feature_x_name:str, sortby:str):
        """    
        Input: 
        - Name of the feature to analyse.
        - A method/way to sort (index/values)
        """    
        print(f'\n{feature_x_name} value counts:')
        if sortby == 'index':
            print('Sorting by index:')
            print(self.df[feature_x_name].value_counts().sort_index())  
        else:
            print('Sorting by values:')
            print(self.df[feature_x_name].value_counts().sort_values())  
        

    def histogram(self, feature_x_name:str):
        """
        Plot histogram to check feature's distribution.
        Input: Name of the feature to analyse.
        """    
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(self.df[feature_x_name], bins=500)
        ax.set(title=f'Histogram of the continuous feature {feature_x_name}',
            xlabel=feature_x_name,
            ylabel='Frequency')
        plt.tight_layout()
        plt.show()


    def scatterplot(self, feature_x_name:str):
        """
        Input: Name of the feature to analyse.
        """
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(self.df[feature_x_name],
                self.df[self.target_feature_name], alpha=0.2)
        ax.set(title=f'{feature_x_name} vs {self.target_feature_name}',
            xlabel=feature_x_name,
            ylabel=self.target_feature_name)
        plt.tight_layout()
        plt.show()


    def continuous_trend_line_plot(self, feature_x_name:str):
        """
        Quantile cut x-axis feature and plot a line to study linear correlation with target variable.
        Input: Name of the feature (continuous) to analyse.
        """    
        # bin continuous feature into intervals and get mean feature_y/SalePrice per interval
        feature_interval = self.df.groupby(pd.qcut(self.df[feature_x_name],50, precision=0, duplicates='drop'))[self.target_feature_name].mean()

        fig, ax = plt.subplots(figsize=(8, 5))
        feature_interval.plot(kind='line', marker='o',ax=ax)
        ax.set(ylabel=f'Mean {self.target_feature_name}', title=f'Trend {feature_x_name} against mean {self.target_feature_name}')
        plt.tight_layout()
        plt.show()


    def barplot(self, feature_x_name:str):
        """
        Bar plot to check feature's distribution.
        Input: Name of the feature (discrete) to analyse.
        """
        print()
        # Bar plot a discrete feature to check its distribution
        bar_counts = self.df[feature_x_name].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(bar_counts.index, bar_counts.values, linewidth=0.8)
        ax.set(title=feature_x_name,
            xlabel=feature_x_name,
            ylabel='Frequency')
        plt.tight_layout()    
        plt.show()


    def boxplot_vs_target(self, feature_x_name:str):
        """
        Shows relationship between a discrete/ordinal feature and the target.
        Input: Name of the feature to analyse.
        """
        plt.figure(figsize=(10, 5))    
        sns.boxplot(data=self.df, x=feature_x_name, y=self.target_feature_name)
        plt.title(f'{feature_x_name} vs {self.target_feature_name} Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    def discrete_trend_line_plot(self, feature_x_name:str):
        """
        Plot a line to study linear correlation between feature object of study and target variable.
        Input: Name of the feature (discrete) to analyse.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        data_to_plot = self.df.groupby(feature_x_name)[self.target_feature_name].mean()
        ax.plot(data_to_plot, marker='o')
        ax.set(title=f'Mean {self.target_feature_name} per {feature_x_name}',
            ylabel=f'Mean {self.target_feature_name}')
        plt.tight_layout()
        plt.show()


    def groupby_feature_against_target_mean(self, feature_x_name:str):
        """
        Group by categories of a explanatory feature and bar plot it against the mean of the response variable.
        Input: Name of the feature (categorical) to analyse.
        """
        (self.df.groupby(feature_x_name)[self.target_feature_name]
            .agg(['mean'])
            .astype(int)
            .sort_values(by='mean', ascending=False)
            .plot(kind='barh', title=f'{feature_x_name} against mean {self.target_feature_name}'))
        plt.tight_layout()
        plt.show()


#####################################################################
    

    def analyse_categorical_feature(self, feature_x_name:str, n_unique:int):
        """
        Detects if feature has more than 15 categories or not, and displays plots and information accordingly.
        Input:
        - Name of the feature (categorical) to analyse.
        - Number of unique values of the feature.
        """
        print(f"\n{feature_x_name} has been detected as CATEGORICAL.")
        self.print_number_unique_values(feature_x_name)
        if n_unique <= self.discrete_threshold:
            self.print_value_counts(feature_x_name, sortby='index')
            self.barplot(feature_x_name)
            self.boxplot_vs_target(feature_x_name)
        else:            
            self.print_value_counts(feature_x_name, sortby='values')
            self.groupby_feature_against_target_mean(feature_x_name)


    def analyse_numerical_feature(self, feature_x_name:str, n_unique:int):
        """
        Detects if numeric feature is discrete (has no more than the threshold number of categories) or not, and displays plots and information accordingly.
        Input:
        - Name of the feature (numerical) to analyse.
        - Number of unique values of the feature.
        """
        self.print_description(feature_x_name)
        # numerical discrete
        if n_unique <= self.discrete_threshold:
            print(f"\n{feature_x_name} has been detected as numerical DISCRETE.")
            self.print_value_counts(feature_x_name, sortby='index')
            self.barplot(feature_x_name)
            self.boxplot_vs_target(feature_x_name)
            self.discrete_trend_line_plot(feature_x_name)
        # numerical continuous
        else:
            print(f"\n{feature_x_name} has been detected as numerical CONTINUOUS.")
            self.histogram(feature_x_name)
            self.scatterplot(feature_x_name)
            self.continuous_trend_line_plot(feature_x_name)
            

    def autoanalyse_feature(self, feature_x_name:str):
        """
        Detects whether a feature is categorical, numerical discrete or numerical continuous and accordingly displays information and visualizations to analyse the feature itself and the feature against the target
        Input:
        - feature: A pd.Series with name.
        - feature_x_name: A string containing the name of the feature to analyse.
        - df: A pd.DF.
        - target_feature_name: A string containing the name of the target feature.
        """    
        self.print_basic_info(feature_x_name)
        n_unique = self.df[feature_x_name].nunique()   

        # categorical features
        if not is_numeric_dtype(self.df[feature_x_name]):
            self.analyse_categorical_feature(feature_x_name, n_unique)

        # numerical features
        else:        
            self.analyse_numerical_feature(feature_x_name, n_unique)