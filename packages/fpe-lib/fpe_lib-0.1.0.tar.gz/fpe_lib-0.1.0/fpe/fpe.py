import pandas as pd
import numpy as np
import numbers
import warnings

warnings.filterwarnings('ignore')

def fpefs(data):
    # Ensure the input is a DataFrame
    df = pd.DataFrame(data)
    col = len(df.columns)
    nfeatures = col - 1
    del df  # Release memory
    X = data.iloc[:, 0:nfeatures]
    y = pd.Series(data.iloc[:, -1])  # Ensure y is a Series
    
    # Normalize numeric features
    for f in range(nfeatures):
        K = X.iloc[:, f]
        da = K.iloc[0]
        if isinstance(da, (numbers.Number, numbers.Real)) and (K.max() - K.min()) > 0:
            K = round(((K - K.min()) / (K.max() - K.min())), 2)
            X.loc[:, f] = K
    
    # Unique function
    def get_unique(list1):
        return list(set(list1))
    
    label = get_unique(y)
    numberOfLabel = len(label)
    Prob = []
    
    # Calculate probabilities
    for j in range(nfeatures):
        mu, ncount, Pvalue = 0, 0, 0
        dp = pd.Series(X.iloc[:, j])
        md = dp.groupby(dp).apply(lambda px: px.index.tolist()).to_dict()
        ulist = md.keys()
        sizeulist = len(ulist)
        
        for m in ulist:
            mlist = []
            mindex = md[m]
            for idx in mindex:
                if y[idx] not in mlist:
                    mlist.append(y[idx])
                if numberOfLabel == len(mlist):
                    break
            nc = len(mlist)
            if nc < numberOfLabel:
                mu += float(nc) / numberOfLabel
                ncount += 1
        
        if ncount > 0:
            Pvalue = round((1 - (0.5) * ((sizeulist - ncount) / sizeulist + mu / ncount)), 2)
        
        Prob.append(Pvalue)
        print(j, mu, ncount, sizeulist, Pvalue)
    
    # Prepare output
    Prob = pd.Series(Prob)
    estimatedProbability = pd.DataFrame({
        "Feature": X.columns,
        "Probability": Prob
    })
    return estimatedProbability
