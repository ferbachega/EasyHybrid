# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Fri May 12 15:57:36 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
 

import sys

#from PySide.QtGui import *
#from PySide.QtCore import *

from PySide import QtCore, QtGui

from GUI.untitled      import Ui_MainWindow

from GLarea.easyMolObj import EasyMolSession
from GLarea.GLWidget   import GLWidget



class EasyMolFunctions:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    

    
    def delete_obj (self, index = 0):
        """ Function doc """
        self.EasyMol.delete(self.current_row)
        self.update_list_view()
    
    
    def center_obj (self, index = 0):
        """ Function doc """
        self.EasyMol.center(self.current_row)
        #self.update_list_view()

    """   L I N E S   """

    def show_lines      (self, Vobject_index = None):
        """ show """
        
        if Vobject_index == None:
            Vobject_index = self.current_row
        
        self.EasyMol.show (_type = 'lines', Vobject_index = Vobject_index)  
    
    def hide_lines      (self, Vobject_index = None):
        """ hide """
        
        if Vobject_index == None:
            Vobject_index = self.current_row
        
        self.EasyMol.hide (_type = 'lines', Vobject_index = Vobject_index)  

    
    
    
    """   R I B B O N S   """

    def show_ribbons (self, Vobject_index = None):
        """ show """
        
        if Vobject_index == None:
            Vobject_index = self.current_row
        
        self.EasyMol.show (_type = 'ribbons', Vobject_index = Vobject_index)  

    
    def hide_ribbons (self, Vobject_index = None):
        """ hide """
        
        if Vobject_index == None:
            Vobject_index = self.current_row
        
        self.EasyMol.hide (_type = 'ribbons', Vobject_index = Vobject_index)  


    """   B A L L  A N D  S T I C K   """


    def show_ball_and_stick (self, Vobject_index = None):
        """ show """
        #print ('here  show_ball_and_stick - gui')

        if Vobject_index == None:
            Vobject_index = self.current_row
        
        self.EasyMol.show (_type = 'ball_and_stick', Vobject_index = Vobject_index)  
    
    def hide_ball_and_stick2 (self, Vobject_index = None):
        """ hide """
        print ('here  hide_ball_and_stick - gui')
        if Vobject_index == None:
            Vobject_index = self.current_row
        self.EasyMol.hide (_type = 'ball_and_stick', Vobject_index = Vobject_index)  
        

    """   S P H E R E S   """

        
    def show_spheres (self, Vobject_index = None):
        """ show """
        #print ('here  show_ball_and_stick - gui')

        if Vobject_index == None:
            Vobject_index = self.current_row
        
        self.EasyMol.show (_type = 'spheres', Vobject_index = Vobject_index)

    
    #def hide_spheres (self, Vobject_index = None):
    #    """ hide """
    #    print ('here  spheres - gui')
    #    
    #    if Vobject_index == None:
    #        Vobject_index = self.current_row
    #    self.EasyMol.hide (_type = 'spheres', Vobject_index = Vobject_index)  

    def hide_spheres2 (self, Vobject_index = None):
        """ hide """
        print ('here  spheres - gui')
        
        if Vobject_index == None:
            Vobject_index = self.current_row
        self.EasyMol.hide (_type = 'spheres', Vobject_index = Vobject_index)






    def show_sticks         (self):
        """ Function doc """


    def show_surface        (self):
        """ Function doc """


    def hide_sticks         (self):
        """ Function doc """

    def hide_surface        (self):
        """ Function doc """





