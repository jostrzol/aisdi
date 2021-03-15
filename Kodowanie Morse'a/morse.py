
from io import TextIOWrapper
from argparse import ArgumentParser


def morsify_char(char: str):
    tr_table = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
    }
    try:
        return tr_table[char.upper()]
    except KeyError:
        return ""


def morsify_word(word: str):
    return " ".join([morsify_char(char)
                    for char in word if morsify_char(char) != ""])


def morsify_file(f: TextIOWrapper):
    result = ""
    for line in f:
        result += " / ".join([morsify_word(word)
                             for word in line.split()
                             if morsify_word(word) != ""]) + "\n"
    return result


def main():
    parser = ArgumentParser(
        "morse", "morsifies a file and prints it to standard output")
    parser.add_argument("file", type=str, help="file to morsify")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf8") as f:
            print(morsify_file(f))
    except PermissionError:
        print("Permission to file denied")
    except FileNotFoundError:
        print("File not found")
    except OSError:
        print("Error opening the file")


if __name__ == "__main__":
    main()
