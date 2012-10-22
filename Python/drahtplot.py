#!/usr/bin/env python
import wx
import wx.lib.plot as plot
import threading,sys
import thread

# Needs Numeric or numarray or NumPy
try:
    import numpy.oldnumeric as _Numeric
except:
    try:
        import numarray as _Numeric  #if numarray is used it is renamed Numeric
    except:
        try:
            import Numeric as _Numeric
        except:
            msg= """
            This module requires the Numeric/numarray or NumPy module,
            which could not be imported.  That one, probably, is not installed
            (it's not part of the standard Python distribution). See the
            Numeric Python site (http://numpy.scipy.org) for information on
            downloading source or binaries."""
            raise ImportError, "Numeric,numarray or NumPy not found. \n" + msg
"""
 used for interactive plot
"""
class TestFrame(wx.Frame):
    """
 used for interactive plot, creation 16/06/08
 La calomnie irrite les hommes et ne les corrige pas
    """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, (600, 400))

        # Now Create the menu bar and items
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(200, 'Page Setup...', 'Setup the printer page')
        self.Bind(wx.EVT_MENU, self.OnFilePageSetup, id=200)
        
        menu.Append(201, 'Print Preview...', 'Show the current plot on page')
        self.Bind(wx.EVT_MENU, self.OnFilePrintPreview, id=201)
        
        menu.Append(202, 'Print...', 'Print the current plot')
        self.Bind(wx.EVT_MENU, self.OnFilePrint, id=202)
        
        menu.Append(203, 'Save Plot...', 'Save current plot')
        self.Bind(wx.EVT_MENU, self.OnSaveFile, id=203)
        
        menu.Append(205, 'E&xit', 'Enough of this already!')
        self.Bind(wx.EVT_MENU, self.OnFileExit, id=205)
        self.mainmenu.Append(menu, '&File')

        menu = wx.Menu()
	
        menu.Append(211, '&Redraw', 'Redraw plots')
        self.Bind(wx.EVT_MENU,self.OnPlotRedraw, id=211)
        menu.Append(212, '&Clear', 'Clear canvas')
        self.Bind(wx.EVT_MENU,self.OnPlotClear, id=212)
        menu.Append(213, '&Scale', 'Scale canvas')
        self.Bind(wx.EVT_MENU,self.OnPlotScale, id=213) 
        menu.Append(214, 'Enable &Zoom', 'Enable Mouse Zoom', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.OnEnableZoom, id=214) 
        menu.Append(215, 'Enable &Grid', 'Turn on Grid', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.OnEnableGrid, id=215)
        menu.Append(217, 'Enable &Drag', 'Activates dragging mode', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.OnEnableDrag, id=217)
        menu.Append(220, 'Enable &Legend', 'Turn on Legend', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.OnEnableLegend, id=220)
        menu.Append(222, 'Enable &Point Label', 'Show Closest Point', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.OnEnablePointLabel, id=222)
       
        menu.Append(225, 'Scroll Up 1', 'Move View Up 1 Unit')
        self.Bind(wx.EVT_MENU,self.OnScrUp, id=225) 
        menu.Append(230, 'Scroll Rt 2', 'Move View Right 2 Units')
        self.Bind(wx.EVT_MENU,self.OnScrRt, id=230)
        menu.Append(235, '&Plot Reset', 'Reset to original plot')
        self.Bind(wx.EVT_MENU,self.OnReset, id=235)

        self.mainmenu.Append(menu, '&Parameters')

        menu = wx.Menu()
        menu.Append(300, '&About', 'About this thing...')
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=300)
        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

        # A status bar to tell people what's happening
        self.CreateStatusBar(1)
        
        self.client = plot.PlotCanvas(self)
        #define the function for drawing pointLabels
        self.client.SetPointLabelFunc(self.DrawPointLabel)
        # Create mouse event for showing cursor coords in status bar
        self.client.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        # Show closest point when enabled
        self.client.canvas.Bind(wx.EVT_MOTION, self.OnMotion)

        self.Show(True)

    def DrawPointLabel(self, dc, mDataDict):
        """This is the fuction that defines how the pointLabels are plotted
            dc - DC that will be passed
            mDataDict - Dictionary of data that you want to use for the pointLabel

            As an example I have decided I want a box at the curve point
            with some text information about the curve plotted below.
            Any wxDC method can be used.
        """
        # ----------
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush( wx.BLACK, wx.SOLID ) )
        
        sx, sy = mDataDict["scaledXY"] #scaled x,y of closest point
        dc.DrawRectangle( sx-5,sy-5, 10, 10)  #10by10 square centered on point
        px,py = mDataDict["pointXY"]
        cNum = mDataDict["curveNum"]
        pntIn = mDataDict["pIndex"]
        legend = mDataDict["legend"]
        #make a string to display
        s = "Crv# %i, '%s', Pt. (%.2f,%.2f), PtInd %i" %(cNum, legend, px, py, pntIn)
        dc.DrawText(s, sx , sy+1)
        # -----------

    def OnMouseLeftDown(self,event):
        s= "Left Mouse Down at Point: (%.4f, %.4f)" % self.client._getXY(event)
        self.SetStatusText(s)
        event.Skip()            #allows plotCanvas OnMouseLeftDown to be called

    def OnMotion(self, event):
        #show closest point (when enbled)
        if self.client.GetEnablePointLabel() == True:
            #make up dict with info for the pointLabel
            #I've decided to mark the closest point on the closest curve
            dlst= self.client.GetClosestPoint( self.client._getXY(event), pointScaled= True)
            if dlst != []:    #returns [] if none
                curveNum, legend, pIndex, pointXY, scaledXY, distance = dlst
                #make up dictionary to pass to my user function (see DrawPointLabel) 
                mDataDict= {"curveNum":curveNum, "legend":legend, "pIndex":pIndex,\
                            "pointXY":pointXY, "scaledXY":scaledXY}
                #pass dict to update the pointLabel
                self.client.UpdatePointLabel(mDataDict)
        event.Skip()           #go to next handler

    def OnFilePageSetup(self, event):
        self.client.PageSetup()
        
    def OnFilePrintPreview(self, event):
        self.client.PrintPreview()
        
    def OnFilePrint(self, event):
        self.client.Printout()
        
    def OnSaveFile(self, event):
        self.client.SaveFile()

    def OnFileExit(self, event):
        self.Close()

    def OnPlotDraw(self, event):
        #log scale example
        self.resetDefaults()
        self.client.setLogScale((True,True))
        self.client.Draw(_drawObjects())

    def OnPlotRedraw(self,event):
        self.client.Redraw()

    def OnPlotClear(self,event):
        self.client.Clear()
        
    def OnPlotScale(self, event):
        if self.client.last_draw != None:
            graphics, xAxis, yAxis= self.client.last_draw
            self.client.Draw(graphics,(1,3.05),(0,1))

    def OnEnableZoom(self, event):
        self.client.SetEnableZoom(event.IsChecked())
        self.mainmenu.Check(217, not event.IsChecked())
        
    def OnEnableGrid(self, event):
        self.client.SetEnableGrid(event.IsChecked())
        
    def OnEnableDrag(self, event):
        self.client.SetEnableDrag(event.IsChecked())
        self.mainmenu.Check(214, not event.IsChecked())
        
    def OnEnableLegend(self, event):
        self.client.SetEnableLegend(event.IsChecked())

    def OnEnablePointLabel(self, event):
        self.client.SetEnablePointLabel(event.IsChecked())

    def OnScrUp(self, event):
        self.client.ScrollUp(1)
        
    def OnScrRt(self,event):
        self.client.ScrollRight(2)

    def OnReset(self,event):
        self.client.Reset()

    def OnHelpAbout(self, event):
        from wx.lib.dialogs import ScrolledMessageDialog
        print "import is ok "
        about = ScrolledMessageDialog(self,self.__doc__, "About...")
        print " about creation is ok "
        about.ShowModal()

    def resetDefaults(self):
        """Just to reset the fonts back to the PlotCanvas defaults"""
        self.client.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL))
        self.client.SetFontSizeAxis(10)
        self.client.SetFontSizeLegend(7)
        self.client.setLogScale((False,False))
        self.client.SetXSpec('auto')
        self.client.SetYSpec('auto')

