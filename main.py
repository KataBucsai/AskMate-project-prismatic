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
    question_list = data_manager.get_table_from_file(file_name)
    question_list = data_manager.base64_decoder(question_list, (4, 5, 6))
    question_list = data_manager.table_sort(question_list, 1, True)
    return render_template('list_questions.html', question_list=question_list)


if __name__ == '__main__':
    app.run(debug=True)