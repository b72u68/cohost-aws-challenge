import psycopg2
import boto3
from flask import Flask, render_template, redirect, request, url_for
from config import postgres, s3_config

ERROR = None
DB = None

# Initialize Flask app
app = Flask(__name__)

# Initialize Amazon S3
s3 = boto3.resource('s3')

BUCKET = s3.Bucket(s3_config["BUCKET"])


# Initialize Amazon RDS
try:
    print('\n[+] Connecting to the database...\n')
    DB = psycopg2.connect(host=postgres["ENDPOINT"],
                          port=postgres["PORT"],
                          user=postgres["USR"],
                          dbname=postgres["DBNAME"],
                          password=postgres["PASSWORD"])
except Exception as e:
    ERROR = e
    print('\n[-] Error while connecting to the database:\n', e)
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
    global DB, ERROR

    try:
        img = request.files.get("img")
        url = s3_config["URI"] + img.filename

        if DB:
            cur = DB.cursor()

            try:
                # Store filename and url in database
                cur.execute('insert into images (name, url) values (%s,%s)',
                            (img.filename, url))
                DB.commit()

            except psycopg2.IntegrityError:
                DB.rollback()
                cur.execute('select * from images where substring(name,1,%s) = %s',
                            (str(len(img.filename)), img.filename))

                num_of_dup = len(cur.fetchall())

                filename = '.'.join(img.filename.split('.')[:-1])
                file_ext = img.filename.split('.')[-1]
                img.filename = f'{filename}({num_of_dup}).{file_ext}'

                url = s3_config["URI"] + img.filename

                cur.execute('insert into images (name, url) values (%s,%s)',
                            (img.filename, url))
                DB.commit()

            finally:
                BUCKET.put_object(Key=img.filename, Body=img.read())

            cur.close()

        return redirect(url_for("upload_success"))

    except Exception as e:
        ERROR = e
        print('[-] Error while uploading file:\n', e)
        return redirect(url_for("upload_fail"))


@app.route("/upload/success")
def upload_success():
    return render_template("upload_success.html")


@app.route("/upload/fail")
def upload_fail():
    return render_template("upload_fail.html", error=ERROR)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
