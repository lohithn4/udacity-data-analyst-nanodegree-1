#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    
    residual_errors = []
    
    for prediction, real in zip(predictions, net_worths):
        residual_errors.append((real - prediction)**2)
        
    cleaned_data = zip(ages, net_worths, residual_errors)
    
    cleaned_data.sort(key = lambda t: t[2])
        
    total_cleaned = len(cleaned_data) * 0.1 # 10% 
    
    for i in range(0, int(total_cleaned)):
        cleaned_data.pop()
    
    return cleaned_data

