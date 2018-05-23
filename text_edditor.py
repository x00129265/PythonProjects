#!/usr/bin/python
import wx
import wx.lib.dialogs
import wx.stc as stc
import os

faces = {
    'times': 'Times New Roman',
    'mono': 'Courier New',
    'helv': 'Arial',
    'other': 'Comic Sans MS',
    'size': 10,
    'size2': 8,
}

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        self.filename = ''
        self.leftMarginWidth = 25
        self.lineNumbersEnabled = True

        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        self.control.CmdKeyAssign(ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN) # Ctrl_+ to zoom in
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT) # Ctrl_- to zoom out

        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))



        fileMenu = wx.Menu()
        menuNew = fileMenu.Append(wx.ID_NEW, "&New\tCtrl+n", " Create a new document")
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open\tCtrl+o", " Open an existing document")
        menuSave = fileMenu.Append(wx.ID_SAVE, "&Save\tCtrl+s", " Save the current document")
        menuSaveAs = fileMenu.Append(wx.ID_SAVEAS, "Save &As\tAlt+a", " Save a new document")
        fileMenu.AppendSeparator()
        menuClose = fileMenu.Append(wx.ID_EXIT, "&Close\tCtrl+w", " Close the application")

        editMenu = wx.Menu()
        menuUndo = editMenu.Append(wx.ID_UNDO, "&Undo\tCtrl+z", " Undo last action")
        menuRedo = editMenu.Append(wx.ID_REDO, "&REDO\tCtrl+r", " Redo last action")
        editMenu.AppendSeparator()
        menuSelectAll = editMenu.Append(wx.ID_SELECTALL, "&Select All\tCtrl+a", " Select All")
        menuCopy = editMenu.Append(wx.ID_COPY, "&Copy\tCtrl+c", " Copy selected text")
        menuCut = editMenu.Append(wx.ID_CUT, "C&ut\tCtrl+x", " Cut selected text")
        menuPaste = editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+p", " Paste text")

        prefMenu = wx.Menu()
        menuLineNumbers = prefMenu.Append(wx.ID_ANY, "Toggle &Line numbers\tCtrl+t", " Show/Hide line numbers column")

        helpMenu = wx.Menu()
        menuHowTo = helpMenu.Append(wx.ID_ANY, "&How To...\tF1", " Get Help using the editor")
        helpMenu.AppendSeparator()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About\tF2", " Read about the editor and its making")

        # Bar menu
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(editMenu, "&Edit")
        menuBar.Append(prefMenu, "&Preferences")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)


        # Binds
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)

        self.Bind(wx.EVT_MENU, self.OnToogleLineNumber, menuLineNumbers)

        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)


        self.Show()
        self.UpdateLineCol(self)

    """Bar manu methods"""
    def OnNew(self, e):
        self.filename = ''
        self.control.SetValue("")

    def OnOpen(self, e):
        try:
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.control.SetValue(f.read())
                f.close()
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Couldn't open the file", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
            f.close()
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
            except:
                pass

    def OnSaveAs(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()
        except:
            pass

    def OnClose(self, e):
        self.Close(True)

    def OnUndo(self, e):
        self.control.Undo()

    def OnRedo(self, e):
        self.control.Redo()

    def OnSelectAll(self, e):
        self.control.SelectAll()

    def OnCopy(self, e):
        self.control.Copy()

    def OnCut(self, e):
        self.control.Cut()

    def OnPaste(self, e):
        self.control.Paste()

    def OnToogleLineNumber(self, e):
        if (self.lineNumbersEnabled):
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnabled = True

    def OnHowTo(self, e):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, "This is how to.", "How To", size=(400, 400))
        dlg.ShowModal()
        dlg.Destroy()

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "My advanced text edditor","About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    """end Bar manu"""

    def UpdateLineCol(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Line %s, Column %s" % (line, col)
        self.StatusBar.SetStatusText(stat, 0)

    # def OnCharEvent(self, e):
        # keyCode = e.GetKeyCode()
        # print(keyCode)
        # if keyCode == 14:


if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow(None, "Text Editor")
    app.MainLoop()