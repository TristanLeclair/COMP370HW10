import argparse
import json
import os
from enum import Enum
from typing import Tuple

import pandas as pd


class Headers(Enum):
    title = "title"
    writer = "writer"
    pony = "pony"
    dialog = "dialog"


def parse_args() -> Tuple[argparse.FileType, str]:
    parser = argparse.ArgumentParser(
        description="Build network graph of pony interactions in my little pony dialog"
    )

    parser.add_argument("-i", type=argparse.FileType("r"), help="Pony dialog csv file")

    parser.add_argument(
        "-o",
        type=str,
        help="Output json file containing objects of all the interactions of the ponies",
    )

    args = parser.parse_args()

    return args.i, args.o


def import_data(input):
    df = pd.read_csv(input)

    # remove writer column
    df = df.drop(columns=[Headers.writer.value])

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # lowercase all pony names
    df[Headers.pony.value] = df[Headers.pony.value].str.lower()
    return df


def create_network(df: pd.DataFrame, most_freq_chars: list) -> dict:
    dialog_dict = {}
    banned_words_in_names = ["others", "ponies", "and", "all"]

    def valid_row(episode, next_episode, pony, next_pony):
        """Check if the current row is a valid row to calculate interaction"""
        if episode != next_episode:
            return False
        # exclude non-important characters
        if pony not in most_freq_chars:
            return False
        if next_pony not in most_freq_chars:
            return False
        if pony == next_pony:
            return False
        # if any of the words in the pony name are in the banned list, skip
        # this is to prevent names like "all ponies" or "others" from being counted
        # as a pony
        # if the current speaker or the next speaker is not a pony, skip
        if any([word in banned_words_in_names for word in pony.split(" ")]):
            return False
        # if the listener is not a pony, skip
        if any([word in banned_words_in_names for word in next_pony.split(" ")]):
            return False
        return True

    def calculate_interaction(row):
        """Calculate the interaction between the current speaker and the next speaker and update the dialog_dict"""
        episode, pony, next_episode, next_pony = (
            row["title"],
            row["pony"],
            row["next_episode"],
            row["next_pony"],
        )
        pony = str(pony).lower()
        next_pony = str(next_pony).lower()

        if not valid_row(episode, next_episode, pony, next_pony):
            return

        if pony not in dialog_dict:
            dialog_dict[pony] = {}

        if next_pony not in dialog_dict[pony]:
            dialog_dict[pony][next_pony] = 1
            return

        dialog_dict[pony][next_pony] += 1

        pass

    # group by episode
    # df_grouped = df.groupby(Headers.title.value)

    df["next_episode"] = df[Headers.title.value].shift(-1)
    df["next_pony"] = df[Headers.pony.value].shift(-1)

    df.apply(calculate_interaction, axis=1)

    return dialog_dict


def get_highest_speaking_ponies(df: pd.DataFrame) -> list:
    # get top 101 most frequent characters
    most_freq_chars = (
        df[Headers.pony.value]
        .value_counts()
        .sort_values(ascending=False)
        .head(101)
        .index.tolist()
    )
    return most_freq_chars


def main():
    input_file, output_file = parse_args()

    df = import_data(input_file)

    df = clean_data(df)

    most_freq_chars = get_highest_speaking_ponies(df)

    dialog_dict = create_network(df, most_freq_chars)

    # if output file is specified, check that path exists
    # if not, create it
    if output_file:
        # extract directory path
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    with open(output_file, "w") as f:
        json.dump(dialog_dict, f, indent=4)

    pass


if __name__ == "__main__":
    main()
