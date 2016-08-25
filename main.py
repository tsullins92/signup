import webapp2
import cgi
import re

page_header = """
<!DOCTYPE HTML>
<html>
<head>
    <title>Signup</title>
    <style type = "css/text">
        .error {
            color: red
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Caesar</a>
    </h1>
"""

page_footer = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):
    def get(self):

        error=self.request.get("error")
        error_escaped=cgi.escape(error,quote=True)

        username=self.request.get("username")
        username_escaped=cgi.escape(username,quote=True)

        password=self.request.get("password")
        password_escaped=cgi.escape(password,quote=True)

        verify_password=self.request.get("verify_password")
        verify_password_escaped=cgi.escape(verify_password,quote=True)

        email=self.request.get("email")
        email_escaped=cgi.escape(email,quote=True)

        forms = """
            <form action="/welcome" method="post">
                <label>
                    Username
                    <input type="text" name="username" value="{0}"/>
                </label>
                <label>
                    Password
                    <input type="password" name="password"/>
                </label>
                <label>
                    Verify Password
                    <input type="password" name="verify_password"/>
                </label>
                <label>
                    Email (optional)
                    <input type="text" name="email" value="{1}"/>
                </label>
                <input type="submit" value="Submit"/>
            </form>{2}
            """.format(username_escaped,email_escaped,error_escaped)

        response = page_header + forms + page_footer

        self.response.write(response)

class Welcome(webapp2.RequestHandler):

    def post(self):

        username=self.request.get("username")
        username_escaped=cgi.escape(username,quote=True)

        password=self.request.get("password")
        password_escaped=cgi.escape(password,quote=True)

        verify_password=self.request.get("verify_password")
        verify_password_escaped=cgi.escape(verify_password,quote=True)

        email=self.request.get("email")
        email_escaped=cgi.escape(email,quote=True)

        error=""
        if re.search("\s", username):
            error = "Username cannot contain spaces"
        elif len(username)>20:
            error = "Username cannot be longer than 20 characters"

        elif re.search("\s", password):
            error = "Password cannot contain spaces"
        elif len(password)>30:
            error = "Password cannot be longer than 30 characters"
        elif password!=verify_password:
            error = "Verify Password and password must be the same"

        elif re.search("\s", email):
            error = "Email cannot contain spaces"
        elif len(email)>50:
            error = "Email cannot be longer than 50 characters"

        welcome = "<h3>Welcome <b>" + username + "!</b></h3>"

        if not error:
            response = page_header + welcome + page_footer
            self.response.write(response)
        else:
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped + "&username=" + username_escaped + "&email=" + email_escaped)












app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
