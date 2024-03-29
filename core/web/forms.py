from flask_wtf import Form, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import FloatField, IntegerField, TextField, StringField, TextAreaField , SelectMultipleField
from wtforms.validators import Required, Optional, NumberRange, Length
from core.database.models import Question, Essay
from flask.ext.login import current_user
import csv

class QuestionForm(Form):
    name = StringField('Name', [Required()], description="The name you want to give this question.", )
   # prompt = TextAreaField('Prompt', [Optional()], description="The prompt for this question (optional).")

    def save(self):
        from app import db
        q = Question(user=current_user)
        self.populate_obj(q)
        db.session.add(q)
        db.session.commit()

class EssayForm(Form):
    text = TextAreaField('Text', [Required()], description="The text of the essay.")
    text=TextAreaField(validators=[Length(150,message="Essay must be of atleast 150 characters")])
    actual_score = FloatField('Score (optional)', [Optional()], description="The score the essay got, out of 5")
    actual_score=FloatField(validators=[NumberRange(min=1,max=5,message="Please enter a score between 1 to 5")])


   # info = TextAreaField("Additional Info (optional)", [Optional()], description="Any additional info you want to store with this essay.")

    def save(self, question):
        from app import db
        e = Essay(question=question)
        self.populate_obj(e)
        db.session.add(e)
        db.session.commit()


class EssayDialect(csv.Dialect):
    quoting = csv.QUOTE_MINIMAL
    delimiter = ","
    quotechar = "\""
    lineterminator = "\n"

class EssayUploadForm(Form):
    upload = FileField('File', [FileRequired(), FileAllowed(['csv'], 'CSV files only!')], description="The csv file with essays you want to upload.")

    def save(self, question, csvfile):
        from app import db
        csvfile.seek(0)
        reader = csv.reader(csvfile, EssayDialect)
        for i, row in enumerate(reader):
            if i == 0:
                continue

            score = row[-1]
            print score
            text = ",".join(row[:-1])

            if len(score) == 0:
                score = None
            else:
                score = float(score)
            e = Essay(question=question, text=text, actual_score=score)
            db.session.add(e)
        db.session.commit()