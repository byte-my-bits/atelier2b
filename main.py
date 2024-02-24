from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.core import Field
from wtforms.validators import InputRequired
from wtforms import Label
import json
import mammoth

import os
import win32com.client

def docx_to_html(file_path):
    with open(file_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value  # The generated HTML
        return html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


@app.route('/', methods=['GET', 'POST'])
def home():
    with open('data/base_struct_config.json') as f:
        json_structure = json.load(f)
    html = docx_to_html('data/exemplu.docx')
    return render_template('form.html', data=json_structure,isinstance=isinstance,html=html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


from docx import Document

# # DE ARATAT LUI ALINA

# import time

# start_time = time.time()

# # Existing code here


# def replace_text_in_docx(input_file_path, output_file_path, old_text, new_text):
#     doc = Document(input_file_path)
#     for paragraph in doc.paragraphs:
#         for run in paragraph.runs:
#             if old_text in run.text:  # Only replace text in runs that contain the old text
#                 run.text = run.text.replace(old_text, new_text)
#     doc.save(output_file_path)

# m_Template = "data/memoriu_dtac_template.docx"
# m_outputDocx = "data/memoriu_dtac_modified.docx"
# m_outputPdf = "data/memoriu_dtac_modified.pdf"

# start_time_delete = time.time()
# if os.path.exists(m_outputDocx):
#     os.remove(m_outputDocx)

# if os.path.exists(m_outputPdf):
#     os.remove(m_outputPdf)

# end_time_delete = time.time()
# execution_time_delete = end_time_delete - start_time_delete
# print(f"Execution time delete: {execution_time_delete} seconds")

# start_time_replace = time.time()
# # Use the function
# replace_text_in_docx(m_Template, m_outputDocx, '@TITLU_PROIECT@', 'TIKI TAKA BARCELONA')
# replace_text_in_docx(m_outputDocx, m_outputDocx, '@AMPLASAMENT@', 'Județul Botoșani, Comuna Mihai Eminescu, Sat Cătămărești Deal, strada Mihai Eminescu, nr. 58B')
# replace_text_in_docx(m_outputDocx, m_outputDocx, '@SEF_PROIECT@', 'Arh. Călin Popovici')
# replace_text_in_docx(m_outputDocx, m_outputDocx, '@PROIECTANT_GENERAL@', 'Arh. Călin Popovici')
# replace_text_in_docx(m_outputDocx, m_outputDocx, '@PROIECTANT@', 'Arh. Grigoraș Alina')
# # replace_text_in_docx(m_outputDocx, m_outputDocx, '@BENEFICIAR@', 'Nelu Scobitoare')

# end_time_replace = time.time()
# execution_time_replace = end_time_replace - start_time_replace
# print(f"Execution time replace: {execution_time_replace} seconds")

# def docx_to_pdf(input_file_path, output_file_path):
#     word = win32com.client.Dispatch('Word.Application')
#     doc = word.Documents.Open(input_file_path)
#     doc.SaveAs(output_file_path, FileFormat=17)  # 17 represents the PDF format in Word
#     doc.Close()
#     word.Quit()

# start_time_convert = time.time()
# # Use the function
# docx_to_pdf(os.path.abspath(m_outputDocx), os.path.abspath(m_outputPdf))

# end_time_convert = time.time()
# execution_time_convert = end_time_convert - start_time_convert
# print(f"Execution time convert: {execution_time_convert} seconds")

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")