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
        rv = self.myapp.get('login?email=milandungrani42@gmail.com&password=123456')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], str('successfully login'))

    #wrong password
    def test_login1(self):
        rv = self.myapp.get('login?email=milandungrani42@gmail.com&password=1234')
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
        rv = self.myapp.get('signup')
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
        rv1 = self.myapp.get('/details?email=milandungrani42@gmail.com&password=12345678')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], 'wrong password or email')

    #login and then check details page
    def test_details3(self):
        rv1 = self.myapp.get('/details?email=milandungrani42@gmail.com&password=123456')
        self.assertEqual(str(rv1.data).split('b')[1].split("'")[1], 'success')
    
    #for logout
    def test_logout(self):
        rv = self.myapp.get('/logout')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'logouted')

    #autofill after successful login
    def test_autofill(self):
        rv = self.myapp.get('/autofill?email=milandungrani42@gmail.com&password=123456&url=https://www.github.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'success')

    #autofill after wrong login
    def test_autofill2(self):
        rv = self.myapp.get('/autofill?email=milandungrani42@gmail.com&password=12345&url=https://www.github.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'Invalid')
    
    #autofill after wrong login details
    def test_autofill3(self):
        rv = self.myapp.get('/autofill?email=pp@p&password=1234564&url=https://www.github.com')
        self.assertEqual(str(rv.data).split('b')[1].split("'")[1], 'wrong login')

    #checking weather page is opening or not
    def test_loginwebsite(self):
        rv = self.myapp.get('/login_website')
        self.assertEqual(rv.status, '200 OK') 
        
    # def test_autoupdate(self):
    #     rv = self.myapp.get('afss.herokuapp.com/autoupdate')
    #     self.assertEqual(rv.status, '500 INTERNAL SERVER ERROR')



       
