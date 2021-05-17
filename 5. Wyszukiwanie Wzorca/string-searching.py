from typing import List


class StringSearching:
    def __init__(self, txt: str, pat: str) -> None:
        """
        Parameters:
            txt: text to be searched
            pat: substring to be found

        Returns:
            List of positions in ascending order of
            the beginnings of "pat" in "txt".
        """
        self._text = txt
        self._pattern = pat

    def find_n(self) -> List[int]:
        """
        Naive Search
        """
        match_indices = []

        M = len(self._pattern)
        N = len(self._text)

        # a loop to slide pat[] one by one
        for i in range(N - M + 1):
            j = 0

            # for current index i, check
            # for pattern match
            while(j < M):
                if (self._text[i + j] != self._pattern[j]):
                    break
                j += 1

            if (j == M):
                # return the pattern's
                # indexes in text
                match_indices.append(i)

        return match_indices

    def find_kmp(self) -> List[int]:
        """
        Knuth–Morris–Pratt algorithm
        """
        match_indices = []
        pattern_lps = self.compute_lps()

        pattern_i = 0
        for i, ch in enumerate(self._text):

            # if a mismatch was found, roll back the pattern
            # index using the information in LPS
            while pattern_i and self._pattern[pattern_i] != ch:
                pattern_i = pattern_lps[pattern_i - 1]

            # if match
            if self._pattern[pattern_i] == ch:
                # if the end of a pattern is reached, record a result
                # and use infromation in LSP array to shift the index
                if pattern_i == len(self._pattern) - 1:
                    match_indices.append(i - pattern_i)
                    pattern_i = pattern_lps[pattern_i]

                else:
                    # move the pattern index forward
                    pattern_i += 1

        return match_indices

    def find_kr(self) -> List[int]:
        """
        Karp-Rabin algorithm
        """
        pass

    def compute_lps(self) -> List[int]:
        # Longest Proper Prefix that is suffix array (LPS)
        lps = [0] * len(self._pattern)

        prefix = 0
        for i in range(1, len(self._pattern)):

            # roll the prefix pointer back until match
            # or beginning of pattern is reached
            while prefix and self._pattern[i] != self._pattern[prefix]:
                prefix = lps[prefix - 1]

            # if match, record the LSP for the
            # current 'i' and move prefix pointer
            if self._pattern[prefix] == self._pattern[i]:
                prefix += 1
                lps[i] = prefix

        return lps


string1 = StringSearching("abcABC123qweqtyqweqweq", "qweq")

# all should print out "[9, 15, 18]"
print(string1.find_n())
print(string1.find_kmp())