class Plot(wx.Dialog):
        """
        plot
        """
        def __init__(self, parent, id, title):
                wx.Dialog.__init__(self, parent, id, title, size=(180, 280))

                self.data = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]
                btn1 = wx.Button(self,  1, 'scatter', (50,50))
                btn2 = wx.Button(self,  2, 'line', (50,90))
                btn3 = wx.Button(self,  3, 'bar', (50,130))
                btn4 = wx.Button(self,  4, 'quit', (50,170))
                wx.EVT_BUTTON(self, 1, self.OnScatter)
                wx.EVT_BUTTON(self, 2, self.OnLine2)
                wx.EVT_BUTTON(self, 3, self.OnBar)
                wx.EVT_BUTTON(self, 4, self.OnQuit)
                wx.EVT_CLOSE(self, self.OnQuit)

        def OnScatter(self, event):
                frm = wx.Frame(self, -1, 'scatter', size=(600,450))
                client = plot.PlotCanvas(frm)
                markers = plot.PolyMarker(self.data, legend='', colour='pink', marker='triangle_down', size=1)
                gc = plot.PlotGraphics([markers], 'Scatter Graph', 'X Axis', 'Y Axis')
                client.Draw(gc, xAxis=(0,15), yAxis=(0,15))
                frm.Show(True)

        def OnLine(self, event):
                frm = wx.Frame(self, -1, 'line', size=(600,450))
                client = plot.PlotCanvas(frm)
                line = plot.PolyLine(self.data, legend='', colour='pink', width=5, style=wx.DOT)
                gc = plot.PlotGraphics([line], 'Line Graph', 'X Axis', 'Y Axis')
                client.Draw(gc,  xAxis= (0,15), yAxis= (0,15))
                frm.Show(True)

        def OnLine2(self, event):
        	toto = TestFrame(None, -1, "Gnade")
                line = plot.PolyLine(self.data, legend='', colour='pink', width=5, style=wx.DOT)
                gc = plot.PlotGraphics([line], 'Line Graph', 'X Axis', 'Y Axis')
                toto.client.Draw(gc,  xAxis= (0,15), yAxis= (0,15))
                toto.Show(True)

        def OnBar(self, event):
                frm = wx.Frame(self, -1, 'bar', size=(600,450))
                client = plot.PlotCanvas(frm)
                bar1 = plot.PolyLine([(1, 0), (1,5)], legend='', colour='gray', width=25)
                bar2 = plot.PolyLine([(3, 0), (3,8)], legend='', colour='gray', width=25)
                bar3 = plot.PolyLine([(5, 0), (5,12)], legend='', colour='gray', width=25)
                bar4 = plot.PolyLine([(6, 0), (6,2)], legend='', colour='gray', width=25)
                gc = plot.PlotGraphics([bar1, bar2, bar3, bar4],'Bar Graph', 'X Axis', 'Y Axis')
                client.Draw(gc, xAxis=(0,15), yAxis=(0,15))
                frm.Show(True)

        def OnQuit(self, event):
                self.Destroy()

