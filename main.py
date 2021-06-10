import psycopg2
import boto3
from flask import Flask, render_template, redirect, request, url_for

ERROR = None
DB = None

# Initialize Flask app
app = Flask(__name__)

# Initialize Amazon S3
s3 = boto3.resource('s3')

BUCKET = s3.Bucket('mdinh-aws-challenge')

# Initialize Amazon RDS
ENDPOINT = "mdinh-dbs.cesr1n4cmq2m.ap-southeast-1.rds.amazonaws.com"
PORT = "5432"
USR = "mdinh"
REGION = "ap-southeast-1a"
DBNAME = "mdinh-dbs"

try:
    print('[+] Connecting to the database...')
    DB = psycopg2.connect(host=ENDPOINT,
                          port=PORT,
                          user=USR,
                          password=SOME TOKEN)
except Exception as e:
    ERROR = e
    print('[-] Error while connecting to the database:\n', e)
    redirect(url_for('upload_fail'), error=ERROR)


def get_uploaded_files():
    return [f.key for f in BUCKET.objects.all()]


@app.route("/")
def home():
    global ERROR
    ERROR = None

    uploaded_files = get_uploaded_files()

    return render_template("home.html", uploaded_files=uploaded_files)


@app.route("/upload", methods=["POST"])
def upload():
    global ERROR

    try:
        img = request.files.get("img")
        uploaded_img = BUCKET.put_object(Key=img.filename, Body=img.read()).key

        print(uploaded_img)

        return redirect(url_for("upload_success"))

    except Exception as e:
        ERROR = e
        return redirect(url_for("upload_fail"))


@app.route("/upload/success")
def upload_success():
    return render_template("upload_success.html")


@app.route("/upload/fail")
def upload_fail():
    return render_template("upload_fail.html", error=ERROR)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
