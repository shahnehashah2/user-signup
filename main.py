import webapp2
import re
import cgi

class MainHandler(webapp2.RequestHandler):
    def makeform(self, username='', email='', usernameErr='', passwordErr='',
                    confirmPasswordErr='', emailErr=''):
        form = '''<form method='post'>
                    <h2>Signup</h2>
                    <label>Username
                        <input type='text' name='username' value=%(username)s>
                    </label>
                    %(usernameErr)s
                    <br>
                    <label>Password
                        <input type='password' name='password'>
                    </label>
                    %(passwordErr)s
                    <br>
                    <label>Confirm Password
                        <input type='password' name='confirmpassword'>
                    </label>
                    %(confirmPasswordErr)s
                    <br>
                    <label>Email(optional)
                        <input type='text' name='email' value=%(email)s>
                    </label>
                    %(emailErr)s
                    <br>
                    <input type='submit'>
                </form>'''
        self.response.write(form% {'username':username,
                                'email':email,
                                'usernameErr':usernameErr,
                                'passwordErr':passwordErr,
                                'confirmPasswordErr':confirmPasswordErr,
                                'emailErr':emailErr})

    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        return PASS_RE.match(password)

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return EMAIL_RE.match(email)

    def get(self):
        self.makeform()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirmpassword = self.request.get("confirmpassword")
        email = self.request.get("email")

        usernameErr = ''
        passwordErr = ''
        confirmPasswordErr = ''
        emailErr = ''

        if username == '':
            usernameErr = "The username cannot be blank"
        elif not self.valid_username(username):
            usernameErr = "Invalid Username"
        if password == '':
            passwordErr = "The password cannot be blank"
        elif not self.valid_password(password):
            passwordErr = "Invalid Password"
        elif password != confirmpassword:
            confirmPasswordErr = "The passwords must match"
        if email:
            if not self.valid_email(email):
                emailErr = "Invalid Email"

        if usernameErr or passwordErr or confirmPasswordErr or emailErr:
            self.makeform(cgi.escape(username), cgi.escape(email), usernameErr,
                        passwordErr, confirmPasswordErr, emailErr)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.write("<h1>Welcome " + self.request.get(username) + "</h1>")

app = webapp2.WSGIApplication([
                ('/', MainHandler),
                ('/welcome', Welcome)
                ], debug=True)
