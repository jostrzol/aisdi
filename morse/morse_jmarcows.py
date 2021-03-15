import argparse
import sys

letter_to_morse = {
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
    "l": ".-..",
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
    "z": "--.."
}


def main(arguments):
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

    args = parser.parse_args(arguments[1:])
    morse = []

    for f in args.file:
        for line in f:
            l = line.rstrip()
            morse_line = ""
            for letter in l:
                if letter == " ":
                    morse_line += " /"
                elif letter.lower() in letter_to_morse.keys():
                    morse_line += f" {letter_to_morse[letter.lower()]}"
            morse.append(morse_line)
    
    for i in range(len(morse)):
        while " / /" in morse[i]:
            morse[i] = morse[i].replace(" / /", " /")
    
    for line in morse:
        print(line)


if __name__ == "__main__":
    main(sys.argv)
