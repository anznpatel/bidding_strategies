import pandas as pd
import numpy as np

validation = pd.read_csv("validation.csv")

optimalCTR = 0
budget = 25000

for s in range(100, 120):
    np.random.seed(s)
    print("seed = ", s)
    for minBid in range(100, 120):
        for maxBid in range(250, 270):
            rand_bidprices = np.random.choice(range(minBid, maxBid), validation.shape[0])
            df = validation.loc[rand_bidprices >= validation["payprice"]]
            meanPayPrice = df["payprice"].mean()
            idx = np.random.choice(range(0, df.shape[0]-1), int(budget/meanPayPrice))
            df2 = df.iloc[idx, :]
            expenditure = df2["payprice"].sum()
            while expenditure > budget:
                idx = np.random.choice(range(0, df2.shape[0]-1), 1)
                df2 = df2.drop(df2.index[[idx]])
                expenditure = df2["payprice"].sum()
            ctr = df2["click"].mean()
            if ctr > optimalCTR:
                optimalCTR = ctr
                avgBidPrice = df2["bidprice"].mean()
                optimalSeed = s
                optimalExpenditure = expenditure
                print(optimalCTR, avgBidPrice, budget, optimalExpenditure, optimalSeed)

print(optimalCTR, avgBidPrice, budget, optimalExpenditure, optimalSeed)

print(validation.shape, df2.shape)

#0.0109589041096 273.690410959 25000 24982 106
#(299749, 26) (359, 26)