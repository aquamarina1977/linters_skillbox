"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
import subprocess
import shlex

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[validators.InputRequired()])
    timeout = IntegerField(validators=[validators.NumberRange(min=1, max=30)], default=10)

def run_python_code_in_subproccess(code: str, timeout: int):
    safe_code = shlex.quote(code)
    command = f'python -c {safe_code}'
    args = shlex.split(command)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    was_killed_by_timeout = False
    try:
        output, error = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        output, error = process.communicate()
        was_killed_by_timeout = True

@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        stdout, stderr, killed = run_python_code_in_subprocess(code, timeout)
        return dict(
            stdout=stdout,
            stderr=stderr,
            timeout=killed
        ), 200


if __name__ == '__main__':
    app.run(debug=True)
