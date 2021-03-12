import unittest
from test.unit.user.test_login import TestLogin
from test.unit.user.test_signin import TestSignin
from test.unit.user.test_editProfile import TestEditProfile
# Login
suite_login = unittest.TestSuite()
suite_login.addTest(TestLogin("test_access"))
suite_login.addTest(TestLogin("test_user"))

# Signin
suite_signin = unittest.TestSuite()
suite_signin.addTest(TestSignin("test_signin_successfully"))
suite_signin.addTest(TestSignin("test_signin_error"))

# EditProfile
suite_editProfile = unittest.TestSuite()
suite_editProfile.addTest(TestEditProfile("test_edit_profile"))
suite_editProfile.addTest(TestEditProfile("test_edit_profile_error"))


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    #runner.run(suite_login)
    runner.run(suite_signin)
    #runner.run(suite_editProfile)
