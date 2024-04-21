"""
Задание: Напишите программу, которая выводит n первых элементов
последовательности 122333444455555…
(число повторяется столько раз, чему оно равно).
"""


def first_elements(n: int) -> list[int]:
    result = []
    counter = 1
    while len(result) <= n:
        result += [counter] * counter
        counter += 1

    return result[:n]


def test():
    assert first_elements(5) == [1, 2, 2, 3, 3]
    assert first_elements(0) == []
    assert first_elements(10) == [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    assert first_elements(16) == [
        1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6
    ]
    assert first_elements(-5) == []


if __name__ == '__main__':
    test()
