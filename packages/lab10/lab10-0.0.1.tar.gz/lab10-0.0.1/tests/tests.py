import unittest
from lab10main.lab10 import reverse_words
class TestReverseWords(unittest.TestCase):
    def test_reverse_simple(self):
        self.assertEqual(reverse_words("abcd"), "dcba")

    def test_reverse_with_symbols(self):
        self.assertEqual(reverse_words("a1bcd efg!h"), "d1cba hgf!e")
        self.assertEqual(reverse_words("abc-def"), "fed-cba")

    def test_empty_string(self):
        self.assertEqual(reverse_words(""), "")

    def test_no_alpha(self):
        self.assertEqual(reverse_words("1234!@#$"), "1234!@#$")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            reverse_words(123)

if __name__ == "__main__":
    unittest.main()