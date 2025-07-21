def apply_bell_curve(df, column_name, target_mean=10, target_std=3):
    """
    Applies a bell curve transformation to a specified column.

    This function standardizes the original scores (calculates z-scores) and then
    scales them to a new distribution defined by the target mean and standard deviation.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        column_name (str): The name of the column to apply the curve to.
        target_mean (int): The desired mean for the new distribution.
        target_std (int): The desired standard deviation for the new distribution.

    Returns:
        pd.DataFrame: The DataFrame with the new 'curved_fine_count' column.
    """
    original_scores = df[column_name]
    
    # If there's no variation in scores, the standard deviation is 0.
    # To avoid division by zero, we can just set all curved scores to the target mean.
    if original_scores.std() == 0:
        df['curved_fine_count'] = target_mean
        return df

    # 1. Calculate the Z-score for each fine count.
    # Z-score = (value - mean) / standard_deviation
    z_scores = (original_scores - original_scores.mean()) / original_scores.std()

    # 2. Scale the Z-scores to the new target distribution.
    curved_scores = z_scores * target_std + target_mean
    
    # 3. Add the new scores to the DataFrame.
    # Round to the nearest whole number and ensure no fines are negative.
    df['curved_fine_count'] = curved_scores.round().astype(int)
    df['curved_fine_count'] = df['curved_fine_count'].clip(lower=0)
    
    return df