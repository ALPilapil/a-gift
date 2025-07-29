import streamlit as st
import pandas as pd
import numpy as np
import os, random
from main import main, combined, search

# everything is top down
st.title("For my favorite girl")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# keep track of variables we'll need here and what operation
# target_word - frequency over time, a graph

#---------------------- WORD ANALYSIS ----------------------#
st.write("# Word Analysis")

st.button("Reset", type="primary")
def pair():
    if st.button("See seperate"):
        df_list = main(uploaded_file)
        
        # iterate through in pairs
        for i in range(0, len(df_list), 2):
            angela_df = df_list[i]
            aaron_df  = df_list[i+1]

            # ensure 'date' is datetime and set as index
            for df in (angela_df, aaron_df):
                df["date"] = pd.to_datetime(df["date"])
                df.set_index("date", inplace=True)

            # build two columns
            col1, col2 = st.columns(2)

            col1.subheader("Angela")
            col1.line_chart(angela_df)

            col2.subheader("Aaron")
            col2.line_chart(aaron_df)

def together():
    if st.button("See combined"):
        combined_list = combined(uploaded_file)

        for df in combined_list:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)

            st.line_chart(df)

def find():
    x = st.text_input("Search for a specific word: ")
    if x:
        df = search(uploaded_file, x)

        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        st.line_chart(df)


pair()
together()
find()