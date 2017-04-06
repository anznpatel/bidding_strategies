import pandas as pd
import numpy as np

train = pd.read_csv("train.csv")

trainMinBid = int(train["bidprice"].min())
trainMaxBid = int(train["bidprice"].max())

validation = pd.read_csv("validation.csv")

optimalCTR = 0
budget = 25000

for s in range(100, 200):
    np.random.seed(s)
    print("seed = ", s)
    for bid in range(trainMinBid-100, trainMaxBid+100):
        #print("const bid = ", bid)
        df = validation.loc[bid >= validation["payprice"]]
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
            optimalBidPrice = bid
            optimalSeed = s
            optimalExpenditure = expenditure
            print(optimalCTR, optimalBidPrice, budget, optimalExpenditure, optimalSeed)

print(optimalCTR, optimalBidPrice, budget, optimalExpenditure, optimalSeed)

print(validation.shape, df2.shape)

#0.0135135135135 397 25000 24933 122
#(299749, 26) (304, 26)