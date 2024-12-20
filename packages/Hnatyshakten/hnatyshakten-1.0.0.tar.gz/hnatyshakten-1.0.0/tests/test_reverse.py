import unittest
from reverse.reverse import reverse_words_with_special_chars


class TestReverseWordsWithSpecialChars(unittest.TestCase):
    def test_regular_text(self):
        self.assertEqual(reverse_words_with_special_chars("Hello world!"), "olleH dlrow!")

    def test_text_with_special_characters(self):
        self.assertEqual(reverse_words_with_special_chars("a,b$c"), "c,b$a")
        self.assertEqual(reverse_words_with_special_chars("abc,d!"), "cba,d!")

    def test_text_with_spaces(self):
        self.assertEqual(reverse_words_with_special_chars("  Hello   world  "), "  olleH   dlrow  ")

    def test_empty_string(self):
        self.assertEqual(reverse_words_with_special_chars(""), "")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            reverse_words_with_special_chars(12345)


if __name__ == "__main__":
    unittest.main()
