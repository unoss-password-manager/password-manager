import wx
from app.view.LoginFrame import loginWindow

def OnClose(event):
    frm.Destroy()

if __name__ == "__main__":
    app = wx.App()
    frm = loginWindow(None, title='Password Keeper')
    frm.Show()
    app.MainLoop()
