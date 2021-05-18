from typing import List


# - - - - Naive Search - - - - - - - - - - - - - - - - - - - - - - - - - - - #

def find_n(text: str, string: str) -> List[int]:
    """
    Naive Search

    Parameters:
        text: text to be searched
        string: substring to be found

    Returns:
        List of positions in ascending order of
        the beginnings of "string" in "text".
    """
    match_indices = []
    if(len(string) > 0):
        M = len(string)
        N = len(text)

        # a loop to slide pat[] one by one
        for i in range(N - M + 1):
            j = 0

            # for current index i, check
            # for pattern match
            while(j < M):
                if (text[i + j] != string[j]):
                    break
                j += 1

            if (j == M):
                # return the pattern's
                # indexes in text
                match_indices.append(i)

    return match_indices


# - - - - Knuth–Morris–Pratt algorithm - - - - - - - - - - - - - - - - - - - #

def find_kmp(text: str, string: str) -> List[int]:
    """
    Knuth–Morris–Pratt algorithm

    Parameters:
        text: text to be searched
        string: substring to be found

    Returns:
        List of positions in ascending order of
        the beginnings of "string" in "text".
    """
    match_indices = []
    if(len(string) > 0):
        pattern_lps = compute_lps(string)

        pattern_i = 0
        for i, ch in enumerate(text):

            # if a mismatch was found, roll back the pattern
            # index using the information in LPS
            while pattern_i and string[pattern_i] != ch:
                pattern_i = pattern_lps[pattern_i - 1]

            # if match
            if string[pattern_i] == ch:
                # if the end of a pattern is reached, record a result
                # and use infromation in LSP array to shift the index
                if pattern_i == len(string) - 1:
                    match_indices.append(i - pattern_i)
                    pattern_i = pattern_lps[pattern_i]

                else:
                    # move the pattern index forward
                    pattern_i += 1

    return match_indices


def compute_lps(string: str) -> List[int]:
    """
    Longest Proper Prefix that is suffix array (LPS)
    """
    # Example:
    #   Pattern:    "ACABACACD"
    #   LPS:        [001012320]
    lps = [0] * len(string)

    prefix = 0
    for i in range(1, len(string)):

        # roll the prefix pointer back until match
        # or beginning of pattern is reached
        while prefix and string[i] != string[prefix]:
            prefix = lps[prefix - 1]

        # if match, record the LSP for the
        # current 'i' and move prefix pointer
        if string[prefix] == string[i]:
            prefix += 1
            lps[i] = prefix

    return lps


# - - - - Karp-Rabin algorithm - - - - - - - - - - - - - - - - - - - - - - - #

def find_kr(text: str, string: str) -> List[int]:
    """
    Karp-Rabin algorithm

    Parameters:
        text: text to be searched
        string: substring to be found

    Returns:
        List of positions in ascending order of
        the beginnings of "string" in "text".
    """
    match_indices = []
    if(len(string) > 0):
        s_hash = hash_kr(string)

        prevstr = ""
        prevhash = None
        for i in range(len(text) - len(string)+1):
            text_slice = text[i:i+len(string)]
            t_hash = hash_kr(text_slice, prevstr, prevhash)
            if t_hash == s_hash and text_slice == string:
                match_indices.append(i)

            prevstr = text_slice
            prevhash = t_hash

    return match_indices


def hash_kr(string: str, prevstr: str = "", prevhash: int = None,
            base=ord('ż') + 1, wordlength: int = 64):
    """
    Hashes the given string in constant time based on the previous hash
    If no previous hash given, hash string

    Parameters:
        string:         string to hash
        prevstr:        prevous value of this hash
        base:           alphabet length
        wordlength:     used to calculate modulo

    Returns:
        hash
    """
    mod = round(((1 << wordlength) - 1)/base)

    # if no prev perform hash of the whole string
    if prevhash is None:
        hash = 0
        for i, ch in enumerate(string[::-1]):
            hash += ord(ch) * base**i % mod
        return hash

    # "remove" the first character
    prevhash -= ord(prevstr[0]) * base**(len(prevstr)-1) % mod
    # "shift" the string
    prevhash *= base % mod
    # "add" the new character
    prevhash += ord(string[-1]) % mod
    return prevhash
