__author__ = "Saad Ahmad and Peter Herman"
__project__ = "gme.estimate"
__created__ = "05-24-2018"


import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from typing import Union
import statsmodels.api as sm
import time as time
import traceback

#-----------------------------------------------------------------------------------------#
# This file contains the underlying functions for the .estimate method in EstimationModel #
#-----------------------------------------------------------------------------------------#

# -----------
# Main function: Sequences the other routines
# -----------

def _estimate_ppml(data_frame,
                   meta_data,
                   specification,
                   fixed_effects: List[Union[str,List[str]]] = [],
                   drop_fixed_effect: Dict[Union[str, Tuple[str]],List[Union[str, Tuple[str]]]] = {},
                   cluster: bool=False,
                   cluster_on: str=None):
    '''
    Performs sector by sector GLM estimation with PPML diagnostics

    Args:
        data_frame: (Pandas.DataFrame) A dataframe containing data for estimation
        meta_data: (obj) a MetaData object from gme.EstimationData
        specification: (obj) a Specification object from gme.EstimationModel
        fixed_effects: (List[Union[str,List[str]]]) A list of variables to construct fixed effects based on.
            Can accept single string entries, which create fixed effects corresponding to that variable or lists of
            strings that create fixed effects corresponding to the interaction of the list items. For example,
            fixed_effects = ['importer',['exporter','year']] would create a set of importer fixed effects and a set of
            exporter-year fixed effects.
        drop_fixed_effect: (optional) Dict[Union[str,Tuple[str]],List[str]]
            A dictionary of fixed effect categories and names that are dropped from the fixed effects dataframe.
            drop_fixed_effect = {('importer','year'):[('ARG','2015'),('BEL','2013')]} would drop the
            fixed effects for importer-year: ARG-2015 and BEL-2013.
            The entry should be a subset of the list supplied for fixed_effects. 
    Returns: (Dict[GLM.fit], Pandas.DataFrame, Dict[DataFrame])
        1. Dictionary of statsmodels.GLM.fit objects with sectors as the keys.
        2. Dataframe with diagnostic information by sector
        3. Dictionary of estimation DataFrames + predicted trade values with sectors as the keys.
    '''

    post_diagnostics_data_frame_dict = {}
    results_dict = {}
    diagnostics_log = pd.DataFrame([])
    start_time = time.time()
    print('Estimation began at ' + time.strftime('%I:%M %p  on %b %d, %Y'))

    if not specification.sector_by_sector:
        data_frame = data_frame.reset_index(drop=True)
        fixed_effects_df = _generate_fixed_effects(data_frame, fixed_effects)
        fe_columns = list(fixed_effects_df.columns)
        estimating_data_frame = pd.concat([data_frame, fixed_effects_df], axis=1)
#       estimating_data_frame = pd.concat([data_frame[specification.lhs_var], data_frame[specification.rhs_var], fixed_effects_df], axis=1)
        model_fit, post_diagnostics_data_frame, diagnostics_log = _regress_ppml(estimating_data_frame, specification,fe_columns, drop_fixed_effect,cluster,cluster_on)
        
        results_dict['all'] = model_fit
                
        end_time = time.time()
        diagnostics_log.at['Completion Time'] = str(round((end_time - start_time)/60,2)) + ' minutes'
        post_diagnostics_data_frame_dict['all'] = post_diagnostics_data_frame


    else:
        sector_groups = data_frame.groupby(meta_data.sector_var_name)
        sector_list = _sectors(data_frame, meta_data)
        iteration_count = 1
        for sector in sector_list:
            sector_start_time = time.time()
            print('Sector ' + str(sector) + ' began at ' + time.strftime('%I:%M %p  on %b %d, %Y'))
            sector_data_frame = sector_groups.get_group(sector)
            sector_data_frame = sector_data_frame.reset_index(drop=True)

            # Create fixed effects
            fixed_effects_df = _generate_fixed_effects(sector_data_frame, fixed_effects)
            fe_columns = list(fixed_effects_df.columns)
            # Dataframe for estimations
            sector_data_frame = pd.concat([sector_data_frame, fixed_effects_df],axis=1)
            model_fit, post_diagnostics_data_frame, diagnostics_output = _regress_ppml(sector_data_frame, specification,fe_columns, drop_fixed_effect,cluster,cluster_on)

            # Timing reports
            sector_end_time = time.time()
            diagnostics_output.at['Sector Completion Time'] = (str(round((sector_end_time - sector_start_time) / 60, 2))
                                                               + ' minutes')
            if iteration_count > 1:
                average_time = ((time.time() - start_time) / 60) / iteration_count
                completion_time = (len(sector_list) - iteration_count) * average_time
                print("Average iteration time:  " + str(average_time) + "  minutes")
                print("Expected time to completion:  " + str(completion_time) + " minutes ("+ str(completion_time/60)
                      + " hours)\n")

            # Store results
            post_diagnostics_data_frame_dict[str(sector)] = post_diagnostics_data_frame
            results_dict[str(sector)] = model_fit
            diagnostics_log = pd.concat([diagnostics_log, diagnostics_output.rename(str(sector))], axis=1)
            iteration_count+=1

    print("Estimation completed at " + time.strftime('%I:%M %p  on %b %d, %Y'))
    return results_dict, diagnostics_log, post_diagnostics_data_frame_dict


