"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
from typing import List


def my_t9(input_numbers: str) -> List[str]:
    t9_mapping = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }

    def generate_words(current_word, remaining_numbers):
        if not remaining_numbers:
            return [current_word]

        results = []
        for char in t9_mapping[remaining_numbers[0]]:
            results.extend(generate_words(current_word + char, remaining_numbers[1:]))

        return results

    return generate_words('', input_numbers)


if __name__ == '__main__':
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    with open('/usr/share/dict/words', 'r') as file:
        for line in file:
            word = line.strip()
            if word in words:
                print(word, end=' ')

