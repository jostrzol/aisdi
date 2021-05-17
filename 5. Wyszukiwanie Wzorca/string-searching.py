from typing import List


class StringSearching:
    def __init__(self, txt: str, pat: str):
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
        M = len(self._pattern)
        N = len(self._text)

        # A loop to slide pat[] one by one
        for i in range(N - M + 1):
            j = 0

            # For current index i, check
            # for pattern match
            while(j < M):
                if (self._text[i + j] != self._pattern[j]):
                    break
                j += 1

            if (j == M):
                # return the pattern's
                # indexes in text
                return list(range(i, (i + M)))

    def find_kmp(self) -> List[int]:
        """
        Knuth–Morris–Pratt algorithm
        """
        pass

    def find_kr(self) -> List[int]:
        """
        Rabin–Karp algorithm
        """
        pass


string1 = StringSearching("abcABC123qwerty", "qwe")
print(string1.find_n())  # should print out "[9, 10, 11]"
