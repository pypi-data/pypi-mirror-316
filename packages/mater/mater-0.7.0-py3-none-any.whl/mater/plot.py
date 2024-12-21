"""Create a UI to plot and filter the outputs"""

import argparse
import os
from typing import Dict, List

import darkdetect
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from mater import Mater

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--output-folder", type=str, help="Name of the folder where the outpus are stored.")

# Parse the arguments
args = parser.parse_args()

# Detect the system theme
if darkdetect.isDark():
    plt.style.use("dark_background")  # Use Matplotlib's dark theme
else:
    plt.style.use("default")  # Use the default (light) theme


# Define a callback to update session state
def update_time():
    st.session_state.time_value = st.session_state.time


def update_times():
    st.session_state.times_value = st.session_state.times


@st.cache_data
def get_data_list(run_name: str):
    run_folder_path = os.path.join(os.getcwd(), run_name)
    data_list = os.listdir(run_folder_path)
    return data_list


@st.cache_data
def get_data(data_name: str, run_name: str):
    model = Mater()
    model.run_name = run_name
    df = model.get(data_name)
    # Groupby to get rid off age_cohort
    level_list = list(df.index.names)
    if "age_cohort" in level_list:
        level_list.remove("age_cohort")
        df = df.groupby(level=level_list).sum()
    return df


@st.cache_data
def df_filtering(df: pd.DataFrame, level_values: Dict[str, List[str]]):
    # Filter the dataframe to plot : create a mask
    index = pd.MultiIndex.from_product(
        [level_values[level] for level in level_values.keys()], names=level_values.keys()
    )
    mask = pd.DataFrame(data=1, index=index, columns=df.columns)

    # Filter the dataframe to plot with the element selection
    filtered_df = df.mul(mask).dropna(how="all")
    return filtered_df


def plot_df(df: pd.DataFrame, plot: bool, all_data: bool, plot_type: str):
    if plot & all_data:
        # Select time
        min_time = df.columns.min()
        max_time = df.columns.max()
        if plot_type == "pie":
            # Initialize session state for the slider
            if "time_value" not in st.session_state:
                st.session_state.time_value = max_time  # Default value
            time = st.sidebar.slider(
                "time",
                min_time,
                max_time,
                value=st.session_state.time_value,  # Use session state as initial value
                key="time",
                on_change=update_time,
            )
            # plot
            fig, ax = plt.subplots()
            df[time].T.plot(ax=ax, kind=plot_type, autopct="%1.1f%%")
            ax.set_title(data_name)
            st.pyplot(fig)
        else:
            # Initialize session state for the slider
            if "times_value" not in st.session_state:
                st.session_state.times_value = (min_time, max_time)  # Default value
            time_steps = st.sidebar.slider(
                "time",
                min_time,
                max_time,
                (st.session_state.times_value[0], st.session_state.times_value[1]),
                key="times",
                on_change=update_times,
            )
            df_time_filtered = df.loc[:, time_steps[0] : time_steps[1]]
            if plot_type == "table":
                st.dataframe(df_time_filtered, use_container_width=True)
            else:
                # plot
                fig, ax = plt.subplots()
                df_time_filtered.T.plot(ax=ax, kind=plot_type)
                ax.set_title(data_name)
                st.pyplot(fig)


# Main app

st.sidebar.title("MATER visualization")

# Get the list of the data available for plotting
output_folder = args.output_folder
data_list = get_data_list(output_folder)

# Create the data selector
data_name = st.sidebar.selectbox("data", data_list)

# Retrieve the dataframe (cached data)
df = get_data(data_name, output_folder)

# visualization type
plot_types = ["line", "area", "pie", "table"]
plot_type = st.sidebar.radio("visualization type", plot_types, horizontal=True)

# plot ?
plot = True
# all data ?
all_data = True

# Select item
level_values = {}
st.sidebar.header("Element selection")
for level in df.index.levels:
    item_list = list(level.unique())
    data = st.sidebar.multiselect(level.name, item_list, item_list[0])
    if not data:
        st.error(f"Please select at least one {level.name}.")
        all_data = False
    level_values[level.name] = data

filtered_df = df_filtering(df, level_values)
if filtered_df.empty & all_data:
    st.error("Please select another element combination.")
    plot = False

# Plot the dataframe with matplotlib
plot_df(filtered_df, plot, all_data, plot_type)


# def mask(df):
#     """Locs the index selected in the listbox.

#     :param df: The dataframe to map
#     :type df: DataFrame
#     :return: Te
#     he dataframe mapped
#     :rtype: DataFrame
#     """
#     lst_level = list(df.index.names)
#     lst_vector = list(df.index.names)
#     mask = pd.DataFrame(
#         data=1,
#         index=pd.MultiIndex.from_product(list(map(self.nametowidget(".").vector.get, lst_vector)), names=lst_level),
#         columns=df.columns,
#     )
#     return df.mul(mask).dropna(how="all")