class MyApp(wx.App):
       """
       essai
       """
       def OnInit(self):
                 dlg = Plot(None, -1, 'plot.py')
                 dlg.Show(True)
                 dlg.Centre()
                 return True

class IGPlot:
    def __init__(self):
        self.tPlot = threading.Thread(target = self.plot,args=())
	self.tPlot.setName("Gnade")
	self.title = "default: interactive plot"
        return None

    def run(self):
        return None
	
    def setData(self,data):
        self.data = data
        return None
	
    def setTitle(self,title):
        self.title = title
        return None
	
    def start(self):
        print " Draht start "
        self.tPlot.start()
	return None     
	
    def stop(self):
        print " Draht stop "
        self.toto0.toto.Close()
        self.tPlot._Thread__stop()
        del(self.toto0)
	return None
    def plot(self):
	self.toto0 = wx.App()
#	data = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]
        print "we are in plot "*30
	self.toto0.toto = TestFrame(None, -1, "Gnade")
	line = plot.PolyLine(self.data, legend='', colour='pink', width=5, style=wx.DOT)
	gc = plot.PlotGraphics([line], self.title, 'X Axis', 'Y Axis')
	self.toto0.toto.client.Draw(gc,  xAxis= (0,1), yAxis= (0,15))
	#self.toto0.toto.Show(True)
	print "self.toto0.MainLoop()"
	self.toto0.MainLoop()
	print "after self.toto0.MainLoop()"
	return None

    def plot1(self):
	line = plot.PolyLine(self.data, legend='', colour='pink', width=5, style=wx.DOT)
	gc = plot.PlotGraphics([line], self.title, 'X Axis', 'Y Axis')
	self.toto0.toto.resetDefaults()
	self.toto0.toto.client.Draw(gc,  xAxis= (0,20), yAxis= (0,20))
	self.toto0.toto.client.Redraw()
	#self.toto0.MainLoop()
    
        return None
        
    def exit(self):
        self.toto0.ExitMainLoop()
        
        
    def isAlive(self):
        return self.tPlot.isAlive()       
     

