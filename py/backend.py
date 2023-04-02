from flask import Flask, render_template, request
from ValdevianTranslator import ValdevianTranslator
import os

translate_text = ValdevianTranslator("t5-small")
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
app = Flask(__name__, template_folder=f'{parent_dir}\\html', static_folder='static')

@app.route("/")
def home():
    return render_template("welcome.html")
@app.route("/translator")
def translator():
    return render_template("translate.html")

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form['input_text']
    model_input = request.form['model']
    translate_text = ValdevianTranslator(model_input)
    translated_text = translate_text.generate_response(input_text)
    return translated_text
@app.route('/req', methods=['GET'])
def requirements():
    return render_template("requirements.html")


if __name__ == "__main__":
    app.run(debug=True)
