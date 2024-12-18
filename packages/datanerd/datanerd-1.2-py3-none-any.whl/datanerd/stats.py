import pandas as pd
import numpy as np

def stats(df):
    df_stats=pd.DataFrame()
    df_stats=df.describe(percentiles=[.1,.2,.25,.3,.4,.5,.6,.7,.75,.8,.9,.95,.99]).T
    dfMissing=((df.isna().sum()/len(df))*100).to_frame('%ofMissingValues')
    dfUnique=df.apply(lambda x: x.nunique(dropna=False), axis=0).to_frame("#ofUniqueValues")
    stats=pd.concat([df_stats,dfMissing,dfUnique],ignore_index=False,axis=1)
    return stats
