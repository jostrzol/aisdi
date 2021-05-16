from typing import List


class StringSearching:
    def __init__(self, txt: str, pat: str):
        """
        Parameters:
            txt: text to be searched
            pat: substring to be found

        Returns:
            List of positions in ascending order of
            the beginnings of "substring" in "text".
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
                # return index at which
                # the pattern starts
                return i

    def find_kmp(self):
        """
        Knuth–Morris–Pratt algorithm
        """
        pass

    def find_kr(self):
        """
        Rabin–Karp algorithm
        """
        pass
