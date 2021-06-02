import os
# import boto3
from flask import Flask, render_template, redirect, request, url_for

# Initialize Flask app
app = Flask(__name__)

# # Initialize Amazon S3 storage
# s3 = boto3.resource('s3')

ERROR = None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=["POST"])
def upload():
    global ERROR

    img = request.files.get("img")

    try:
        # s3.Bucket('bucket_name').put_object(Key=img.filename, Body=img.read())
        print(img.filename)
        return redirect(url_for("upload_success"))

    except Exception as e:
        ERROR = e
        print("[-] Error:", e)
        return redirect(url_for("home"))


@app.route("/upload/success")
def upload_success():
    return render_template("upload_success.html")


@app.route("/upload/fail")
def upload_fail():
    return render_template("upload_fail.html", error=ERROR)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
