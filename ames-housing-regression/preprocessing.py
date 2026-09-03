import eda_tools

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import sklearn

from pandas.api.types import is_numeric_dtype 

from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor, VotingRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, OrdinalEncoder, StandardScaler, PowerTransformer
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, cross_val_predict, KFold, RandomizedSearchCV



###------------------------------#####
###      PREPROCESSING TOOLS
###------------------------------#####

def print_features_to_process(roadmap, strategy):
    """Loops through the roadmap dictionary and prints name and reason fields per feature if that strategy key's value is True. """
    if strategy == None:
        return
    for feature, task in roadmap.items():
        if task[strategy] == True:
            print(f'{feature}\n{task["reason"]} \n')



###------------------------------#####
###         TRANSFORMERS
###------------------------------#####


### DROPPING COLUMNS ### -----------------------

# columns that need to be dropped
cols_drop = ['Id', 'GarageCond', 'ScreenPorch', 'PoolQC', 'PoolArea', 'MiscFeature', 'Condition2', 'KitchenAbvGr', 'Street', 'Heating', 'BsmtHalfBath', 'Utilities', 'MiscVal']


# columns that need to be inputed the value 'missing'
cols_impute_missing = ['BsmtQual', 'FireplaceQu', 'BsmtExposure', 'GarageFinish', 'GarageYrBlt', 'GarageType', 'BsmtFinType1', 'MasVnrType', 'GarageQual', 'Fence', 'BsmtCond', 'BsmtFinType2', 'Alley', 'Electrical']


# column transformer to drop columns
drop_transformer = ColumnTransformer(
    transformers=[
        ('drop_out', 'drop', cols_drop)
    ],
    remainder='passthrough',
    verbose_feature_names_out=False,
    n_jobs=-1
)


### IMPUTING VALUES ### -----------------------

# column transformer to impute values
impute_transformer = ColumnTransformer(
    transformers=[
        ('imputer_missing', SimpleImputer(strategy='constant', fill_value='missing'), cols_impute_missing),
        ('imputer_median', SimpleImputer(strategy='median'), ['MasVnrArea']),
        ('imputer_zero', SimpleImputer(strategy='constant', fill_value=0),['LotFrontage'])
    ],
    remainder='passthrough',
    verbose_feature_names_out=False,
    n_jobs=-1
)


### GROUPING CATEGORIES ### -----------------------

# column transformer to group categories
group_cat_transformer = ColumnTransformer(
    transformers=[
        ('group_neighborhood', FunctionTransformer(lambda x: x.replace(['NPkVill', 'Blueste'], 'rare'), feature_names_out='one-to-one'),['Neighborhood']),

        ('group_SaleCondition', FunctionTransformer(lambda x:x.replace(['AdjLand', 'Alloca', 'Family'], 'rare_SaleCondition'), feature_names_out='one-to-one'), ['SaleCondition']),

        ('group_GarageType', FunctionTransformer(lambda x:x.replace(['2Types', 'CarPort','Basment'], 'rare_garage_type'), feature_names_out='one-to-one'), ['GarageType']),

        ('group_SaleType', FunctionTransformer(lambda x:x.where(x.isin(['WD', 'New']), 'rare_SaleType'), feature_names_out='one-to-one'), ['SaleType']), 

        ('group_Functional', FunctionTransformer(lambda x:x.where(x.isin(['Typ']), 'no_typ'), feature_names_out='one-to-one'), ['Functional']), # function df.where() keeps value where True (opposite of df.mask())
        
        ('group_RoofStyle', FunctionTransformer(lambda x:x.where(x.isin(['Gable', 'Hip']), 'rare_RoofStyle'), feature_names_out='one-to-one'), ['RoofStyle']),         

        ('group_Foundation', FunctionTransformer(lambda x:x.mask(x.isin(['Wood', 'Slab', 'Stone']), 'rare_Foundation'), feature_names_out='one-to-one'), ['Foundation']), # function df.mask() replaces value where True       
        
        ('group_LotConfig', FunctionTransformer(lambda x:x.mask(x.isin(['FR2', 'FR3']), 'rare_LotConfig'), feature_names_out='one-to-one'), ['LotConfig']),

        ('group_LotShape', FunctionTransformer(lambda x:x.mask(x.isin(['IR2', 'IR3']), 'rare_LotShape'), feature_names_out='one-to-one'), ['LotShape']),

        ('group_HeatingQC', FunctionTransformer(lambda x:x.mask(x.isin(['Fa', 'Po']), 'ba_HeatingQC'), feature_names_out='one-to-one'), ['HeatingQC']),

        ('group_HouseStyle', FunctionTransformer(lambda x:x.mask(x.isin(['2.5Fin', '2.5Unf', '1.5Unf']), 'rare_HouseStyle'), feature_names_out='one-to-one'), ['HouseStyle']),        

        ('group_GarageQual', FunctionTransformer(lambda x:x.mask(x.isin(['Ex', 'Gd', 'TA']), 'GQ_abv_av').mask(x.isin(['Po', 'Fa']), 'GQ_bel_av'), feature_names_out='one-to-one'), ['GarageQual']),

        ('group_Fence', FunctionTransformer(lambda x:x.mask(x.isin(['MnWw','MnPrv']), 'minimum_Fence'), feature_names_out='one-to-one'), ['Fence']),

        ('group_Exterior1st', FunctionTransformer(lambda x:x.mask(x.isin(['AsphShn', 'ImStucc', 'CBlock', 'BrkComm', 'Stone', 'AsbShng', 'Stucco', 'WdShing']), 'rare_Exterior1st'), feature_names_out='one-to-one'), ['Exterior1st']),

        ('group_MSSubClass', FunctionTransformer(lambda x:x.mask(x.isin([40, 180, 45, 75, 85]), 0), feature_names_out='one-to-one'), ['MSSubClass']),

        ('group_ExterCond', FunctionTransformer(lambda x:x.mask(x.isin(['Ex', 'Gd', 'TA']), 'EC_abv_av').mask(x.isin(['Po', 'Fa']), 'EC_bel_av'), feature_names_out='one-to-one'), ['ExterCond']),

        ('group_Exterior2nd', FunctionTransformer(lambda x:x.mask(x.isin(['AsphShn', 'ImStucc', 'CBlock', 'Brk Cmn', 'BrkFace', 'Stone', 'AsbShng', 'Stucco', 'Other']), 'rare_Exterior2nd'), feature_names_out='one-to-one'), ['Exterior2nd']),

        ('group_BsmtCond', FunctionTransformer(lambda x:x.mask(x.isin(['Po', 'Fa']), 'below_typical_BC'), feature_names_out='one-to-one'), ['BsmtCond']),

        ('group_Electrical', FunctionTransformer(lambda x:x.mask(x.isin(['missing', 'Mix', 'FuseP', 'FuseF']), 'rare_Electrical'), feature_names_out='one-to-one'), ['Electrical']),
        
        ('group_LandSlope', FunctionTransformer(lambda x:x.where(x.isin(['Gtl']), 'no_Gtl'), feature_names_out='one-to-one'), ['LandSlope']),
        
        ('group_BsmtFinType2', FunctionTransformer(lambda x:x.where(x.isin(['Unf']), 'no_Unf'), feature_names_out='one-to-one'), ['BsmtFinType2']),
        
        ('group_RoofMatl', FunctionTransformer(lambda x:x.where(x.isin(['CompShg']), 'no_CompShg'), feature_names_out='one-to-one'), ['RoofMatl']),

    ],
    remainder='passthrough',
    verbose_feature_names_out=False,
    n_jobs=-1
)


