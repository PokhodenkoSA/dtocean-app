# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:16:37 2017

@author: mtopper
"""

import os

from PyQt4 import QtCore, QtGui

from dtocean_app.main import DTOceanWindow, Shell
from dtocean_app.pipeline import InputVarItem
from dtocean_app.widgets.input import ListSelect


def test_open_dtocean_window(qtbot, mock):
        
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mock.patch.object(QtGui.QMessageBox,
                      'question',
                      return_value=QtGui.QMessageBox.Yes)
    
    assert window.windowTitle() == "DTOcean"


def test_new_project(qtbot, mock):
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mock.patch.object(QtGui.QMessageBox,
                      'question',
                      return_value=QtGui.QMessageBox.Yes)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    assert test_var._id == "device.system_type"


def test_set_device_type(qtbot, mock):
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mock.patch.object(QtGui.QMessageBox,
                      'question',
                      return_value=QtGui.QMessageBox.Yes)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
    
    assert tree_widget.currentItem() == test_var
    assert window._data_context._bottom_contents is not None
    assert isinstance(window._data_context._bottom_contents, ListSelect)
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status(): assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    assert True


def test_initiate_pipeline(qtbot, mock):
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mock.patch.object(QtGui.QMessageBox,
                      'question',
                      return_value=QtGui.QMessageBox.Yes)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status(): assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    assert True


def test_export_data(qtbot, mock, tmpdir):

    # File path
    datastate_file_name = "my_datastate.dts"
    datastate_file_path = os.path.join(str(tmpdir), datastate_file_name)
    
    mock.patch.object(QtGui.QMessageBox,
                      'question',
                      return_value=QtGui.QMessageBox.Yes)
                      
    mock.patch.object(QtGui.QFileDialog,
                      'getSaveFileName',
                      return_value=datastate_file_path)
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status(): assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Export data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionExport")
        
    assert os.path.isfile(datastate_file_path)
    
    
def test_import_data(qtbot, mock, tmpdir):

    # File path
    datastate_file_name = "my_datastate.dts"
    datastate_file_path = os.path.join(str(tmpdir), datastate_file_name)
    
    mock.patch.object(QtGui.QMessageBox,
                      'question',
                      return_value=QtGui.QMessageBox.Yes)
                      
    mock.patch.object(QtGui.QFileDialog,
                      'getSaveFileName',
                      return_value=datastate_file_path)
                      
    mock.patch.object(QtGui.QFileDialog,
                      'getOpenFileName',
                      return_value=datastate_file_path)
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        check_var = window._pipeline_dock._find_item("Device Technology Type",
                                                     InputVarItem)
        assert check_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Export data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionExport")
        
    assert os.path.isfile(datastate_file_path)
    
    # Open a new project
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    # Import data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionImport")
    
    # Check the test variable
    qtbot.waitUntil(check_status)
    
    assert True


def menu_click(qtbot, main_window, menu, action_name):
        
    qtbot.keyClick(main_window, menu.title().at(1).toLatin1(),
                   QtCore.Qt.AltModifier)
                
    for action in menu.actions():
        
        if not action.objectName(): continue
            
        if action.objectName() and action.objectName() == action_name:
            qtbot.keyClick(menu, QtCore.Qt.Key_Enter)
            return
        
        qtbot.wait(200)
        qtbot.keyClick(menu, QtCore.Qt.Key_Down)
        
    errStr = "Action '{}' not found in menu '{}'".format(action_name,
                                                         menu.objectName())
    raise ValueError(errStr)
