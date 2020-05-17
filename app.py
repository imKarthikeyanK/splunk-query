from flask import Flask, render_template, request, redirect, url_for
from splunk_utils import query_splunk
from flask_mail import Mail, Message
from config import Config
from threading import Thread

app = Flask(__name__)

# configuring app with the imported mail config
app.config.from_object(Config)

# creating mail instance
mail = Mail(app)


"""
mailer method to send mails
args:
receipient => string receipient mail id
subject => string subject
body => string body of mail
"""
def mailer(recipient, subject, body):
    with app.app_context():
        msg = Message(
            subject,
            recipients=[recipient],
            body=body
        )

        # attaching splunk-result to the mail
        with app.open_resource("files/splunk-result.txt") as fs:
            msg.attach('splunk-result.txt', "text/plain", fs.read())
        
        # mail dispatch
        mail.send(msg)


# landing route reders the form
@app.route("/")
def index():
    status = "index"
    if request.args:
        status = request.args["status"]
    return render_template("index.htm", status=status)


# form submission route
@app.route("/splunk-query", methods=['POST'])
def splunk_query():
    if request.method == "POST":
        data = request.form # submitted form data
        host, port = data["ip"].split(":")
        username = data["username"]
        password = data["password"]
        query = data["query"]
        time_range = data["range"]
        email = data["email"]

        status = "failed"  # initial status of process

        # calls the query method to retrieve data from splunk
        try:
            result = query_splunk(host, port, username, password, query, time_range)
        except TimeoutError:
            print("TimeOutError")

        print(result)

        # mail is sent only if we have got any data from splunk 
        # else User will be informed in the UI 
        if result:
            status="success"

            # result is stored in text file, keeping in mind
            # that passing such big data in mail wont mean good
            with open("files/splunk-result.txt", "w") as f:
                f.write(str(result))
            
            # static subject and body info
            SUBJECT = "Splunk Query Result"
            BODY = "The Splunk results for request query ('{}') has been attached as " \
                    "a file. \nPlease have a look.".format(query)
            
            # mailer method is passed into thread to avoid blocking
            thr = Thread(target=mailer, args=[email.strip(), SUBJECT, BODY])
            thr.start()

        return redirect(url_for('index', status=status))


if __name__ == "__main__":
    app.run(debug=True)
