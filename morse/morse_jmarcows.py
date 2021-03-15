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


def file_to_array(file):
    f = open(file, "r")
    array_of_lines = []
    for line in f:
        array_of_lines.append(line)
    f.close()
    return array_of_lines


# quick test
y = letter_to_morse["y"]
print(y)

# can you hear me GitLab?
