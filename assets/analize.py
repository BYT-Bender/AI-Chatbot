# Copyright © 2023 BYT-Bender

# Import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
from qbstyles import mpl_style


# Define the Graph class
class Graph:
    def __init__(self, config):
        self.config = config
        if self.config["graph_data"]["theme"].lower() == "dark":
            mpl_style(dark=True)
            self.facecolor = "#0c1c23"
        elif self.config["graph_data"]["theme"].lower() == "light":
            mpl_style(dark=False)
            self.facecolor = "#ffffff"

    # Create a bar chart to plot conversation usage
    def plot_conversation_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)
        conversation_df = pd.read_csv(self.config["data"]["conversation"]["usage"])

        plt.bar(conversation_df["id"], conversation_df["count"], color="b")
        plt.xticks(conversation_df["id"])

        if show_label:
            plt.xlabel("Response ID")
            plt.ylabel("Response Count")
        if show_title:
            plt.title("Response Distribution by ID")

        ax.set_axisbelow(True)
        plt.grid(axis="x")

        for i, count in enumerate(conversation_df["count"]):
            plt.text(conversation_df["id"][i], count, str(count), ha="center", va="bottom")

    # Create a bar chart to plot command usage
    def plot_command_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)

        command_df = pd.read_csv(self.config["data"]["command"]["usage"])

        plt.bar(command_df["id"], command_df["count"], color="b")
        plt.xticks(command_df["id"])

        if show_label:
            plt.xlabel("Command ID")
            plt.ylabel("Command Count")
        if show_title:
            plt.title("Command Distribution by ID")

        ax.set_axisbelow(True)
        plt.grid(axis="x")

        for i, count in enumerate(command_df["count"]):
            plt.text(command_df["id"][i], count, str(count), ha="center", va="bottom")

    # Create a pie chart to plot exit command usage
    def plot_exit_command_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)
        command_df = pd.read_csv(self.config["data"]["command"]["usage"])

        exit_commands_df = command_df.loc[command_df["id"].isin(self.config["graph_data"]["exit_commands"].values())]

        if show_label:
            label = self.config["graph_data"]["exit_commands"].keys()
        else:
            label = None

        plt.pie(
            exit_commands_df["count"],
            labels=label,
            autopct="%1.2f%%",
            pctdistance=0.80,
            explode=[0.02, 0.02, 0.02],
        )

        if show_title:
            plt.title("Exit Command Usage")

        hole = plt.Circle((0, 0), 0.65, facecolor=self.facecolor)
        ax.add_artist(hole)

    # Create a line chart to plot response usage over time
    def plot_response_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)
        response_df = pd.read_csv(self.config["data"]["common"]["response_usage"])

        grouped_data = (response_df.groupby(["date", "response_type"])["count"].sum().unstack(fill_value=0))

        x = grouped_data.index
        y_total = grouped_data.sum(axis=1)

        plt.plot(x, y_total, label="Total", marker=".", markersize=8)

        for response_type in self.config["graph_data"]["response_types"]:
            y = grouped_data[response_type].values
            plt.plot(x, y, label=response_type.capitalize(), linestyle="--")

        if show_label:
            plt.xlabel("Date")
            plt.ylabel("Count")

        if show_title:
            plt.title("Response Usage")

        plt.legend()

    def main(self):
        # Plot all charts and display them
        self.plot_conversation_usage(1, show_title=False, show_label=True)
        self.plot_command_usage(3, show_title=False, show_label=True)
        self.plot_exit_command_usage(2, show_title=False, show_label=True)
        self.plot_response_usage(4, show_title=False, show_label=True)

        plt.show()
