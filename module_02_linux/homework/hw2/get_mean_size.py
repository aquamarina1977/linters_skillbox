"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    lines = ls_output.split('\n')[1:]
    total_size = 0
    num_files = 0
    for line in lines:
        parts = line.split()
        if len(parts) > 4:
            try:
                size = int(parts[4])
                total_size += size
                num_files += 1
            except ValueError:
                continue
    if num_files > 0:
        mean_size = total_size / num_files
    else:
        mean_size = 0
    return mean_size


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)
