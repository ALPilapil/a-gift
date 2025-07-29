import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def clean_conversation(df, column="Text"):
    """
    lets remove eveything not alphanumeric
    """
    df[column] = (
        df[column]
        .astype(str)
        .str.replace(r"[^A-Za-z0-9\s]", "", regex=True)
    )
    return df

def word_freq_by_day_and_type(df, target_words,
                              date_col="Message Date",
                              type_col="Type",
                              text_col="Text"):
    # 1) parse dates and normalize text
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df["date"] = df[date_col].dt.date
    df[text_col] = df[text_col].fillna("").str.lower()
    
    freq_dfs = {}
    for chat_type in df[type_col].unique():
        sub = df[df[type_col] == chat_type].copy()
        # 2) count each word in each row
        for word in target_words:
            pattern = rf"\b{re.escape(word.lower())}\b"
            sub[word] = sub[text_col].str.count(pattern)
        # 3) aggregate by date
        freq = (
            sub
            .groupby("date")[target_words]
            .sum()
            .reset_index()
        )
        freq_dfs[chat_type] = freq
    
    return freq_dfs

def main(uploaded_file):
    """
    just use this part to load in data and do some basic analysis on certain things
    library wordcloud is just presentation stuff

    note that streamlit comes with plots that work automatically on dfs

    WORD ANALYSIS
    1. top pet names
    - baby, babe
    2. inside jokes
    - chopped, rizz, ts, holy, chinese, fat, fatty, aye(ee...), vietnamese, freak
    3. characters
    - colin, sky, justin, manik, andrew, nguyen

    IMAGES
    1. random image generator

    MILESTONES
    1. first to...
    - i love you
    """
    # CLEAN DATA
    conversation = pd.read_csv(uploaded_file)
    # incoming = angela, outgoing = aaron
    trimed_converasation = conversation.loc[:, ["Message Date", "Type", "Text"]]
    # clean the data
    cleaned_conversation = clean_conversation(trimed_converasation)

    #--------------------- WORD ANALYSIS ---------------------#
    # diff types of targets
    pet_targets = ["baby", "babe", "my baby"]
    joke_targets = ["chopped", "rizz", "ts", "holy", "chinese", "fat", "fatty", "aye", "vietnamese", "freak"]
    character_targets = ["colin", "sky", "justin", "manik", "andrew", "nguyen"]

    # get tables for each of them
    pet_freq_tables = word_freq_by_day_and_type(cleaned_conversation, pet_targets)
    joke_freq_tables = word_freq_by_day_and_type(cleaned_conversation, joke_targets)
    character_freq_tables = word_freq_by_day_and_type(cleaned_conversation, character_targets)
 
    # then seperate into aaron and angela
    angela_pet = pet_freq_tables["Incoming"]
    aaron_pet = pet_freq_tables["Outgoing"]

    angela_joke = joke_freq_tables["Incoming"]
    aaron_joke = joke_freq_tables["Outgoing"]

    angela_char = character_freq_tables["Incoming"]
    aaron_char = character_freq_tables["Outgoing"]

    return [angela_pet, aaron_pet, angela_joke, aaron_joke, angela_char, aaron_char]

def combined(uploaded_file):

    df_list = main(uploaded_file)

    angela_pet = df_list[0]
    aaron_pet = df_list[1]
    angela_joke = df_list[2]
    aaron_joke = df_list[3]
    angela_char = df_list[4]
    aaron_char = df_list[5]

    combined_pet = (
    pd.concat([angela_pet, aaron_pet], axis=0)   # stack rows
      .groupby("date")                           # group by day
      .sum()                                     # sum each word‑count column
      .reset_index()
    )

    combined_joke = (
        pd.concat([angela_joke, aaron_joke], axis=0)
        .groupby("date")
        .sum()
        .reset_index()
    )

    combined_char = (
        pd.concat([angela_char, aaron_char], axis=0)
        .groupby("date")
        .sum()
        .reset_index()
    )

    return [combined_pet, combined_joke, combined_char]

def search(uploaded_file, targets):

    if isinstance(targets, str):
        targets = [targets]

    # CLEAN DATA
    conversation = pd.read_csv(uploaded_file)
    # incoming = angela, outgoing = aaron
    trimed_converasation = conversation.loc[:, ["Message Date", "Type", "Text"]]
    # clean the data
    cleaned_conversation = clean_conversation(trimed_converasation)

    tgt_freq_tables = word_freq_by_day_and_type(cleaned_conversation, targets)

    angela_target = tgt_freq_tables["Incoming"]
    aaron_target = tgt_freq_tables["Outgoing"]

    combined = (
    pd.concat([angela_target, aaron_target], axis=0)   # stack rows
      .groupby("date")                           # group by day
      .sum()                                     # sum each word‑count column
      .reset_index()
    )

    return combined
