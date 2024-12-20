import re


def reverse_words_with_special_chars(text: str) -> str:

    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    def reverse_word(word):
        letters = [ch for ch in word if ch.isalpha()]
        reversed_word = list(word)
        letter_index = len(letters) - 1

        for i, ch in enumerate(word):
            if ch.isalpha():
                reversed_word[i] = letters[letter_index]
                letter_index -= 1
        return ''.join(reversed_word)

    words = re.split(r'(\s+)', text)
    return ''.join(reverse_word(word) for word in words)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    user_input = input("Enter text: ")
    try:
        result = reverse_words_with_special_chars(user_input)
        print("Reversed text:", result)
    except ValueError as e:
        print("Error:", e)