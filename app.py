from flask import Flask, render_template, request
from splunk_utils import query_splunk

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/splunk-query", methods=['POST'])
def splunk_query():
    if request.method == "POST":
        data = request.form
        print(data)
        for i in data:
            print(i, data[i])

    return render_template("index.htm")

if __name__ == "__main__":
    app.run(debug=True)
