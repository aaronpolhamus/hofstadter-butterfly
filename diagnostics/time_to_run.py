"""
Run this after you've run benchmarks.py to get the /tmp/runtimes.csv data
"""
import pandas as pd
from statsmodels.regression.linear_model import OLS

df = pd.read_csv('/tmp/runtimes.csv')
df['constant'] = 1
df['resolution_sq'] = df['resolution'] ** 2
quad_model = OLS(df['avg_time'], df[['resolution_sq', 'resolution', 'constant']]).fit()
quad_model.summary()