# --------------
# Prep for Estimation Functions
# --------------
def _generate_fixed_effects(data_frame,
                            fixed_effects: List[Union[str, List[str]]] = []):
    '''
    Create fixed effects for single and interacted categorical variables.

    Args:
        data_frame: Pandas.DataFrame
            A DataFrame containing data for estimation.
        fixed_effects: List[Union[str,List[str]]]
            A list of variables to construct fixed effects based on.
            Can accept single string entries, which create fixed effects corresponding to that variable or lists of
            strings, which create fixed effects corresponding to the interaction of the list items. For example,
            fixed_effects = ['importer',['exporter','year']] would create a set of importer fixed effects and a set of
            exporter-year fixed effects.
    Returns: Pandas.DataFrame
        A DataFrame of fixed effects to be concatenated with the estimating DataFrame.
    '''

    fixed_effect_data_frame = pd.DataFrame([])
    # Get list for separate and combine fixed effect
    combined_fixed_effects = []
    separate_fixed_effects = []

    for item in fixed_effects:
        if type(item) is list:
            combined_fixed_effects.append(item)
        else:
            separate_fixed_effects.append(item)

    # Construct simple fixed effects
    for category in separate_fixed_effects:
        name = category + '_fe'
        temp_fe = pd.get_dummies(data_frame[category], prefix=name, dtype=int)
        fixed_effect_data_frame = pd.concat((fixed_effect_data_frame, temp_fe), axis=1)

    # Construct multiple fixed effects
    for item in combined_fixed_effects:
        if len(item) < 1:
            raise ValueError('A fixed_effects list element cannot be an empty list [].')

        if len(item) == 1:
            name = '_'.join(item) + '_fe'
            temp_fe = pd.get_dummies(data_frame[item[0]], prefix=name, dtype=int)
            fixed_effect_data_frame = pd.concat((fixed_effect_data_frame, temp_fe), axis=1)

        elif len(item) > 1:
            name = '_'.join(item) + '_fe'
            temp_data_frame = data_frame.loc[:, item]
            temp_data_frame.loc[:, name] = temp_data_frame.astype(str).sum(axis=1).copy()
            temp_fe = pd.get_dummies(temp_data_frame[name], prefix=name, dtype=int)
            fixed_effect_data_frame = pd.concat((fixed_effect_data_frame, temp_fe), axis=1)

    fixed_effect_data_frame = fixed_effect_data_frame.reset_index(drop=True)
    return fixed_effect_data_frame


