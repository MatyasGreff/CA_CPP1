# CA_CPP1
CA final submission code
Django project for the CPP module To run this app locally, start a new virtual environment and install the dependencies from requirements.txt.
Some of the details are placeholders in the main settings file, to make the app work you need to set up a public S3 bucket and set up an IAM user with full access to it.

AWS_S3_ACCESS_KEY_ID = 'Access key ID of your IAM user' AWS_S3_SECRET_ACCESS_KEY = 'Access key of your IAM user' AWS_STORAGE_BUCKET_NAME = 'Your bucket name' # These are needed for Django storages, so the app can connect to the S3 bucket
