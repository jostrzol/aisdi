import importlib
string_searching = importlib.import_module("string-searching")


# - - - - Naive Search - - - - - - - - - - - - - - - - - - - - - - - - - - - #

def test_find_n_normal_case():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "qweq"
    assert(string_searching.find_n(text_1, string_1) == [9, 15, 18])


def test_find_n_empty_text():
    text_1 = ""
    string_1 = "qweq"
    assert(string_searching.find_n(text_1, string_1) == [])


def test_find_n_empty_string():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = ""
    assert(string_searching.find_n(text_1, string_1) == [])


def test_find_n_both_empty():
    text_1 = ""
    string_1 = ""
    assert(string_searching.find_n(text_1, string_1) == [])


def test_find_n_string_equal_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "abcABC123qweqtyqweqweq"
    assert(string_searching.find_n(text_1, string_1) == [0])


def test_find_n_string_longer_than_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "abcABC123qweqtyqweqweq1"
    assert(string_searching.find_n(text_1, string_1) == [])


def test_find_n_string_not_in_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "bella"
    assert(string_searching.find_n(text_1, string_1) == [])


# - - - - Knuth–Morris–Pratt algorithm - - - - - - - - - - - - - - - - - - - #

def test_find_kmp_normal_case():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "qweq"
    assert(string_searching.find_kmp(text_1, string_1) == [9, 15, 18])


def test_find_kmp_empty_text():
    text_1 = ""
    string_1 = "qweq"
    assert(string_searching.find_kmp(text_1, string_1) == [])


def test_find_kmp_empty_string():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = ""
    assert(string_searching.find_kmp(text_1, string_1) == [])


def test_find_kmp_both_empty():
    text_1 = ""
    string_1 = ""
    assert(string_searching.find_kmp(text_1, string_1) == [])


def test_find_kmp_string_equal_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "abcABC123qweqtyqweqweq"
    assert(string_searching.find_kmp(text_1, string_1) == [0])


def test_find_kmp_string_longer_than_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "abcABC123qweqtyqweqweq1"
    assert(string_searching.find_kmp(text_1, string_1) == [])


def test_find_kmp_string_not_in_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "bella"
    assert(string_searching.find_kmp(text_1, string_1) == [])


# - - - - Karp-Rabin algorithm - - - - - - - - - - - - - - - - - - - - - - - #

def test_find_kr_normal_case():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "qweq"
    assert(string_searching.find_kr(text_1, string_1) == [9, 15, 18])


def test_find_kr_empty_text():
    text_1 = ""
    string_1 = "qweq"
    assert(string_searching.find_kr(text_1, string_1) == [])


def test_find_kr_empty_string():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = ""
    assert(string_searching.find_kr(text_1, string_1) == [])


def test_find_kr_both_empty():
    text_1 = ""
    string_1 = ""
    assert(string_searching.find_kr(text_1, string_1) == [])


def test_find_kr_string_equal_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "abcABC123qweqtyqweqweq"
    assert(string_searching.find_kr(text_1, string_1) == [0])


def test_find_kr_string_longer_than_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "abcABC123qweqtyqweqweq1"
    assert(string_searching.find_kr(text_1, string_1) == [])


def test_find_kr_string_not_in_text():
    text_1 = "abcABC123qweqtyqweqweq"
    string_1 = "bella"
    assert(string_searching.find_kr(text_1, string_1) == [])
