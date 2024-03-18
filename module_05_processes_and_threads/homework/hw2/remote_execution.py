"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

import subprocess
import shlex
from typing import Tuple

def run_python_code_in_subprocess(code: str, timeout: int = 1) -> Tuple[str, str, bool]:
    command = f'python3 -c "{code}"'
    command = shlex.split(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    was_killed_by_timeout = False
    try:
        outs, errs = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as err:
        process.kill()
        outs, errs = process.communicate()
        was_killed_by_timeout = True
    return outs.decode(), errs.decode(), was_killed_by_timeout


if __name__ == '__main__':
    output, _, _ = run_python_code_in_subprocess("print('Hello')", 5)
    print(output)