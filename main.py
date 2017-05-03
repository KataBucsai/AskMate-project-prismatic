from flask import Flask, render_template, request, redirect
import csv
import data_manager
import os
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)