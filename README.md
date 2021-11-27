# django-bot-server-tutorial

To run old Django with new Python3 follow instructions given here `https://stackoverflow.com/a/65880079`

The above instruction is necessary because I've added User model for authentication.


## Step 1: Install requirements.txt

`pip install -r requirements.txt`

## Step 2: Create databases

Create the databases and the initial migrations with the following command:
`python manage.py migrate`

## Step 3: Run server

And start the server with 

`python manage.py runserver`

You should now be able to go to localhost:8000/chat/ and chat with the bot
