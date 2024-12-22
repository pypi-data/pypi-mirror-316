import pandas as pd
import numpy as np

def change_data_capture(Source_dataframe,new_dataframe,key_column):
    df_old = Source_dataframe
    df_new = new_dataframe
    
    df_old = df_old.sort_values(by=key_column).reset_index(drop=True)
    df_new = df_new.sort_values(by=key_column).reset_index(drop=True)

    
    if len(key_column) > 1:
        df_old['key'] = df_old[key_column].astype(str).fillna('').agg('-'.join, axis=1)
        df_new['key'] = df_new[key_column].astype(str).fillna('').agg('-'.join, axis=1)
        key = 'key'

    else:    
        key = key_column[0]
    
    inserted_rows = df_new[~df_new[key].isin(df_old[key])]
    
    deleted_rows = df_old[~df_old[key].isin(df_new[key])]
    non_key_columns = [col for col in df_old.columns if col != key]
    merged_df = pd.merge(df_old, df_new, on=key,how = 'inner', suffixes=('_old', '_new'))
    for col in non_key_columns:
        old_col = col+'_old'
        new_col = col+'_new'
        flg_col = col+'_flg'
        merged_df[flg_col] = np.where( merged_df[old_col] == merged_df[new_col] , True, False)
    flag_columns = merged_df.filter(regex='_flg').columns
    rows_with_false_flags = merged_df[flag_columns].apply(lambda row: (row == False).any(), axis=1)
    filtered_df = merged_df[rows_with_false_flags]
    return inserted_rows, filtered_df,deleted_rows

 def test_cdc_sample_data():
    df_old = pd.DataFrame({
    'col1': ['A','B', 'C', 'D'],
    'col2': [0,1, 3, 4],
    'col3': ['X','Y', 'Z', 'W'],
    'col4': [100,200, 600, 400]})

    df_new = pd.DataFrame({
    'col1': ['B', 'C', 'D', 'E'],  # Added 'E'
    'col2': [1, 3, 4, 5],           # New values for 'E'
    'col3': ['X', 'Y', 'W', 'V'],
    'col4': [100, 300, 400, 500]})
    return df_old, df_new