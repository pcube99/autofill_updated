from application_temp import myapp
import unittest
import requests
# python -m unittest test_app
class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.myapp = myapp.test_client()
    #main page is loaded
    def test_main(self):
        rv = self.myapp.get('/')
        self.assertEqual(rv.status, '200 OK')

    #login
    def test_login(self):
        rv = self.myapp.get('login?email=gg3@mailsac.com&password=123456')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], str('successfully login'))

    #wrong password
    def test_login1(self):
        rv = self.myapp.get('login?email=gg3@mailsac.com&password=1234')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], str('Invalid'))

    #wrong email
    def test_login2(self):
        rv = self.myapp.get('login?email=milan&password=123456')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], str('Invalid'))

    #no user exists
    def test_login3(self):
        rv = self.myapp.get('login?email=milan@d.com&password=123456')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], str('failed login'))
	
    #try to find out route which is not there
    def test_404(self):
        rv = self.myapp.get('/other')
        self.assertEqual(rv.status, '404 NOT FOUND')

    #signup page is working
    def test_signup(self):
        rv = self.myapp.get('/signup')
        self.assertEqual(rv.status, '200 OK')

    #checking help page
    def test_help(self):
        rv = self.myapp.get('/help')
        self.assertEqual(rv.status, '200 OK')

    #without login check details page
    def test_details(self):
        rv = self.myapp.get('/details?email=pp@p.co&password=123456')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'wrong login')

    #invalid login while showing details
    def test_details2(self):
        rv = self.myapp.get('/details?email=pp.x&password=123456')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'Invalid')

    #login and then check details page
    def test_details1(self):
        rv1 = self.myapp.get('/details?email=gg3@mailsac.com&password=12345678')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], 'wrong password or email')

    #login and then check details page
    def test_details3(self):
        rv1 = self.myapp.get('/details?email=gg3@mailsac.com&password=123456')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], 'success')
    
    #for logout
    def test_logout(self):
        rv = self.myapp.get('/logout')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'logouted')

    #autofill after successful login
    def test_autofill(self):
        rv = self.myapp.get('/autofill?email=gg3@mailsac.com&password=123456&url=https://www.github.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'success')

    #autofill after wrong login
    def test_autofill2(self):
        rv = self.myapp.get('/autofill?email=gg3@mailsac.com&password=12345&url=https://www.github.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'Invalid')
    
    #autofill after wrong login details
    def test_autofill3(self):
        rv = self.myapp.get('/autofill?email=pp@p&password=1234564&url=https://www.github.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'wrong login')

    #checking weather page is opening or not
    def test_loginwebsite(self):
        rv = self.myapp.get('/login_website')
        self.assertEqual(rv.status, '200 OK') 

    #autoupdate when true details
    def test_autoupdate(self):
        rv = self.myapp.get('/autoupdate?email=gg3@mailsac.com&password=123456&id=name&value=pankil')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'success')

    #autoupdate when wrong email or pass
    def test_autoupdate1(self):
        rv = self.myapp.get('/autoupdate?email=gg3@mailsac.com&password=1234567&id=email&value=201601094daiict@gmail.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'wrong password or email')

    # autoupdate when no such user exists 
    def test_autoupdate2(self):
        rv = self.myapp.get('/autoupdate?email=201601094daiic@gmail.com&password=qwer1234&url=https://github.com&id=email&value=201601094daiict@gmail.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'wrong login')

    # verify when no such user exists
    def test_verify(self):
        rv1 = self.myapp.get('/verify?email=milandungrani@gmail.com&password=123456')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], "invalid login")

    # verify when user is already verified
    def test_verify1(self):
        rv1 = self.myapp.get('/verify?email=gg3@mailsac.com&password=123456&otp=2421')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], "already verified")

    # verify when user enters right otp
    def test_verify2(self):
        rv1 = self.myapp.get('/verify?email=lysander.jeriko@bullstore.net&password=123456&otp=2421')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], "verified")

    # verify when user enters wrong otp
    def test_verify3(self):
        rv1 = self.myapp.get('/verify?email=lysander.jeriko@bullstore.net&password=123456&otp=2422')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], "wrong otp")

    # change password when user enters different password than sent to his registered mail
    def test_changepass(self):
        rv1 = self.myapp.get('/changedpassword?reset_pass=123456')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], "enter the password which is sent to your registered email")

    # change password when user enters same password as sent to his registered mail
    def test_changepass1(self):
        rv1 = self.myapp.get('/changedpassword?reset_pass=654321')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], "password changed")

    #check response of resend page
    def test_resend(self):
        rv = self.myapp.get('/resend')
        self.assertEqual(rv.status, '200 OK')
    