import wx
from app.model.user import User

class UserSetting(wx.Panel):
    def __init__(self, parent, user=None):
        wx.Panel.__init__(self, parent)

        self.user = user
        # and put some text with a larger bold font on it
        st = wx.StaticText(self, label="Password Manager", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        self.parent = parent
        loginLbl = wx.StaticText(self, label="Username:")      
        self.loginTxt = wx.TextCtrl(self, size=wx.Size(150, 20), style=wx.TE_PROCESS_ENTER)
        oldPassLbl = wx.StaticText(self, label="Old Password:")        
        self.oldPassTxt = wx.TextCtrl(self, size=wx.Size(150, 20), style=wx.TE_PASSWORD)
        passLbl = wx.StaticText(self, label="Password:")        
        self.passTxt = wx.TextCtrl(self, size=wx.Size(150, 20), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        repassLbl = wx.StaticText(self, label="Re-enter Password:")        
        self.repassTxt = wx.TextCtrl(self, size=wx.Size(150, 20), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        regBtn = wx.Button(self, wx.ID_OK, label="&Register")
        cancelBtn = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        
        #create a grid
        self.grid = wx.GridBagSizer(hgap=5, vgap=5)
        self.grid.Add(loginLbl, pos=(0,0))
        self.grid.Add(self.loginTxt, pos=(0,1))
        

        buttonLayout = wx.BoxSizer(wx.HORIZONTAL)
        buttonLayout.Add(cancelBtn, 0, wx.ALL, 10)
        buttonLayout.Add(regBtn, 0, wx.ALL, 10)

        if self.user == None:
            self.grid.Add(passLbl, pos=(1,0))
            self.grid.Add(self.passTxt, pos=(1,1))
            self.grid.Add(repassLbl, pos=(2,0))
            self.grid.Add(self.repassTxt, pos=(2,1))
            oldPassLbl.Hide()
            self.oldPassTxt.Hide()            
        else:
            self.grid.Add(oldPassLbl, pos=(1,0))
            self.grid.Add(self.oldPassTxt, pos=(1,1))
            self.grid.Add(passLbl, pos=(2,0))
            self.grid.Add(self.passTxt, pos=(2,1))
            self.grid.Add(repassLbl, pos=(3,0))
            self.grid.Add(self.repassTxt, pos=(3,1))
            self.loginTxt.SetEditable(False)
            self.loginTxt.SetValue(self.user.getUsername())
            regBtn.SetLabel("Con&firm")            

        #Binds
        self.loginTxt.Bind(wx.EVT_TEXT_ENTER, self.onClick)
        self.passTxt.Bind(wx.EVT_TEXT_ENTER, self.onClick)
        self.repassTxt.Bind(wx.EVT_TEXT_ENTER, self.onClick)
        regBtn.Bind(wx.EVT_BUTTON, self.onClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, 0, wx.CENTER)
        sizer.AddStretchSpacer()
        sizer.Add(self.grid, 1, wx.CENTER)
        sizer.Add(buttonLayout, 0, wx.CENTER, 10)
        sizer.AddStretchSpacer()

        #Layout sizers
        self.SetSizerAndFit(sizer)
        self.SetAutoLayout(1)        

    def onClick(self, event):
        if self.validate():
            user = User(self.loginTxt.GetValue())
            self.parent.CloseUserSetting("SUCCESS")

    def clear(self):
        self.oldPassTxt.SetValue("")
        self.passTxt.SetValue("")
        self.repassTxt.SetValue("")
        self.oldPassTxt.SetFocus()

    def onCancel(self, event):
        self.Hide()
        self.parent.CloseUserSetting("CANCEL")

    def validate(self):
        msg = ""
        passValue = self.passTxt.GetValue()
        repassValue = self.repassTxt.GetValue()
        username = self.loginTxt.GetValue()
        if not username.strip():
            self.loginTxt.SetFocus()
            msg = "Please enter your username"
        elif self.user != None and not self.oldPassTxt.GetValue().strip():
            self.oldPassTxt.SetFocus()
            msg = "Please enter your old password"
        elif not passValue.strip():
            self.passTxt.SetFocus()
            msg = "Please enter your password"
        elif not repassValue.strip():
            self.repassTxt.SetFocus()
            msg = "Please re-enter your password"
        elif passValue != repassValue:
            self.repassTxt.SetFocus()
            msg = "Password must be matched"
        else:
            mode = "edit"
            if self.user == None:
                mode = "new"
                self.user = User(username)
                
            if mode == "new" and self.user.isExisting():
                msg = "Username is already exist. Please choose other username or login if this is you."
            elif mode == "edit" and self.oldPassTxt.GetValue().strip() != self.user.getPassword():
                msg = "Your old password does not matched."
                self.clear()
            else:
                self.user.changePassword(passValue)
                if mode == "new":
                    msg = "User has been registered succesfully."
                else:
                    msg = "Password has been updated."
                dlg = wx.MessageDialog(self, msg, "Information", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return True

        #display error message dialog
        if msg:
            dlg = wx.MessageDialog(self, msg, "Validation Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        else:
            return True

