from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/splunk-query", methods=['POST'])
def splunk_query():
    if request.method == "POST":
        data = request.form
        print(data)

    return render_template("index.htm")

if __name__ == "__main__":
    app.run(debug=True)