class MainWindow(QtGui.QMainWindow, Ui_MainWindow, EasyMolFunctions):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setupUi(self)
        
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.open_treeview_menu)
        #self.treeWidget.clicked.connect(self.on_treeView_clicked)
        #QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("on_treeview_item_clicked(QtreeWidgetItem*)"), self.on_treeView_item_clicked)
        #QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("clicked(QModelIndex)"),          self.on_treeview_clicked_QModelIndex)
        #QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("on_treeview_item_clicked(QtreeWidgetItem*)"), self.on_treeView_item_clicked)
        QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("on_treeview_item_clicked(QTreeWidgetItem*,int)"), self.on_treeview_item_clicked)
        self.generate_actions ()
        

        self.toolBar_2.addSeparator()
        self.label2 = QtGui.QLabel()
        self.toolBar_2.addWidget(self.label2)
        self.label2.setObjectName("  Selecting:  ")
        self.label2.setText(QtGui.QApplication.translate("MainWindow", "Selecting", None, QtGui.QApplication.UnicodeUTF8))
        
        self.toolBar_2.addSeparator()
        self.selection_mode_combo=QtGui.QComboBox()
        self.toolBar_2.addWidget(self.selection_mode_combo)
        self.selection_mode_combo.insertItems(1,["atom","residue","chain","molecule"])
        QtCore.QObject.connect(self.selection_mode_combo, QtCore.SIGNAL("activated(QString)"), self.change_selection_mode)



        
        glmenu = [self.actionOpen]
        self.current_row = None     # selected row from the treeview menu

        self.glwidget = GLWidget(self, glmenu = glmenu)

        
        QtCore.QObject.connect(self.toolBar_2, QtCore.SIGNAL("toggled(bool)"), self.change_viewing_and_picking_mode)
        #self.toolBar_2.addAction(self.actionViewing)

        self.EasyMol  = EasyMolSession(glwidget =  self.glwidget)

        self.setCentralWidget(self.glwidget)
        self.show()
    

    def generate_actions (self):
        """ Function doc """
        
        #New_Project = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("NewProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew_Project.setIcon(icon7)
        #self.actionNew_Project.setObjectName("actionNew_Project")
        
        #Open
        self.actionOpen.triggered.connect(self.showDialog)
        
        '''    Change - viewing and picking mode    '''
        self.actionViewing.triggered.connect(self.change_viewing_and_picking_mode)

        
        '''    Center    '''
        #Delete
        self.Action_center = QtGui.QAction('Center', self)
        self.Action_center.setStatusTip('Center on Object')
        self.Action_center.triggered.connect(self.center_obj)
        
        
        
        '''    Delete    '''
        #Delete
        self.Action_delete = QtGui.QAction('Delete', self)
        self.Action_delete.setStatusTip('Delete Object')
        self.Action_delete.triggered.connect(self.delete_obj)

        
        '''    Lines    '''
        # show
        self.Action_show_lines = QtGui.QAction('Lines', self)
        self.Action_show_lines.setStatusTip('Show lines')
        self.Action_show_lines.triggered.connect(self.show_lines)
        # hide
        self.Action_hide_lines = QtGui.QAction('Lines', self)
        self.Action_hide_lines.setStatusTip('Show lines')
        self.Action_hide_lines.triggered.connect(self.hide_lines)

        
        '''   Ribbons   '''
        # show
        self.Action_show_ribbons = QtGui.QAction('Ribbons', self)
        self.Action_show_ribbons.setStatusTip('Show Ribbons')
        self.Action_show_ribbons.triggered.connect(self.show_ribbons)
        # hide
        self.Action_hide_ribbons = QtGui.QAction('Ribbons', self)
        self.Action_hide_ribbons.setStatusTip('Hide Ribbons')
        self.Action_hide_ribbons.triggered.connect(self.hide_ribbons)
        

        '''   Ball and Stick   '''
        # show
        self.Action_show_ball_and_stick = QtGui.QAction('Ball and Stick', self)
        self.Action_show_ball_and_stick.setStatusTip('Show Ball and Stick')
        self.Action_show_ball_and_stick.triggered.connect(self.show_ball_and_stick)
        # hide
        self.Action_hide_ball_and_stick = QtGui.QAction('Ball and Stick', self)
        self.Action_hide_ball_and_stick.setStatusTip('Hide Ball and Stick')
        self.Action_hide_ball_and_stick.triggered.connect(self.hide_ball_and_stick2)
        
        '''   Spheres   '''
        # show
        self.Action_show_spheres = QtGui.QAction('Spheres', self)
        self.Action_show_spheres.setStatusTip('Show Spheres')
        self.Action_show_spheres.triggered.connect(self.show_spheres)
        # hide          
        self.Action_hide_spheres = QtGui.QAction('Spheres', self)
        self.Action_hide_spheres.setStatusTip('Hide Spheres')
        self.Action_hide_spheres.triggered.connect(self.hide_spheres2)
        
        
        '''
        #Stick
        self.Action_show_stick = QtGui.QAction('Stick', self)
        self.Action_show_stick.setStatusTip('Show Stick')
        self.Action_show_stick.triggered.connect(self.show_sticks)
        
        #Spheres
        self.Action_show_spheres = QtGui.QAction('Spheres', self)
        self.Action_show_spheres.setStatusTip('Show Spheres')
        self.Action_show_spheres.triggered.connect(self.show_spheres)
        



        #Surface
        self.Action_show_surface = QtGui.QAction('Surface', self)
        self.Action_show_surface.setStatusTip('Show Surface')
        self.Action_show_surface.triggered.connect(self.show_surface)

        '''
        #exite
        self.Action_exite = QtGui.QAction('Exit', self)
        self.Action_exite.setShortcut('Ctrl+Q')
        self.Action_exite.setStatusTip('Exit application')
        self.Action_exite.triggered.connect(self.close)


    def on_treeview_clicked_QModelIndex(self, model):
        """ Function doc """
        print (model)
   

    def on_treeview_item_clicked (self, item, Int):
        #print (item, Int)
        #print (item.text(0),item.text(1))
        
        state = item.checkState(0)
        #print ('state: ',state)
        object_id = int(item.text(1))
        #print (object_id)
        if state == QtCore.Qt.CheckState.Unchecked:
            #setCheckState(int column, Qt::CheckState state)
            item.setCheckState(0, QtCore.Qt.CheckState.Checked)
            self.EasyMol.enable(int(object_id))
            #print (self.EasyMol.Vobjects[object_id].actived)
            
        if state == QtCore.Qt.CheckState.Checked:
            item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
            self.EasyMol.disable(int(object_id))
        
    
    def change_viewing_and_picking_mode (self):
        """ Function doc """
        if self.actionViewing.isChecked() :
            self.glwidget.setCursor(QtCore.Qt.CrossCursor)
            self.selection_mode_combo.setEnabled(False)
            self.actionViewing.setText("Picking")
            self.EasyMol._picking_selection_mode = True 
        else:
            self.glwidget.setCursor(QtCore.Qt.ArrowCursor)
            self.selection_mode_combo.setEnabled(True)
            self.actionViewing.setText("Viewing")
            self.EasyMol._picking_selection_mode = False 
        self.glwidget.updateGL()
    
    def change_selection_mode(self, selection_mode):
        """ Function doc """
        #print (selection_mode)
        self.EasyMol.selection_mode(selection_mode)

        
    def setup_icons (self):
        """ Function doc """
        icon6 = QIcon()
        icon6.addPixmap(QPixmap("/home/fernando/programs/EasyHybrid/easyhybrid/QtEasyMol/GUI/NewProject.png"), QIcon.Normal, QIcon.Off)
        self.actionNew_Project.setIcon(icon6)
        

    def showDialog(self):
        '''
        dir = self.sourceDir
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"
        options = "" # ???
        fileObj = QFileDialog.getOpenFileName(self, " File dialog ", dir, filters, selected_filter, options)
        '''
        
        filters = "PDB files (*.pdb);;XYZ (*.xyz);;All (*)"
        #selected_filter = "Images (*.png *.xpm *.jpg)"
        options = "" # ???
        
        dialog = QtGui.QFileDialog()
        fname, _ = dialog.getOpenFileName(self, 'Open file','/home', filters, options)
        
        if self.EasyMol.load(fname):
            self.update_list_view()
        else:
            pass


    def update_list_view (self):
        """ Function doc """
        Vobjects_list = self.EasyMol.get_vobject_list()
        self.treeWidget.clear()

        for key in Vobjects_list:
            item = QtGui.QTreeWidgetItem(self.treeWidget)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            
            if self.EasyMol.Vobjects[int(key)].actived:
                item.setCheckState(0, QtCore.Qt.Checked)           
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)           
            
            item.setText(1, QtGui.QApplication.translate("MainWindow", str(key)          , None, QtGui.QApplication.UnicodeUTF8))
            item.setText(2, QtGui.QApplication.translate("MainWindow", Vobjects_list[key], None, QtGui.QApplication.UnicodeUTF8))
            item.setText(3, QtGui.QApplication.translate("MainWindow", "12"              , None, QtGui.QApplication.UnicodeUTF8))
            item.setText(4, QtGui.QApplication.translate("MainWindow", "123"             , None, QtGui.QApplication.UnicodeUTF8))
            item.setText(5, QtGui.QApplication.translate("MainWindow", "no"              , None, QtGui.QApplication.UnicodeUTF8))            

        
    def open_treeview_menu(self, position):
        #print ('menu')
        
        
        
        indexes = self.treeWidget.selectedIndexes()
        
        #print (position)
        #index = indexes[0]
        #for index in indexes:
        #    print ('index.parent().isValid()', index.parent().isValid())
        #    print ('index.parent()'          , index.parent())
        #    print ('index '                  , index )
        #    print ('index.row() '                  , index.row() )

            
            #print (indexes[0].model ())
        index =  indexes[0]
        self.current_row = index.row()
        
        if len(indexes) > 0:
        
             level = 0
             index = indexes[0]
             while index.parent().isValid():
                 index = index.parent()
                 
                 #print (index.checkState())
                 level += 1
         
        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(self.Action_center)
            
            menu_show = menu.addMenu("&Show")
            menu_show.addAction(self.Action_show_lines)
            menu_show.addAction(self.Action_show_ribbons)
            menu_show.addAction(self.Action_show_ball_and_stick)
            menu_show.addAction(self.Action_show_spheres)

            menu_hide = menu.addMenu("&Hide")
            menu_hide.addAction(self.Action_hide_lines)
            menu_hide.addAction(self.Action_hide_ribbons)
            menu_hide.addAction(self.Action_hide_ball_and_stick)
            menu_hide.addAction(self.Action_hide_spheres)

            menu.addSeparator()
            menu.addAction(self.Action_delete)

        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
        self.current_row =  None


'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
'''