def _drop_fe(data_frame,drop_dic):
    '''
    Drops user-provided fixed effect columns from a dataframe
    Arguments
    data_frame: Pandas.DataFrame
        A DataFrame containing data for estimation.
    drop_dic: Dict[Union[str,Tuple[str]],List[str]]
        A dictionary of fixed effect categories and names to be dropped from dataframe.
        drop_dic = {('importer','year'):[('ARG','2015'),('BEL','2013')]} would drop the
        fixed effect columns for importer-year: ARG-2015 and BEL-2013.
        The fixed effect categories should be a subset of the list supplied for fixed_effects. 
    Returns: (Pandas.DataFrame, List)
        1. A copy of the input data_frame with fixed effects columns removed
        2. List of fixed effect column names removed
    '''
        
    reduced_df=data_frame.copy()
    var_drop=[]
   
    #Check if values in dic are lists
    for key in drop_dic.keys():
        if isinstance(drop_dic[key],str):
                raise ValueError('Dropped Fixed Effect Names must be given as list or tuple')
    
    #Obtain the names to be dropped as a list of tuples
    for key in drop_dic.keys():
        for val in drop_dic[key]:
            if not isinstance(key,tuple):
                var_drop.append((key,val))
            else:   
                 var_drop.append(key+val)
   
    #Drop the columns from the dataframe that match the tuples
    column_drop=[]
    for var_tuple in var_drop:
        for col_name in reduced_df.columns:
            if all(drop_name in col_name for drop_name in var_tuple):
                reduced_df.drop(col_name, axis=1, inplace=True)
                column_drop.append(col_name)
    return reduced_df,column_drop

def _sectors(data_frame, meta_data):
    '''
    A function to extract a list of sectors from the estimating data_frame
    :param data_frame: (Pandas.DataFrame) A pandas data frmae to be used for estimation with a column defining
    sector or product IDs.
    :param meta_data: (obj) a MetaData object from gme.EstimationData
    :return: (list) a list of sorted sector IDs.
    '''
    sector_list = data_frame[meta_data.sector_var_name].unique()
    sector_list = np.ndarray.tolist(sector_list)
    sector_list.sort()
    return sector_list


# -------------
# PPML Regression and pre-diagnostics
# -------------


def _regress_ppml(data_frame, specification, fe_columns, drop_fixed_effect, cluster, cluster_on):
    '''
    Perform a GLM estimation with collinearity, insufficient variation, and overfit diagnostics and corrections.
    :param data_frame: (Pandas.DataFrame) A DataFrame for estimation
    :param specification: (obj) a Specification object from gme.EstimationModel
    :param specification: List of Fixed Effect columns in Dataframe
    :param drop_fixed_effect: (optional) A dictionary of FE categories and names to be dropped
    :return: (GLM.fit() obj, Pandas.DataFrame, Pandas.Series)
        1. The first returned object is a GLM.fit() results object containing estimates, p-values, etc.
        2. The second return object is the dataframe used for estimation that has problematic columns removed.
        3. A column containing diagnostic information from the different checks and corrections undertaken.
    '''
    # Check for zero trade fixed effects
    data_frame_copy = data_frame.copy()
    adjusted_data_frame, problem_variable_list, rhs_cols = _new_trade_contingent_collinearity_check(data_frame=data_frame_copy,
                                                                                      specification=specification, fe_columns=fe_columns)

    # Check for perfect collinearity and drop any user-specified FE
    rhs = adjusted_data_frame[rhs_cols] 
    adj_rhs,user_fe=_drop_fe(rhs,drop_fixed_effect)
    non_collinear_rhs, collinear_fe = _collinearity_check(adj_rhs)

    total_fe_drop=user_fe+collinear_fe
    if len(total_fe_drop) > 0:
        for col in total_fe_drop:
            adjusted_data_frame.drop(labels = col, axis = 1, inplace=True)
