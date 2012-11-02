import wx
msgDlg = wx.MessageDialog (None, 'Mangez-vous beaucoup de pommes ?',
                           'Question 1', wx.YES_NO | wx.ICON_QUESTION)
reponse = msgDlg.ShowModal()
# traitement selon reponse ici...
# Destruction de la boite de dialogue
msgDlg.Destroy()

