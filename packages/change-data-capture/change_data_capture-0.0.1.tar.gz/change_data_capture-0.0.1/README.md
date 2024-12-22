**Author: Dhivya Nagasubramanian**

**Purpose:**
Change data capture will be able to compare two datasets stored in pandas dataframe to identify Addition, deletions, and changed records. This is an effective ETL package that works seamlessly.

**Requirements packages:**

**NumPy** - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays. <br>
**pandas**  -  Dataframe utility. <br>


**Installation Instructions:**

pip install change-data-capture



**How to use it :**
There are two main functions of this framework.

**1. change_data_capture(Source_dataframe,new_dataframe,key_column)**

- This is the main functionionility for change data capture package that does the CDC.


**2. test_cdc_sample_data()**

- This would generate sample datasets to test the above function

   

**How to test the package with out data ?** 

**Step1** - Run with  "test_cdc_sample_data" by passing appropriate values 

eg: df_old, df_new = test_cdc_sample_data()


**Step2** - Run the cdc function  change_data_capture(Source_dataframe,new_dataframe,key_column)

eg: inserted_rows, filtered_df,deleted_rows = change_data_capture(Source_dataframe,new_dataframe,key_column)
   