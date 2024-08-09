import concurrent.futures
import json
import numpy as np
import os
import pandas as pd
import sys

from helpers import *


script_dir = os.path.dirname(os.path.realpath(__file__))


def parse(
    file_path=os.path.join(script_dir, "data/akl_dictionary.xlsx"),
    sheet_name="root_words",
    auto_match=False,
):
    """Parses every dictionary entry from an Excel file to a list.

    Args:
        file_path (str, optional): The path to the Excel file. Defaults to '<script_dir>/data/akl_dictionary.xlsx'.
        sheet_name (str, optional): The name of the Excel sheet. Defaults to 'root_words'.
        auto_match (bool, optional): Performs auto matching if True, does not if False. Defaults to False

    Returns:
        list: A list of dictionaries, each representing a dictionary entry containing:
            - 'word': The word
            - 'pos': Parts of Speech
            - 'definitions': List of definitions
            - 'origin': Origin or etymology
            - 'classification': Some classification
            - 'similar': List of similar words
            - 'opposite': List of opposite
            - 'examples': List of examples
            - 'inflections': List of inflections
            - 'sources': List of sources
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.set_index("word", inplace=True)
    df.replace(np.nan, None, inplace=True)
    entries = [
        {"word": word, "attributes": attributes.to_dict(orient="records")}
        for word, attributes in df.groupby(level=0)
    ]

    dictionary = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(parse_entry, entries)

        for result in results:
            new_entry = result
            dictionary.append(new_entry)

    if auto_match:
        return auto_match_entries(dictionary)

    return dictionary


def parse_entry(entry):
    """Parses a dictionary entry.

    Args:
        entry (dict): The dictionary entry.

    Returns:
        dict: A dictionary containing the word and its attributes.
    """
    word = entry["word"].strip()

    if not is_valid(word):
        None

    print(word)

    attributes = []
    for attribute in entry["attributes"]:

        if definition := attribute.get("definition"):
            definition = (
                to_sentence(definition)
                .replace("(sn:", "(scientific name:")
                .replace("(ctr:", "(contraction of:")
            )
        else:
            definition = None

        if pos := attribute.get("pos"):
            pos = format_pos(pos.strip())

            if pos == "n." and word[0].isupper():
                pos += "prop."
        else:
            pos = None

        if origin := attribute.get("origin"):
            if origin.strip() not in VALID_ORIGINS:
                print("Invalid origin")
                break
            origin = origin.strip()
        else:
            origin = None

        if classification := attribute.get("classification"):
            if classification.strip() not in VALID_CLASSIFICATIONS:
                print("Invalid classification")
                break
            classification = classification.strip()
        else:
            classification = None

        if attribute.get("similar"):
            similar = [word.strip() for word in attribute["similar"].split(",")]
        else:
            similar = []

        if attribute.get("opposite"):
            opposite = [word.strip() for word in attribute["opposite"].split(",")]
        else:
            opposite = []

        if attribute.get("examples"):
            examples = [
                {"original": example.strip(), "translations": {}}
                for example in attribute["examples"].split("//")
            ]

            if examples_translation := attribute.get("examples_translation"):
                for i, translation in enumerate(examples_translation.split("//")):
                    examples[i]["translations"]["eng"] = translation
        else:
            examples = []

        if source := attribute.get("source"):
            source = source.strip()
        else:
            source = None

        attributes.append(
            {
                "pos": pos,
                "definition": definition,
                "origin": origin,
                "classification": classification,
                "similar": similar,
                "opposite": opposite,
                "examples": examples,
                "inflections": [],
                "sources": [source],
            }
        )

    new_entry = {"word": word, "attributes": attributes}

    return new_entry


def export(
    dictionary,
    out_path=os.path.join(script_dir, "output/akl_dictionary.json"),
    overwrite=False,
):
    """Exports a list of dictionaries representing a dictionary entry to a JSON file.

    Args:
        dictionary (list): A list of dictionaries, each representing a dictionary entry.
        out_path (str, optional): The path to the output JSON file. Defaults to '<script_dir>/output/akl_dictionary.json'
        overwrite (bool, optional): Overwrites existing output file if True, otherwise if False. Defaults to False.

    Returns:
        bool: True if successful, False otherwise.
    """
    print("Exporting...")

    if not overwrite and os.path.isfile(out_path):
        permit = None
        while permit not in ["y", "n"]:
            permit = input(f"{out_path} already exists.\n Overwrite? (Y/n) ").lower()
            if permit == "n":
                sys.exit("Terminated")

    with open(out_path, "w") as out_file:
        json.dump(dictionary, out_file, indent=4, ensure_ascii=False)

    print("Exported successfully.")

    return True


if __name__ == "__main__":
    export(parse())