#
#    if len(collinear_column_list) == 0:
#        collinearity_indicator = 'No'
#    else:
#        collinearity_indicator = 'Yes'
    #collinearity_column = pd.Series({'Collinearities': collinearity_indicator})
    excluded_column_list = problem_variable_list + total_fe_drop
    exclusion_column = pd.Series({'Number of Regressors Dropped': len(excluded_column_list)})
    print('Omitted Regressors: ' + str(excluded_column_list))
   
    # GLM Estimation
    if cluster is False:
        try:
            estimates = sm.GLM(endog=adjusted_data_frame[specification.lhs_var],
                           exog=non_collinear_rhs,
                           family=sm.families.Poisson()
                           ).fit(cov_type=specification.std_errors,
                                 maxiter=specification.iteration_limit)
            adjusted_data_frame['predicted_trade'] = estimates.mu

        except:
            traceback.print_exc()
            estimates = 'Estimation could not complete.  GLM process raised an error.'
    else:
        try:

            model = sm.GEE(endog=adjusted_data_frame[specification.lhs_var],
                        exog=non_collinear_rhs,groups=adjusted_data_frame[cluster_on], 
                        family=sm.families.Poisson())
            
            estimates=model.fit()
            adjusted_data_frame['predicted_trade'] = model.predict(estimates.params)

        except:
            traceback.print_exc()
            estimates = 'Estimation could not complete.  GLM process raised an error.'
        
        
    # Checks for overfit (only valid when keep=False)
    try:
        fit_check_outcome = _overfit_check(data_frame=adjusted_data_frame,
                                           specification=specification,
                                           predicted_trade_column='predicted_trade')
        overfit_column = pd.Series({'Overfit Warning': fit_check_outcome})
    except:
        # CHECK THAT ESTIMATES DOES NOT GET USED LATER
        # Add something to return for diagnostics. I believe it needs to be a dataframe that can be combined
        overfit_column = pd.Series({'Overfit Warning': 'Estimation could not complete'})


    # Collect diagnostics
    diagnostics = pd.concat([overfit_column,exclusion_column])
    diagnostics.at['Regressors with Zero Trade'] =  problem_variable_list
    diagnostics.at['Regressors from User'] = user_fe
    diagnostics.at['Regressors Perfectly Collinear'] = collinear_fe
    
    return estimates, adjusted_data_frame, diagnostics


def _trade_contingent_collinearity_check(data_frame, specification):
    '''
    PPML diagnostic for columns that are collinear when trade is greater than zero, as in Santos and Silva (2011)
    Arguments
    :param data_frame: (Pandas.DataFrame) A DataFrame for estimation
    :param specification: (obj) a Specification object from gme.EstimationModel
    :return: (Pandas.DataFrame, list)
        1. A copy of the input data_frame with columns collinear when trade is greater than zero and associated
        observations removed
        2. List containing the names of the columns that were collinear when trade is greater than zero.
    '''

    # Main dataframe for manipulation
    data_frame_copy = data_frame.copy()

    # Identify problematic variables due to perfect collinearity when y>0
    nonzero_data_frame = data_frame_copy.loc[data_frame_copy[specification.lhs_var] > 0,:]
    lhs = [specification.lhs_var]
    rhs_columns = list(nonzero_data_frame.columns)
    rhs_columns.remove(specification.lhs_var)
    rhs = nonzero_data_frame[rhs_columns]
    noncollinear_columns, excluded_columns_list = _collinearity_check(rhs)
    rhs_columns = list(noncollinear_columns.columns)

    # Check if problematic and delete associated observations
    data_frame_copy['mask'] = 1
    problem_variable_list = []
    for col in excluded_columns_list:
        # mean_value = data_frame.loc[(data_frame_copy[specification.lhs_var] > 0),col].mean()
        mean_value = data_frame_copy[data_frame_copy[specification.lhs_var] > 0][col].mean()
        max_value = data_frame_copy[data_frame_copy[specification.lhs_var] == 0][col].max()
        min_value = data_frame_copy[data_frame_copy[specification.lhs_var] == 0][col].min()
        if min_value < mean_value and mean_value < max_value:
            rhs_columns.append(col)
        else:
            problem_variable_list.append(col)
            if data_frame_copy[col].nunique() == 2:
                data_frame_copy.loc[data_frame_copy[col] == 1, 'mask'] = 0

    # Return final data_frame with removed columns and observations
    data_frame_copy = data_frame_copy.loc[data_frame_copy['mask'] != 0,:]
    all = lhs + rhs_columns
    data_frame_copy = data_frame_copy[all]
    return data_frame_copy, problem_variable_list


