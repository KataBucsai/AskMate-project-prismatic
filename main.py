from flask import Flask, render_template, request, redirect
import csv
import data_manager
import os
from importlib.machinery import SourceFileLoader
from werkzeug.utils import secure_filename

current_file_path = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/uploads/img/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def list_questions():
    file_name = current_file_path + "/data/question.csv"
    question_list = data_manager.get_table_from_file(file_name, (4, 5, 6))
    question_list = data_manager.table_sort(question_list, 1, True)
    return render_template('list_questions.html', question_list=question_list)


@app.route('/create_new_question', methods=['POST'])
def create_new_question():
    file_name = current_file_path + "/data/question.csv"
    question_list = data_manager.get_table_from_file(file_name, (4, 5, 6))
    question_list_csv_format = data_manager.get_timeform_to_stamp(question_list)
    question_list_csv_format = data_manager.add_item_to_table(question_list_csv_format, request.form)
    data_manager.write_table_to_file(file_name, question_list_csv_format, (4, 5, 6))
    return redirect('/')


@app.route('/question/new')
def new_question():
    return render_template('new_question.html')


@app.route('/question/<id>')
def display_question(id):
    # view counter += 1
    question_file_name = current_file_path + "/data/question.csv"
    question_list = data_manager.get_table_from_file(question_file_name, (4, 5, 6))
    for row in question_list:
        if row[0] == id:
            title = row[4]
            message = row[5]
            row[2] = str(int(row[2])+1)
            question_list = data_manager.get_timeform_to_stamp(question_list)
            data_manager.write_table_to_file(question_file_name, question_list, (4, 5, 6))
            break
    answer_file_name = current_file_path + "/data/answer.csv"
    answer_list = data_manager.get_table_from_file(answer_file_name, (4, 5))
    list_answers = []
    for row in answer_list:
        if row[3] == id:
            list_answers.append(row)
    return render_template('display_question.html', id=id, title=title, message=message, list_answers=list_answers)


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return render_template('new_answer.html', question_id=question_id)


@app.route('/create_new_answer', methods=['POST'])
def add_new_answer():
    file_name = current_file_path + "/data/answer.csv"
    answer_list = data_manager.get_table_from_file(file_name, (4, 5))
    answer_list_csv_format = data_manager.get_timeform_to_stamp(answer_list)
    answer_list_csv_format = data_manager.add_item_to_answer_table(answer_list_csv_format, request.form)
    data_manager.write_table_to_file(file_name, answer_list_csv_format, (4, 5))
    return redirect('/question/' + request.form["question_id"])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_image/<id>', methods=['GET', 'POST'])
def add_image(id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # filename-to-table
            question_file_name = current_file_path + "/data/question.csv"
            question_list = data_manager.get_table_from_file(question_file_name, (4, 5, 6))
            for row in question_list:
                if row[0] == id:
                    row[6] = '/images/' + filename
                    break
            # update csv
            question_list_csv_format = data_manager.get_timeform_to_stamp(question_list)
            # question_list_csv_format = data_manager.add_item_to_table(question_list_csv_format, request.form)
            data_manager.write_table_to_file(question_file_name, question_list_csv_format, (4, 5, 6))
            return redirect('/')
    return render_template('file_upload.html')


@app.route('/vote_question_up')
def vote_question_up():
    print(request.args.get('id'))
    file_name = current_file_path + "/data/question.csv"
    question_list = data_manager.get_table_from_file(file_name, (4, 5, 6))
    for row in question_list:
        if row[0] == request.args.get('id'):
            row[3] = str(int(row[3]) + 1)
            break
    question_list_csv_format = data_manager.get_timeform_to_stamp(question_list)
    data_manager.write_table_to_file(file_name, question_list_csv_format, (4, 5, 6))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)