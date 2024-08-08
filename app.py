from flask import Flask, render_template
import modules.generate_text

app = Flask(__name__)

@app.route('/')
def home():
    text1,text2 = modules.generate_text.Generate_text()
    return render_template('index.html',text1=text1,text2=text2)

if __name__ == "__main__":
    app.run(debug=True)