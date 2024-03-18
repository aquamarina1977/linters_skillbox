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
#
#
# import shlex
# import subprocess
# from subprocess import Popen
# from flask import Flask
# from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField
# from wtforms.validators import InputRequired, NumberRange
#
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key'
# app.config['WTF_CSRF_ENABLED'] = False
#
#
# class CodeForm(FlaskForm):
#     code = StringField(validators=[InputRequired()])
#     timeout = IntegerField(validators=[NumberRange(1, 30)], default=10)
#
#
# def run_python_code_in_subproccess(code: str, timeout: int) -> tuple[str, str, bool]:
#     safe_code: str = shlex.quote(code)
#     command: str = f'python -c {safe_code}'
#     args: list[str] = shlex.split(command)
#     process: Popen = Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     was_killed_by_timeout: bool = False
#     try:
#         output, errors = process.communicate(timeout=timeout)
#     except subprocess.TimeoutExpired:
#         process.kill()
#         output, errors = process.communicate()
#         was_killed_by_timeout = True
#
#     return output.decode(), errors.decode(), was_killed_by_timeout
#
#
# @app.route('/run_code', methods=['POST'])
# def run_code():
#     code_form: CodeForm = CodeForm()
#     if code_form.validate_on_submit():
#         code: str = code_form.code.data
#         timeout: int = code_form.timeout.data
#         stdout, stderr, killed = run_python_code_in_subproccess(code, timeout)
#         return dict(
#             stdout=stdout,
#             stderr=stderr,
#             timelimit=killed
#         ), 200
#
#     return f'Bad request. Error = {code_form.errors}', 400
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
