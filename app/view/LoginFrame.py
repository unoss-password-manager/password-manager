#!python
import wx
from app.view.UserSetting import UserSetting
from app.model.user import User
from app.view.MenuFrame import MainWindow


class loginWindow(wx.Frame):
   
    def __init__(self, *args, **kw):
        # set no resize style
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                                wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, style=no_resize)

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        #create a grid
        self.grid = wx.GridBagSizer(hgap=5, vgap=5)

        # and put some text with a larger bold font on it
        st = wx.StaticText(self.pnl, label="Password Manager", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        loginLbl = wx.StaticText(self.pnl, label="Username:")      
        self.loginTxt = wx.TextCtrl(self.pnl, size=wx.Size(150, 20), style=wx.TE_PROCESS_ENTER)
        passLbl = wx.StaticText(self.pnl, label="Password:")        
        self.passTxt = wx.TextCtrl(self.pnl, size=wx.Size(150, 20), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        btnLogin = wx.Button(self.pnl, label="&Login")
        btnNewUser = wx.Button(self.pnl, label="&New User")
        
        self.grid.Add(loginLbl, pos=(0,0))
        self.grid.Add(self.loginTxt, pos=(0,1))
        self.grid.Add(passLbl, pos=(1,0))
        self.grid.Add(self.passTxt, pos=(1,1))

        buttonLayout = wx.BoxSizer(wx.HORIZONTAL)
        buttonLayout.Add(btnNewUser, 0, wx.ALL, 10)
        buttonLayout.Add(btnLogin, 0, wx.ALL, 10)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Login or register to manage password")

        self.sizer = wx.BoxSizer(wx.VERTICAL)        
        self.sizer.Add(st, 0, wx.CENTER)
        self.sizer.AddStretchSpacer()
        self.sizer.Add(self.grid, 1, wx.CENTER)
        self.sizer.Add(buttonLayout, 0, wx.CENTER)
        self.sizer.AddStretchSpacer()

        #Binds
        self.loginTxt.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        self.passTxt.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        btnNewUser.Bind(wx.EVT_BUTTON, self.onRegister)
        btnLogin.Bind(wx.EVT_BUTTON, self.onLogin)

        self.registerPanel = UserSetting(self)

        sizerBox = wx.BoxSizer()
        sizerBox.Add(self.pnl, 1, wx.EXPAND)
        sizerBox.Add(self.registerPanel, 1, wx.EXPAND)
        self.registerPanel.Hide()

        #set icon
        ico = wx.Icon('pw.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        
        #Layout sizers
        self.pnl.SetSizer(self.sizer)
        self.pnl.SetAutoLayout(1)
        self.sizer.Fit(self.pnl)
        self.SetSizeHints(250,300,500,400)
        self.SetSizer(sizerBox)

    def onRegister(self, event):
        #show register panel
        self.pnl.Hide()
        self.registerPanel.Show()
        self.Layout()

    def CloseUserSetting(self, returnCode):
        self.pnl.Show()
        self.registerPanel.Hide()
        self.Layout()

    def onLogin(self, event):
        #validate
        if self.validate():
            frm = MainWindow(self.user, None, title='Password Keeper')
            frm.Show()
            frm.Maximize(True)
            self.Close()

    def validate(self):
        msg = ""
        username = self.loginTxt.GetValue()
        passwd = self.passTxt.GetValue()
        username = self.loginTxt.GetValue()
        if not username.strip():
            self.loginTxt.SetFocus()
            msg = "Please enter your username"
        elif not passwd.strip():
            self.passTxt.SetFocus()
            msg = "Please enter your password"
        else:
            self.user = User(username)
            if not self.user.matchPassword(passwd):
                msg = "Username and password does not matched."
                self.passTxt.SetValue("")
                self.passTxt.SetFocus()

        #display error message dialog
        if msg:
            dlg = wx.MessageDialog(self, msg, "Validation Error", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        else:
            return True
