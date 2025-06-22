# Aklanon Dictionary Parser

**A Python script that parses an Aklanon dictionary and converts it into several
useful formats**

## About

This parser parses an [Aklanon](https://en.wikipedia.org/wiki/Aklanon_language)
dictionary from the book
[A Study of the Aklanon Dialect (Vol. 2)](https://files.eric.ed.gov/fulltext/ED145704.pdf)
in Excel format and outputs it to [JSON format](output/akl_dictionary.json),
[frequency list](output/akl_freqlist.csv), and
[word list](output/akl_wordlist.txt). Since the book is in PDF format, the
dictionary is manually encoded from the book to the Excel file. The encoded data
is still incomplete as it is very time consuming to manually encode. Thus,
[contribute](#contributing) if you can.

## Output

> <strong style="font-size: large;">4,471 words collected</strong> <small>(as of
> 08/09/2024)</small>

| Resource       | Format | Link                                                     |
| -------------- | ------ | -------------------------------------------------------- |
| Dictionary     | json   | [output/akl_dictionary.json](output/akl_dictionary.json) |
| Frequency list | csv    | [output/akl_freqlist.csv](output/akl_freqlist.csv)       |
| Word list      | txt    | [output/akl_wordlist.txt](output/akl_wordlist.txt)       |

### JSON Dictionary

The JSON dictionary is structured as a list of words and its corresponding list
of attributes. The attributes include part of speech, definition, etymology,
classifications, synonyms, antonyms, example sentences, inflections, and
sources. The entries are sorted alphabetically.

```json
[
  {
    "word": "The word itself",
    "attributes": [
      {
        "pos": "Simplified arts of speech",
        "definition": "The definition",
        "origin": "The etymology",
        "classification": "Any classification",
        "similar": ["List of synonyms"],
        "opposite": ["List of antonyms"],
        "examples": ["List of example sentences that use the word"],
        "inflections": ["List of inflected forms"],
        "sources": ["List of sources"]
      }
    ]
  }
]
```

### Frequency list

The frequency list is structured as a list of words and its corresponding
frequency value sorted from highest to lowest frequency value. Since there's no
available Aklanon frequency list yet, all frequency values are set to 1.

```csv
a,1
ab-ab,1
aba,1
```

### Word list

The word list is simply the list of words sorted alphabetically.
