import unittest
import os
import app.utils as utils
import tests.TestUtil as testUtil
from app.model.user import User
from app.model.account import Account


class Test_Account(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testUtil.setupData()
        #setup test user data
        self.user = User("test_user")
        self.user.changePassword("test_password")
        #setup some accounts
        account = Account("Facebook")
        account.setAccountUsername("user_fb")
        self.user.addAccount(account, "pass_fb")
        account2 = Account("Instagram")
        account2.setAccountUsername("user_instagram")
        self.user.addAccount(account2, "pass_instagram")

    @classmethod
    def tearDownClass(self):
        testUtil.tearDown()

    def test_add_remove_account(self):
        accountName = "Google"
        accountUsername = "userGoogle"
        accountPass = "googlePassword"        
        account = Account(accountName)
        account.setAccountUsername(accountUsername)
        self.user.addAccount(account, accountPass)

        accountList = self.user.getAccountList()
        self.assertEqual(len(accountList), 3)
        self.assertIn(account, accountList)

        self.assertTrue(self.user.isAccountExist(account))
        
        self.user.removeAccount(account)
        self.assertEqual(len(accountList), 2)
        self.assertNotIn(account, accountList)

    def test_list_accounts(self):
        accountList = self.user.getAccountList()
        self.assertEqual(len(accountList), 2)
        self.assertEqual(accountList[0].accountName, "Facebook")
        self.assertEqual(accountList[0].accountUsername, "user_fb")
        self.assertEqual(accountList[1].accountName, "Instagram")
        self.assertEqual(accountList[1].accountUsername, "user_instagram")

    def test_decrypt_password(self):
        account_fb = self.user.getAccountList()[0]
        self.assertEqual(utils.decrypt(account_fb.getAccountPassword(), self.user.getPassword()), "pass_fb")
        account_instagram = self.user.getAccountList()[1]
        self.assertEqual(utils.decrypt(account_instagram.getAccountPassword(), self.user.getPassword()), "pass_instagram")  


    