def _collinearity_check(data_frame, tolerance_level=1e-05):
    '''
    Identifies and drops perfectly collinear columns
    :param data_frame: (Pandas.DataFrame) A DataFrame for estimation
    :param tolerance_level: (float) Tolerance parameter for identifying zero values (default=1e-05)
    :return: (Pandas.DataFrame) Original DataFrame with collinear columns removed
    '''

    data_array = data_frame.values
    q_factor, r_factor = np.linalg.qr(data_array)
    r_diagonal = np.abs(r_factor.diagonal())
    r_range = np.arange(r_diagonal.size)

    # Get list of collinear columns
    collinear_columns = np.where(r_diagonal < tolerance_level)[0]
    collinear_data_frame = data_frame.iloc[:, collinear_columns]
    collinear_column_list = list(collinear_data_frame.columns.values)

    # Get df with independent columns
    collinear_locations = list(collinear_columns)
    independent_columns = list(set(r_range).symmetric_difference(set(collinear_locations)))
    return data_frame.iloc[:, independent_columns], collinear_column_list


# ----------------
# Post-estimation Diagnostics
# ----------------

def _overfit_check(data_frame, specification: str = 'trade',
                   predicted_trade_column: str = 'predicted_trade'):
    '''
    Checks if predictions from GLM estimation are perfectly fitted arguments
    :param data_frame: (Pandas.DataFrame)
    :param specification:
    :param predicted_trade_column:
    :return:
    '''
    '''
    Checks if predictions from GLM estiamtion are perfectly fitted
    Arguments
    ---------
    first: DataFrame object
    second: String for variable name containing trade values (default='trade')
    third: String for variable name containing predicted trade values (defalt='ptrade')

    Returns
    -------
    String indicting if the predictions are perfectly fitted
    '''
    fit_check = 'No'
    non_zero = data_frame.loc[data_frame[specification.lhs_var] > 0,specification.lhs_var]
    low = non_zero.min() * 1e-6
    fit_zero_observations = data_frame.loc[data_frame[specification.lhs_var] == 0, predicted_trade_column]
    if fit_zero_observations.min() < low:
        fit_check = 'Yes'
    return fit_check

def _new_trade_contingent_collinearity_check(data_frame, specification, fe_columns):
    '''
    PPML diagnostic for columns that are collinear when trade is greater than zero, as in Santos and Silva (2011)
    Arguments
    :param data_frame: (Pandas.DataFrame) A DataFrame for estimation
    :param specification: (obj) a Specification object from gme.EstimationModel
    :fe_columns: List of fe_variables to be used in the estimation
    :return: (Pandas.DataFrame, list)
        1. A copy of the input data_frame with columns collinear when trade is greater than zero and associated
        observations removed
        2. List containing the names of the columns that were collinear when trade is greater than zero.
        3. List of remaining fixed effect columns
    '''

    # Main dataframe for manipulation
    data_frame_copy = data_frame.copy()

    # Identify problematic variables due to perfect collinearity when y>0
    nonzero_data_frame = data_frame_copy.loc[data_frame_copy[specification.lhs_var] > 0]

    orig_rhs_columns = specification.rhs_var + fe_columns
    rhs = nonzero_data_frame[orig_rhs_columns]
    noncollinear_columns, excluded_columns_list = _collinearity_check(rhs)
    new_rhs_columns = list(noncollinear_columns.columns)

    # Check if problematic and delete associated observations
    data_frame_copy['mask'] = 1
    problem_variable_list = []
    for col in excluded_columns_list:
        mean_value = data_frame_copy[data_frame_copy[specification.lhs_var] > 0][col].mean()
        max_value = data_frame_copy[data_frame_copy[specification.lhs_var] == 0][col].max()
        min_value = data_frame_copy[data_frame_copy[specification.lhs_var] == 0][col].min()
        if min_value < mean_value and mean_value < max_value:
            new_rhs_columns.append(col)
        else:
            problem_variable_list.append(col)
            if data_frame_copy[col].nunique() == 2:
                data_frame_copy.loc[data_frame_copy[col] == 1, 'mask'] = 0

    # Return final data_frame with removed columns and observations
    #data_frame_copy = data_frame_copy[data_frame_copy['mask'] != 0] #To account for FEs with non-zero trade
    drop_obs= data_frame_copy[(data_frame_copy[specification.lhs_var] == 0) & (data_frame_copy['mask']== 0)].index
    data_frame_copy.drop(drop_obs,inplace=True)
    
    drop_columns=problem_variable_list + ['mask']
    for col in drop_columns:
        data_frame_copy.drop(col, axis=1, inplace=True)

    return data_frame_copy, problem_variable_list, new_rhs_columns






