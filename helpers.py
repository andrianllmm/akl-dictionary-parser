import re


def is_valid(word):
    """Validates a word based on specified patterns.
    The pattern dictates that the word must only contain of alphabet letters, apostrophes, hyphens, and periods.

    Args:
        word (str): Any word.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.match(r"^[a-zA-Z\'\-\.]+$", word))


def to_sentence(s):
    """Converts a string to sentence case.

    Args:
        s (str): Any string.

    Returns:
        str: The string in sentence case.
    """
    if not s:
        return None

    if len(s) > 1:
        s = s[0].upper() + s[1:]
        if s[-1] not in [".", "?", "!"]:
            s += "."

    return s


def format_pos(pos):
    """Formats a Parts of Speech (POS) tag into simpler forms.

    Args:
        pos (str): The POS tag.

    Returns:
        str/None: The formatted POS tag, if POS is provided, None otherwise.
    """
    if pos:
        formatted_pos = pos.lower()

        pos_formats = {
            "n": "n.",
            "n.mascl": "n.mascl.",
            "n.fem": "n.fem.",
            "n.prop.": "n.prop.",
            "v": "v.",
            "rv1": "v.r.1",
            "rv2": "v.r.2",
            "rv3": "v.r.3",
            "rv4": "v.r.4",
            "rv5": "v.r.5",
            "rv6": "v.r.6",
            "rv7": "v.r.7",
            "rv8": "v.r.8",
            "rv9": "v.r.9",
            "cv": "v.c.",
            "dv": "v.d.",
            "st1": "v.st.1",
            "st2": "v.st.2",
            "st3": "v.st.3",
            "st4": "v.st.4",
            "st5": "v.st.5",
            "stq": "v.st.q",
            "rel": "v.rel.",
            "rel.v": "v.rel.",
            "rec": "v.rec.",
            "rec.v": "v.rec.",
            "tm": "m.t.",
            "am": "m.a.",
            "om": "m.o.",
            "rm": "m.r.",
            "lm": "m.l.",
            "em": "m.e.",
            "pro": "pro.",
            "t/pro": "pro.t.",
            "a/pro": "pro.a.",
            "r/pro": "pro.r.",
            "adj": "adj.",
            "adj.mascl": "adj.mascl.",
            "adj.fem": "adj.fem.",
            "adv": "adv.",
            "conj": "conj.",
            "prep": "prep.",
            "intj": "intj.",
            "n.det": "det.n.",
            "v.det": "det.v.",
            "a.det": "det.adj.",
            "dem": "dem.",
            "t/dem": "dem.t.",
            "a/dem": "dem.a.",
            "r/dem": "dem.r.",
            "dec": "dec.",
            "a/dec": "dec.a.",
            "loc": "loc.",
            "p": "p.",
            "qp": "p.q.",
            "neg": "p.neg.",
            "dp": "p.d.",
            "tp": "tp.",
            "ifx": "ifx.",
            "pfx": "pfx.",
            "sfx": "sfx.",
        }

        return pos_formats[formatted_pos]
    return None


def auto_match_entries(entries):
    """Ensures that all listed similar or opposite words of each dictionary entry has its own entry.

    Args:
        entries (list): A list of dictionary entries.

    Returns:
        list: A list of dictionary entries.
    """
    auto_matched_entries = []

    try:
        for entry in entries:
            print(entry["word"])

            for attribute in entry["attributes"]:
                if attribute.get("similar"):
                    for similar in attribute["similar"]:
                        if similar not in [fe["word"] for fe in entries]:
                            similar_entry = {
                                "word": similar,
                                "attributes": [
                                    {
                                        "definition": "",
                                        "pos": attribute["pos"],
                                        "origin": None,
                                        "classification": None,
                                        "sources": attribute["sources"],
                                        "similar": [
                                            entry["word"],
                                        ],
                                        "opposite": [],
                                        "examples": [],
                                    }
                                ],
                            }
                            auto_matched_entries.append(similar_entry)
                            print("added " + similar_entry["word"])
                        else:
                            similar_entry = list(
                                filter(
                                    lambda entry: entry["word"] == similar,
                                    entries,
                                )
                            )[0]
                            for attribute in similar_entry["attributes"]:
                                if entry["word"] not in attribute["similar"]:
                                    attribute["similar"].append(entry["word"])

                if attribute.get("opposite"):
                    for opposite in attribute["opposite"]:
                        if opposite not in [fe["word"] for fe in entries]:
                            opposite_entry = {
                                "word": opposite,
                                "attributes": [
                                    {
                                        "definition": "",
                                        "pos": attribute["pos"],
                                        "origin": None,
                                        "classification": None,
                                        "sources": attribute["sources"],
                                        "similar": [],
                                        "opposite": [
                                            entry["word"],
                                        ],
                                        "examples": [],
                                    }
                                ],
                            }
                            auto_matched_entries.append(opposite_entry)
                            print("added " + opposite_entry["word"])
                        else:
                            opposite_entry = list(
                                filter(
                                    lambda entry: entry["word"] == opposite,
                                    entries,
                                )
                            )[0]
                            for attribute in opposite_entry["attributes"]:
                                if entry["word"] not in attribute["opposite"]:
                                    attribute["opposite"].append(entry["word"])

    except KeyboardInterrupt:
        pass

    return auto_matched_entries


VALID_ORIGINS = [
    "sp",
    "eng",
    "tag",
    "ch",
    "hil",
    "jp",
    "lib",
    "bkd",
    "ibj",
    "oak",
    "nab",
    "kin",
]

VALID_CLASSIFICATIONS = [
    "fe",
    "ae",
    "idm",
    "expr",
    "slg",
    "sup",
    "stf",
    "cor",
    "gen",
    "vul",
]