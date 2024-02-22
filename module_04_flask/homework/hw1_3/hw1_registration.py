"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Email, Length, Optional

from hw2_validators import number_length, NumberLength

app = Flask(__name__)

#TODO
#В строке phone = IntegerField(validators=[DataRequired()]) был добавлен валидатор Length(),
#по этой прчине падал тест test_invalid_phone
#Тест, проверяющий валидность комментария падал, так как я упустила из виду, что в качестве
#валидатора выбран Optional(). По этой причине я просто убрала тест на валидность комментария.

class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    phone = IntegerField(validators=[DataRequired(), NumberLength(10, 10)])
    name = StringField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    index = IntegerField(validators=[DataRequired()])
    comment = StringField(validators=[Optional()])


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
