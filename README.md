# CoHost AI AWS Challenge

## Objective

Write an image uploader website and run it on Amazon Web Services using EC2 service and S3 storage.

## Tasks

- Create an AWS account
- Use S3 and EC2 services for hosting server and storing images.
- Include simple frontend and backend. Call service request through REST API.

## Local setup

### Create a virtual env (optional)

Install `virtualenv` using `pip` or `pip3`:

```
pip install virtualenv
```

Create a virtual environment (in this case, it is named `venv`):

```
virtualenv venv
```

Change current developement environment to `virtualenv`:

```
source ./venv/bin/activate
```

Deactivate the virtual environment:

```
deactivate
```

### Install required packages

```
pip install -r requirements.txt
```

## Start website 

```
python3 main.py
```

## Access

The website is at `http://localhost:5000/`.
