

# Wall Management App
Wall App is an application that allows users to register, login, reset password along with that it has wall management feature.

## Registration and Login:
create a new user and this new user receives a welcome email. New users can then log in. If the user forgets his/her password then he/she can reset their own password by providing a registered email address.

## Wall (authed):

After logging in, a user can post messages on the site-wide wall along with that user can edit/delete his/her own messages & also authed users can comments on others' messages. It has the feature of edit/delete own comments.
 
## Wall (guest):

Guests as well as authed users can see all of the messages on the wall & the comments.


It has Automated tests to confirm the functionality of the above requirements. 
This project contains the Django back-end with Django REST framework and back-end code required to make it all work.





## Django setup instructions.


1. Create a python virtual environment using below command.

   `python3 -m venv virtual-env`

2. Activate the environment.

   `source virtual-env/bin/activate`

3. Install dependencies.

   `pip install -r requirements.txt`

4. You can configure the DB for local/production if you wish in `settings.local.py/production.py`

5. You can configure the Email smtp settings in `settings.settings.py`

6. If you are using a fresh database in local, execute these commands.

   `python manage.py makemigrations `

   `python manage.py migrate`

7. Run this command and your django app should be running on port `8000`

   `python manage.py runserver`


