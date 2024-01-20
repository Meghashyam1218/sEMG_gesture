import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Assuming your data is stored in a DataFrame named 'df1'
df = pd.read_csv("test.csv")

print(df["Gesture"])
# X=df1[['POT Value 1','POT Value 2']]
# y = df1['Gesture']


# # If not, you can read your data into a DataFrame using pd.read_csv() or another appropriate method
# scaler = MinMaxScaler()
# df = scaler.fit_transform(X)

# df=X
# df['Gesture']=y
# print(df)
# Calculate windowed average
window_size = 10  # Adjust the window size as needed
df["POT_Value_1_Wavg"] = df["POT Value 1"].rolling(window=window_size).mean()
df["POT_Value_2_Wavg"] = df["POT Value 2"].rolling(window=window_size).mean()

# Calculate windowed standard deviation
df["POT_Value_1_Wstd"] = df["POT Value 1"].rolling(window=window_size).std()
df["POT_Value_2_Wstd"] = df["POT Value 2"].rolling(window=window_size).std()

# Calculate mean absolute deviation
df["POT_Value_1_MAD"] = (
    df["POT Value 1"]
    .rolling(window=window_size)
    .apply(lambda x: np.mean(np.abs(x - x.mean())))
)
df["POT_Value_2_MAD"] = (
    df["POT Value 2"]
    .rolling(window=window_size)
    .apply(lambda x: np.mean(np.abs(x - x.mean())))
)

df["POT_Value_Delta"] = df["POT Value 2"] - df["POT Value 1"]
df["POT_Wavg_Delta"] = df["POT_Value_2_Wavg"] - df["POT_Value_1_Wavg"]
df["POT_Wstd_Delta"] = df["POT_Value_2_Wstd"] - df["POT_Value_1_Wstd"]
df["POT_MAD_Delta"] = df["POT_Value_2_MAD"] - df["POT_Value_1_MAD"]


# Drop NaN values resulting from the rolling calculations
df = df.dropna()

# Print the resulting DataFrame
print(df)

# Save the DataFrame to a new CSV file
# df.to_csv('all_output_data.csv', index=False)
