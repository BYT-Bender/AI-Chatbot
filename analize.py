import matplotlib.pyplot as plt
import pandas as pd
from qbstyles import mpl_style
import json

class Graph:
    def __init__(self, config):
        self.config = config
        if self.config["graph_data"]["theme"].lower() == "dark":
            mpl_style(dark=True)
            self.facecolor = "#0c1c23"
        elif self.config["graph_data"]["theme"].lower() == "light":
            mpl_style(dark=False)
            self.facecolor = "#ffffff"

    # Conversation Response by ID
    def plot_conversation_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)
        conversation_df = pd.read_csv(self.config["conversation_response_usage"])

        plt.bar(conversation_df["id"], conversation_df["count"], color='b')
        plt.xticks(conversation_df["id"])

        if show_label:
            plt.xlabel("Response ID")
            plt.ylabel("Response Count")
        if show_title:
            plt.title("Response Distribution by ID") 

        ax.set_axisbelow(True)
        plt.grid(axis="x")

        for i, count in enumerate(conversation_df["count"]):
            plt.text(conversation_df["id"][i], count, str(count), ha='center', va='bottom')

    # Command Usage by ID
    def plot_command_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)

        command_df = pd.read_csv(self.config["command_usage"])

        plt.bar(command_df["id"], command_df["count"], color='b')
        plt.xticks(command_df["id"])

        if show_label:
            plt.xlabel("Command ID")
            plt.ylabel("Command Count")
        if show_title:
            plt.title("Command Distribution by ID")

        ax.set_axisbelow(True)
        plt.grid(axis="x")

        for i, count in enumerate(command_df["count"]):
            plt.text(command_df["id"][i], count, str(count), ha='center', va='bottom')

    # Exit Command Usage
    def plot_exit_command_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)
        command_df = pd.read_csv(self.config["command_usage"])
        
        exit_commands_df = command_df.loc[command_df['id'].isin(self.config["graph_data"]["exit_commands"].values())]

        if show_label:
            label = self.config["graph_data"]["exit_commands"].keys()
        else:
            label = None

        plt.pie(exit_commands_df["count"], labels = label, autopct='%1.2f%%', pctdistance=0.80, explode=[0.02, 0.02, 0.02])
        
        if show_title:
            plt.title("Exit Command Usage")

        hole = plt.Circle((0, 0), 0.65, facecolor=self.facecolor)
        ax.add_artist(hole)

    def plot_response_usage(self, position, show_title=True, show_label=True):
        ax = plt.subplot(2, 2, position)
        response_df = pd.read_csv(self.config["response_usage"])

        grouped_data = response_df.groupby(["date", "response_type"])["count"].sum().unstack(fill_value=0)

        x = grouped_data.index
        y_total = grouped_data.sum(axis=1)

        plt.plot(x, y_total, label="Total", marker = '.', markersize = 8)

        for response_type in self.config["graph_data"]["response_types"]:
            y = grouped_data[response_type].values
            plt.plot(x, y, label=response_type.capitalize(), linestyle = '--')
            
        if show_label:
            plt.xlabel("Date")
            plt.ylabel("Count")

        if show_title:
            plt.title("Response Usage")

        plt.legend()


    def main(self):
        self.plot_conversation_usage(1, show_title=False, show_label=True)
        self.plot_command_usage(3, show_title=False, show_label=True)
        self.plot_exit_command_usage(2, show_title=False, show_label=True)
        self.plot_response_usage(4, show_title=False, show_label=True)

        # plt.tight_layout()
        plt.show()
    

# def load_config(config_file):
#     try:
#         with open(config_file, "r") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         raise Exception(f"Config file '{config_file}' not found.")
#     except Exception as error:
#         raise Exception(f"Error loading configuration: {error}")
    
# if __name__ == "__main__":
#     config_file = "config.json"
#     config = load_config(config_file)
    
#     graph = Graph(config)
#     graph.main()
