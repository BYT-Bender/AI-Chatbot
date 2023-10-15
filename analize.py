import matplotlib.pyplot as plt
import pandas as pd

# Response by ID
response_df = pd.read_csv("assets/data/response_usage.csv")

plt.bar(response_df["id"], response_df["count"], color='b')
plt.xticks(response_df["id"])
plt.xlabel("Response ID")
plt.ylabel("Response Count")
plt.title("Response Distribution by ID")

plt.show()


# Command Usage by ID
command_df = pd.read_csv("assets/data/command_usage.csv")

plt.bar(command_df["id"], command_df["count"], color='b')
plt.xticks(command_df["id"])
plt.xlabel("Command ID")
plt.ylabel("Command Count")
plt.title("Command Distribution by ID")

plt.show()
