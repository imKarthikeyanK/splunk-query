# Splunk-Query - Flask Application

This app lets you connect to a remote splunk server and query info from that server. On successfull quering the results will be sent to the given mail id as a text file. The app has Flask in backend and Jinja2 templates in frontend.

# Mail configuration
first we need to configure the mail to receive mail notifications
```bash
1. open config.py
2. change values according to your mail configurations
3. if its gmail then just change MAIL_USERNAME and MAIL_PASSWORD and MAIL_DEFAULT_SENDER
```

# installation

To install the system should have `python 3.5` or greater and use [PIP](https://pip.pypa.io/en/stable/) to install packages.
``` bash
1. clone or download the repository
2. create a virtual env
3. activate the virtual env
4. pip install -r requirements.txt
```

# Usage
to run the server please follow the below instructions
```bash
run python app.py
app will be running in localhost 127.0.0.1:5000
```

