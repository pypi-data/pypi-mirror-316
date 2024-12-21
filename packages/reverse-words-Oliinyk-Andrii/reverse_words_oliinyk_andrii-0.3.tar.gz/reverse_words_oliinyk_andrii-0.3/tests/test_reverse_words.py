import unittest
from reverse_words_package.src.reverse_words_andrii_oliinyk.reverse_words import reverse_words_with_non_letters_preserved

class TestReverseWords(unittest.TestCase):
    def test_reverse_simple(self):
        self.assertEqual(reverse_words_with_non_letters_preserved("abcd efgh"), "dcba hgfe")

    def test_reverse_with_special_characters(self):
        self.assertEqual(reverse_words_with_non_letters_preserved("a1bcd efg!h"), "d1cba hgf!e")

    def test_empty_string(self):
        self.assertEqual(reverse_words_with_non_letters_preserved(""), "")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            reverse_words_with_non_letters_preserved(12345)

    def test_no_letters(self):
        with self.assertRaises(ValueError):
            reverse_words_with_non_letters_preserved("12345")

    def test_letters_and_numbers(self):
        self.assertEqual(reverse_words_with_non_letters_preserved("h3llo w0r1d"), "o3llh d0r1w")

if __name__ == "__main__":
    unittest.main()
