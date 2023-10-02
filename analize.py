import matplotlib.pyplot as plt
import pandas as pd

response_df = pd.read_csv("data/response_data.csv")

plt.bar(response_df["id"], response_df["count"], color='b')
plt.xticks(response_df["id"])
plt.xlabel("Response ID")
plt.ylabel("Response Count")
plt.title("Response Distribution by ID")

plt.show()