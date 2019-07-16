import wx
import wx.grid as grid
from app.view.UserSetting import UserSetting
from app.model.account import Account

class ChangePasswordDialog(wx.Dialog): 
    def __init__(self, parent, title, user): 
        super(ChangePasswordDialog, self).__init__(parent, title = title, size = (350,250)) 
        panel = UserSetting(self, user)

    def CloseUserSetting(self, returnCode="CANCEL"):
        if returnCode == "SUCCESS":
            self.EndModal(wx.ID_OK)
        self.Destroy()

class MainWindow(wx.Frame):
   
    def __init__(self, user, *args, **kw):
        # ensure the parent's __init__ is called
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                                wx.MAXIMIZE_BOX | wx.CLOSE_BOX)
        wx.Frame.__init__(self, None, style=no_resize)
        self.user = user
        self.mode = "new"

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        # and put some text with a larger bold font on it
        st = wx.StaticText(self.pnl, label="Password Manager", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        self.btnNew = wx.Button(self.pnl, label="&New")
        self.btnRemove = wx.Button(self.pnl, label="&Remove")
        self.btnEdit = wx.Button(self.pnl, label="&Edit")        

        #create grid
        self.list_ctrl = wx.ListCtrl(self.pnl, size=(0,200),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         |wx.LC_SORT_ASCENDING
                         )
        
        
        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Ready.")

        buttonLayout = wx.BoxSizer(wx.VERTICAL)
        buttonLayout.Add(self.btnNew, 0, wx.ALL, 10)
        buttonLayout.Add(self.btnEdit, 0, wx.ALL, 10) 
        buttonLayout.Add(self.btnRemove, 0, wx.ALL, 10)

        middleBox = wx.BoxSizer(wx.HORIZONTAL)
        middleBox.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND)
        middleBox.Add(buttonLayout, 0, wx.CENTRE)
        middleBox.Add(self.buildEditAccount(), 1, wx.ALL|wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.VERTICAL)        
        sizer.Add(st, 0, wx.CENTRE)
        sizer.AddSpacer(20)
        sizer.Add(middleBox, 1, wx.ALL|wx.EXPAND, 15)

        sizerBox = wx.BoxSizer()
        sizerBox.Add(self.pnl, 1, wx.EXPAND)

        #set icon
        ico = wx.Icon('pw.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        #Layout sizers
        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(1)
        sizer.Fit(self.pnl)        
        self.SetSizer(sizerBox)
        self.clearEditAccount()

        self.list_ctrl.InsertColumn(0, 'Account')
        self.list_ctrl.InsertColumn(1, 'Username')
        self.listAccounts()

        #bind buttons
        self.bindButtons()

    def bindButtons(self):        
        self.btnCancel.Bind(wx.EVT_BUTTON, self.cancelEditAccount)
        self.btnCopy.Bind(wx.EVT_BUTTON, self.copyPassword)
        self.btnEdit.Bind(wx.EVT_BUTTON, self.editAccount)
        self.btnNew.Bind(wx.EVT_BUTTON, self.newAccount)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.deleteAccount)
        self.btnSave.Bind(wx.EVT_BUTTON, self.saveAccount)        
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelected)
        self.list_ctrl.Bind(wx.EVT_SIZE, self.sizeColumns)
        self.passTxt.Bind(wx.EVT_TEXT_ENTER, self.saveAccount)
        self.repassTxt.Bind(wx.EVT_TEXT_ENTER, self.saveAccount)
        

    def buildEditAccount(self):
        accountLbl = wx.StaticText(self.pnl, label="Account Name:")      
        self.accountTxt = wx.TextCtrl(self.pnl)
        usernameLbl = wx.StaticText(self.pnl, label="Username:")      
        self.usernameTxt = wx.TextCtrl(self.pnl)
        passLbl = wx.StaticText(self.pnl, label="Password:")        
        self.passTxt = wx.TextCtrl(self.pnl, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.repassLbl = wx.StaticText(self.pnl, label="Re-enter Password:")        
        self.repassTxt = wx.TextCtrl(self.pnl, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        #buttons
        self.btnSave = wx.Button(self.pnl, label="&Save")
        self.btnCancel = wx.Button(self.pnl, label="&Cancel")
        self.btnCopy = wx.Button(self.pnl, label="&Copy Password")

        buttonLayout = wx.BoxSizer(wx.HORIZONTAL)
        buttonLayout.Add(self.btnCancel, 0, wx.ALL)        
        buttonLayout.AddSpacer(10)
        buttonLayout.Add(self.btnSave, 0, wx.ALL)
        buttonLayout.Add(self.btnCopy, 0, wx.ALL)

        self.grid = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid.Add(accountLbl, pos=(0,0))
        self.grid.Add(self.accountTxt, pos=(0,1), flag=wx.EXPAND|wx.ALL)
        self.grid.Add(usernameLbl, pos=(1,0))
        self.grid.Add(self.usernameTxt, pos=(1,1), flag=wx.EXPAND|wx.ALL)
        self.grid.Add(passLbl, pos=(2,0))
        self.grid.Add(self.passTxt, pos=(2,1), flag=wx.EXPAND|wx.ALL)
        self.grid.Add(self.repassLbl, pos=(3,0))
        self.grid.Add(self.repassTxt, pos=(3,1), flag=wx.EXPAND|wx.ALL)
        self.grid.AddGrowableCol(1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(self.grid, 0, wx.EXPAND | wx.ALL)
        sizer.AddSpacer(15)
        sizer.Add(buttonLayout, 0, wx.ALIGN_RIGHT)
        return sizer

    def cancelEditAccount(self, event):
        dlg = wx.MessageDialog(self, 
        "Do you want to discard your changes?",
        "Confirm Exit",  wx.YES_NO|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            self.clearEditAccount()
            if self.mode == "new": #deselect item
                self.list_ctrl.SetItemState(self.selectedIndex, 0, wx.LIST_STATE_SELECTED)

    def changePassword(self, event):
        dialog = ChangePasswordDialog(self, "Change Password", self.user)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            self.list_ctrl.DeleteAllItems()
            self.listAccounts() 
        

    def clearEditAccount(self):
        self.btnNew.Enable()        
        self.btnCopy.Show()        
        self.accountTxt.SetEditable(False)
        self.usernameTxt.SetEditable(False)
        self.passTxt.SetEditable(False)
        self.repassTxt.SetEditable(False)
        self.repassTxt.Hide()
        self.repassLbl.Hide()
        self.btnSave.Hide()
        self.btnCancel.Hide()
        if self.mode == "new":
            self.btnEdit.Disable()
            self.btnRemove.Disable()
            self.btnCopy.Disable()
            self.clearFormAccount()
        else:
            self.btnCopy.Enable()
            self.btnEdit.Enable()
            self.btnRemove.Enable()
            self.passTxt.SetValue("xxxxxxxx")
            self.repassTxt.SetValue("")
        self.Layout()

    def clearFormAccount(self):
        self.accountTxt.SetValue("")
        self.usernameTxt.SetValue("")
        self.passTxt.SetValue("")
        self.repassTxt.SetValue("")

    def copyPassword(self, event):
        self.selectedAccount.copyPassword(self.user.getPassword())
        self.showDialog("Password has been copied to the clipboard", "Information", wx.OK|wx.ICON_INFORMATION)
        
    def deleteAccount(self, event):
        dlg = wx.MessageDialog(self, 
        "Are you sure want to delete account "+ self.selectedAccount.accountName +"?",
        "Confirmation",  wx.YES_NO|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            self.user.removeAccount(self.selectedAccount)
            self.list_ctrl.DeleteItem(self.selectedIndex)
            self.mode = "new"
            self.clearEditAccount()
            self.list_ctrl.SetItemState(self.selectedIndex, 0, wx.LIST_STATE_SELECTED)

    def editAccount(self, event):
        self.formEditMode()
        self.mode = "edit"
        self.passTxt.SetValue("")

    def formEditMode(self):
        self.btnCancel.Show()
        self.btnCopy.Hide()
        self.btnEdit.Disable()
        self.btnNew.Disable()
        self.btnRemove.Disable()        
        self.btnSave.Show()
        self.repassTxt.SetEditable(True)
        self.passTxt.SetEditable(True)
        self.repassTxt.Show()
        self.repassLbl.Show()
        self.Layout()

    def listAccounts(self):
        index = 1
        for account in self.user.getAccountList(True):
            print(index)
            indexList = self.list_ctrl.InsertItem(index, account.accountName)
            self.list_ctrl.SetItem(indexList, 1, account.accountUsername)
            index += 1

    def makeMenuBar(self):
        #FILE MENU
        fileMenu = wx.Menu()
        changePassword = fileMenu.Append(-1, "&Change Password", "Change user password")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, "&About", "About Password Manager")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        #EVENTS
        self.Bind(wx.EVT_MENU, self.changePassword,  changePassword)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        
    def newAccount(self, event):
        self.clearFormAccount()
        self.accountTxt.SetEditable(True)
        self.usernameTxt.SetEditable(True)
        self.formEditMode()
        self.mode = "new"

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.4
        dlg = wx.MessageDialog( self, "A simple user account manager", "About Password Manager", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def onSelectAccount(self):
        self.btnCopy.Enable()
        self.btnEdit.Enable()
        self.btnRemove.Enable()

    def onSelected(self, event):
        accountNameLi = self.list_ctrl.GetItem(event.GetIndex(), 0)
        usernameLi = self.list_ctrl.GetItem(event.GetIndex(), 1)
        
        for account in self.user.getAccountList():
            if account.accountName == accountNameLi.GetText() and account.accountUsername == usernameLi.GetText():
                self.accountTxt.SetValue(account.accountName)
                self.usernameTxt.SetValue(account.accountUsername)
                self.passTxt.SetValue("XXXXXXXX")
                self.selectedAccount = account
                self.selectedIndex = event.GetIndex()
                self.onSelectAccount()
                break

    def saveAccount(self, event):
        if self.validate():
            if self.mode == "new" :
                msg = "Account has been added"
                newAccount = Account(self.accountTxt.GetValue())
                newAccount.setAccountUsername(self.usernameTxt.GetValue())
                if not self.user.isAccountExist(newAccount):
                    self.user.addAccount(newAccount, self.passTxt.GetValue())
                    indexItem = 1
                    if self.list_ctrl.GetItemCount() > 0:
                        indexItem = self.list_ctrl.GetItemCount() + 1
                    index = self.list_ctrl.InsertItem(indexItem, newAccount.accountName)
                    self.list_ctrl.SetItem(index, 1, newAccount.accountUsername)
                    self.showDialog(msg, "Information", wx.OK|wx.ICON_INFORMATION)
                else:
                    msg = "Account is already exist."
                    self.showDialog(msg, "Error", wx.OK|wx.ICON_ERROR)
            else:
                msg = "Account has been updated"
                self.user.addAccount(self.selectedAccount, self.passTxt.GetValue())
                self.showDialog(msg, "Information", wx.OK|wx.ICON_INFORMATION)
            self.clearEditAccount()

    def showDialog(self, msg, title, style):
        dlg = wx.MessageDialog(self, msg, title, style)
        dlg.ShowModal()
        dlg.Destroy()
        
    def sizeColumns(self, event=None):
        width = self.list_ctrl.GetSize()[0]
        numCols = self.list_ctrl.GetColumnCount()

        for i in range(numCols):
             self.list_ctrl.SetColumnWidth(i, width/numCols) #set your column width to whatever proportions you want

        if event:
            event.Skip() #since this is a wx.EVT_SIZE, this line is important
            
    def validate(self):
        msg = ""
        passValue = self.passTxt.GetValue()
        repassValue = self.repassTxt.GetValue()
        username = self.usernameTxt.GetValue()
        accountName = self.accountTxt.GetValue()
        if not accountName.strip():
            self.accountTxt.SetFocus()
            msg = "Please enter your account name"
        elif not username.strip():
            self.usernameTxt.SetFocus()
            msg = "Please enter your username"
        elif not passValue.strip():
            self.passTxt.SetFocus()
            msg = "Please enter your password"
        elif not repassValue.strip():
            self.repassTxt.SetFocus()
            msg = "Please re-enter your password"
        elif passValue != repassValue:
            self.passTxt.SetValue("")
            self.repassTxt.SetValue("")
            self.passTxt.SetFocus()
            msg = "Password must be matched"
        else:
            return True

        #display error message dialog
        if msg:
            self.showDialog(msg, "Validation Error", wx.OK | wx.ICON_ERROR)
            return False
        else:
            return True

