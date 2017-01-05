
#    Copyright (C) 2016 Mathew Topper, Rui Duarte
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Set up logging
import logging

module_logger = logging.getLogger(__name__)

from PyQt4 import QtGui, QtCore

from dtocean_core.strategies.basic import BasicStrategy

from . import GUIStrategy, StrategyWidget, PyQtABCMeta
from ..widgets.dialogs import Message


class GUIBasicStrategy(GUIStrategy, BasicStrategy):
    
    """A basic strategy which will run all selected modules and themes in
    sequence."""
    
    def __init__(self):
        
        BasicStrategy.__init__(self)
        GUIStrategy.__init__(self)
        
        return
    
    @property
    def allow_rerun(self):
        
        return True
        
    def get_weight(self):

        '''A method for getting the order of priority of the strategy.

        Returns:
          int
        '''

        return 1
    
    def get_widget(self, parent, shell):
        
        widget = BasicWidget(parent, "No Configuration Required")
        
        return widget


class BasicWidget(Message, StrategyWidget):
    
    __metaclass__ = PyQtABCMeta
    
    config_set = QtCore.pyqtSignal()
    config_null = QtCore.pyqtSignal()
    
    def __init__(self, parent, text):
        
        super(BasicWidget, self).__init__(parent, text)
        
        return
        
    def get_configuration(self):
                
        return {}

    def set_configuration(self, *args):
                
        return

    def paintEvent(self, event):
        
        super(BasicWidget, self).paintEvent(event)
        self.config_set.emit()
        
        return

        

