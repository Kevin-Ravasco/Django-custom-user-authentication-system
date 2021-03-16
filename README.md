# Django Custom Auth System 
this project is a custom user model in django that uses email field instead of the username field to signup or signin.
when user signs up, he is prompted to confirm his/her email as a confirmation link is sent to the email he/she used
to sign up to the site. After successfull confirmation, then the user can log in.

The app has tests written in accounts/tests directory.

the project contains a registrtion and a login page for user creation and login.
it has a simple home page which when successfully logged in the user is redirected to.
the home veiw has @login_required decorator hence unauthenticated users cannot view the homepage.

the app is called accounts and has its templates in templates/accounts



to change from the built in django user model, in settings.py we added:

AUTH_USER_MODEL = 'accounts.User' #changes the built-in user model to ours

Note:
Superuser account:
email: admin@gmail.com
pass: admin

### Features Summary
1. Use email instead of username to authenticate
2. Send user emails upon registration. During redistration, a user cannot log in until he/she confirms their email
3. Brute force attack protection. A limit is set on maximum login attempts. When the attempts are exceeded, 
  the user is set active=False to protect the account and an email to notify the user of the suspecious activity
  is sent. The user can also recover their account using a link provided in this email.
  
  This login limit is set in settings.py as MAX_LOGIN_ATTEMPTS 
4.Time limit after each login is also set in seconds to provide some space between successive login attempts
  This is set in settings.py as LOGIN_ATTEMPTS_TIME_LIMIT

### Improvement.
You can use a background process to send the auth emails. e.g. Celery.


### Testing
Tests written in accounts/tests
