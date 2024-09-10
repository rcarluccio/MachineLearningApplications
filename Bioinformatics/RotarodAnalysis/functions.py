# Import libraries
import numpy as np
import pandas as pd

# Sample std per column
def get_std_percolumn(x):
    std_c = []
    for col in (x):
        std_c.append(np.sqrt(np.sum((abs(x[col] - x[col].mean())**2)/(len(x[col])-1))))
        
    return pd.Series(std_c)

    
# Define a function to compute row average
def row_average(row):
    return row.mean()

def row_std(row):
    return row.std()

def filtervalues (filter_vals, exercise_score):
# This function retrieves the age of death of the mouse from the first occurence of 0 into the exercise score tab
    def func(x):
        l = []
        for val in filter_vals:
            for col in exercise_score:
                if x[col] == val:
                    l.append(col)
                    
        return pd.Series(l)
        
    return exercise_score.apply(func, axis=1)[0]
    
# Extract data for plotting
def LatencyperGeno(df_test,exercise_score,genotype,sex):

    if (genotype =="All") and (sex=="None"):
        Cpko_data = exercise_score
    
    elif sex == "None":
        # extract data indepently from sex:
        Cpko_data = exercise_score.loc[(df_test[genotype] == True) ]
        
    elif sex != "None":
        # if the mouse has this mutation & sex:
        Cpko_data = exercise_score.loc[(df_test[genotype] == True) & (df_test[sex] == True)]
    
    def CalcMiceValues(Cpko_data):
    
        # Apply the row_average function to each row - per mouse - using the apply() method
        Cpko_exercise_avg_score_per_mouse = Cpko_data.apply(row_average, axis=1)

        # We get the mean of each column
        Cpko_mean_exercise_score =  Cpko_data.mean() # per column
        Cpko_std                 =  Cpko_data.std() # sample standard deviation, it's the same of get_std_percolumn
        
        # Z score
        z_score                  = (Cpko_data - Cpko_mean_exercise_score) / Cpko_std
        
        # Standard Error of the mean. The condition for using this as an estimate is that your sample size n is greater than 30 (given by the central limit theorem) and meets the independence condition n <= 10% of population size.
        Cpko_SE                 =  Cpko_std  / np.sqrt(len( Cpko_std))
        
        # Min-max normalisation
        Cpko_max_min             = np.max(Cpko_data) - np.min(Cpko_data)
        
        Cpko_mean_norm           = (Cpko_data  - Cpko_mean_exercise_score)/Cpko_max_min

        
        return Cpko_std, Cpko_mean_exercise_score, z_score, Cpko_SE
        
    return CalcMiceValues(Cpko_data)
