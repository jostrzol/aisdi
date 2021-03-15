import argparse
import sys

letter_to_morse_dict = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "line": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    " ": "/"
}


def letter_to_morse(letter):
    try:
        return f"{letter_to_morse_dict[letter.lower()]} "
    except KeyError:
        return ""


def main(arguments):
    parser = argparse.ArgumentParser(prog="morse translator",
                                     description="reads the contents of " +
                                     "a given text file and prints its " +
                                     "content into standard output in " +
                                     "morse code")

    parser.add_argument('files', type=argparse.FileType('r'), nargs='+',
                        help="files to translate into morse code")

    args = parser.parse_args()

    for f in args.files:
        morse = []
        for line in f:
            line = line.rstrip()
            morse_line = ""
            for letter in line:
                morse_line += letter_to_morse(letter)
            morse_line = morse_line[:-1]
            morse.append(morse_line)

        for i in range(len(morse)):
            while " / /" in morse[i]:
                morse[i] = morse[i].replace(" / /", " /")

        for line in morse:
            print(line)


if __name__ == "__main__":
    main(sys.argv)
