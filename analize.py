import matplotlib.pyplot as plt
import pandas as pd
from qbstyles import mpl_style

mpl_style(dark=True)

# Conversation Response by ID
def plot_conversation_usage():
    ax = plt.subplot(2, 2, 1)
    conversation_df = pd.read_csv("assets/data/conversation_response_usage.csv")

    plt.bar(conversation_df["id"], conversation_df["count"], color='b')
    plt.xticks(conversation_df["id"])
    plt.xlabel("Response ID")
    plt.ylabel("Response Count")
    # plt.title("Response Distribution by ID") 

    ax.set_axisbelow(True)
    plt.grid(axis="x")

    for i, count in enumerate(conversation_df["count"]):
        plt.text(conversation_df["id"][i], count, str(count), ha='center', va='bottom')

# Command Usage by ID
def plot_command_usage():
    ax = plt.subplot(2, 2, 3)

    command_df = pd.read_csv("assets/data/command_usage.csv")

    plt.bar(command_df["id"], command_df["count"], color='b')
    plt.xticks(command_df["id"])
    plt.xlabel("Command ID")
    plt.ylabel("Command Count")
    # plt.title("Command Distribution by ID")

    ax.set_axisbelow(True)
    plt.grid(axis="x")

    for i, count in enumerate(command_df["count"]):
        plt.text(command_df["id"][i], count, str(count), ha='center', va='bottom')

# Exit Command Usage
def plot_exit_command_usage():
    ax = plt.subplot(2, 2, 2)
    command_df = pd.read_csv("assets/data/command_usage.csv")

    exit_commands = {
        "exit()": 1,
        "quit()": 2,
        "Ctrl + C": 3
    }

    exit_commands_df = command_df.loc[command_df['id'].isin(exit_commands.values())]

    plt.pie(exit_commands_df["count"], labels = exit_commands.keys(), autopct='%1.2f%%', pctdistance=0.80, explode=[0.02, 0.02, 0.02])
    # plt.title("Exit Command Usage")

    hole = plt.Circle((0, 0), 0.65, facecolor='#0c1c23')
    ax.add_artist(hole)


plot_conversation_usage()
plot_command_usage()
plot_exit_command_usage()

# plt.tight_layout()
plt.show()
