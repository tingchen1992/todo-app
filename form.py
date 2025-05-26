from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField(
        "任務名稱", validators=[DataRequired(message="任務名稱必填！"), Length(max=100)]
    )
    submit = SubmitField("新增")
