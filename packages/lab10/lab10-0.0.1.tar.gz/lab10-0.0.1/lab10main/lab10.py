def reverse_words(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Вхідний аргумент повинен бути рядком.")

    def reverse_word(word):
        letters = [letter for letter in word if letter.isalpha()]
        reversed_word = []

        for letter in word:
            if letter.isalpha():
                reversed_word.append(letters.pop())
            else:
                reversed_word.append(letter)
        return ''.join(reversed_word)

    words = text.split()
    return ' '.join(reverse_word(word) for word in words)


if __name__ == "__main__":
    print("Введіть символьний рядок: ")
    text = input()
    print(reverse_words(text))