### CLIPPING VALUES ### -----------------------

# column transformer to clip values
clip_transformer = ColumnTransformer(
    transformers=[
        ('clip_OverallCond', FunctionTransformer(lambda x: x.clip(lower=3), feature_names_out='one-to-one'), ['OverallCond']),
        ('clip_BedroomAbvGr', FunctionTransformer(lambda x: x.clip(lower=2, upper=5), feature_names_out='one-to-one'), ['BedroomAbvGr']),
        ('clip_to_one', FunctionTransformer(lambda x: x.clip(upper=1), feature_names_out='one-to-one'), ['BsmtFinSF2', '3SsnPorch', 'LowQualFinSF']),
       
    ],
    remainder='passthrough',
    verbose_feature_names_out=False,
    n_jobs=-1
)


### ENCODING VALUES ### -----------------------

# custom function to map values for feature HeatingQC
def heatingqc_map(df):
    # assign values to map/encode C
    map = {'Ex':3, 'Gd':2, 'TA':1, 'ba_HeatingQC':0}     
    return pd.DataFrame(df).iloc[:,0].map(map).to_frame()

# columns that drop missing as the reference category
cols_drop_missing_cat = ['BsmtQual', 'FireplaceQu', 'BsmtCond', 'BsmtExposure', 'GarageFinish', 'GarageType', 'BsmtFinType1', 'MasVnrType', 'GarageQual', 'Fence', 'Alley']

# columns that drop first as the reference category
cols_drop_first_cat = ['ExterQual', 'KitchenQual', 'Neighborhood', 'YrSold', 'MSZoning', 'SaleCondition', 'LandContour', 'Condition1', 'MoSold', 'BedroomAbvGr', 'SaleType', 'BldgType', 'RoofStyle', 'Foundation', 'LotConfig', 'LotShape', 'HouseStyle', 'Exterior1st','MSSubClass', 'Exterior2nd', 'PavedDrive', 'Electrical']

# columns to binary encode
cols_binary_encode = ['CentralAir', 'Functional', 'LandSlope', 'ExterCond', 'BsmtFinType2']

# column transformer to encode
encode_transformer = ColumnTransformer(
    transformers=[

        ('OHE_missing', OneHotEncoder(handle_unknown='ignore',
                        sparse_output=False,
                        drop=['missing'] * len(cols_drop_missing_cat)), cols_drop_missing_cat),

        ('OHE_first', OneHotEncoder(handle_unknown='ignore',
                                    sparse_output=False,
                                    drop='first'), cols_drop_first_cat),

        ('simple_encoder', OrdinalEncoder(handle_unknown='use_encoded_value',
                                          unknown_value=2), cols_binary_encode),

        ('map_heatingqc', FunctionTransformer(heatingqc_map,
                                              feature_names_out='one-to-one'),['HeatingQC']),
        
        ## map_heatingqc transformer is mapping the quality rank to integers. The same would've been achieved with the following transformer:
        
        ##('OHE', OrdinalEncoder(categories=[['ba_HeatingQC', 'TA', 'Gd', 'Ex']], handle_unknown='use_encoded_value', unknown_value=-1), ['HeatingQC']) 

    ],
    remainder='drop',
    verbose_feature_names_out=False,
    n_jobs=-1
)


###------------------------------#####
###         PREPROCESSORS
###------------------------------#####

# first version of the preprocessor with the bare minimum preprocessing steps
preprocessor_v0 = Pipeline(steps=[
    ('drop_transformer', drop_transformer),
    ('impute_transformer', impute_transformer),
    ('group_transformer', group_cat_transformer),
    ('clip_transformer', clip_transformer),
    ('encode_transformer', encode_transformer)])
