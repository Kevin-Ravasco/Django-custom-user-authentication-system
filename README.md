# CustomUserModelDjango
this project is a custom user model in django that uses email field instead of the username field to signup or signin.

the project contains a registrtion and a login page for user creation and login.
it has a simple home page which when successfully logged in the user is redirected to.
the home veiw has @login_required decorator hence unauthenticated users cannot view the homepage.

the app is called accounts and has its templates in templates/accounts



to change from the built in django user model, in settings.py we added:

AUTH_USER_MODEL = 'accounts.User' # changes the built-in user model to ours

Note:
Superuser account:
email: admin@gmail.com
pass: admin

