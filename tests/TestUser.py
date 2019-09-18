import unittest
import app.utils as utils
import tests.TestUtil as testUtil
import os
from app.model.user import User


class Test_User(unittest.TestCase):
    @classmethod
    def setUpClass(self):        
        #setup test user data
        testUtil.setupData()
        self.user = User("test_user")
        self.user.changePassword("test_password")
        
    @classmethod
    def tearDownClass(self):
        testUtil.tearDown()

    def test_match_password(self):
        passwd1 = self.user.getPassword()
        passwd2 = "test_different_password"
        matched = self.user.matchPassword(passwd1)
        self.assertTrue(matched)
        not_matched = self.user.matchPassword(passwd2)
        self.assertFalse(not_matched)

        #change password
        self.user.changePassword(passwd2)
        self.assertFalse(self.user.matchPassword(passwd1))
        self.assertTrue(self.user.matchPassword(passwd2))

    def test_is_user_exist(self):
        user2 = User("test_user")
        self.assertTrue(user2.isExisting())
        user3 = User("Test_User")
        self.assertFalse(user3.isExisting())
        self.assertTrue(self.user.getUsername(), "test_user")
