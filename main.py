from src.preprocessing import preprocess
from src.feature_engineering import (
    create_ratio_features,
    create_spending_features,
    create_credit_features
)

df = preprocess()

df = create_ratio_features(df)

df = create_spending_features(df)

df= create_credit_features(df)

print(df[
    [
        "credit_utilization",
        "credit_cushion",
        "available_credit",
        "revolve_percentage"
    ]
].head())

print(df.shape)