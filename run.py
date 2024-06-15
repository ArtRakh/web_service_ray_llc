from flask import Flask, request, flash, abort, redirect, url_for, render_template, send_file
import pandas as pd
import joblib
import pyarrow
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
from pathlib import Path
clf = joblib.load('catboost_model_final.pickle.dat')

app = Flask(__name__)

@app.route('/badrequest400')
def bad_request():
    return abort(400)

app.config.update(dict(
    SECRET_KEY="c4ca4238a0b923820dcc509a6f75849b",
    WTF_CSRF_SECRET_KEY="356a192b7913b04c54574d18c28d46e6395428ab"
))

class MyForm(FlaskForm):
    type = StringField('File type', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():

        f = form.file.data
        if str(form.type.data)=='csv':
            df = pd.read_csv(f, index_col=0)
            X = df.drop(columns=['target'])
            predict_proba = clf.predict_proba(X)[:, 1]
            result = pd.DataFrame(predict_proba, columns=['proba'])
            filename = 'predictions.'+str(form.type.data)
            result.to_csv(filename, index=False)
            return send_file(
                filename,
                mimetype='text/csv',
                as_attachment=True
            )
        else:
            return redirect(url_for('bad_request'))

    return render_template('submit.html', form=form)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''