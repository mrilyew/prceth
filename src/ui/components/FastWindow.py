from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QPoint
from components.locale import _
from components.db import Collection, Entity, Relation
from components.settings import settings
import keyboard

class FastWindowThread(QtCore.QThread):
    show_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        self.show_signal.emit('show')

class FastWindow(QtWidgets.QWidget):
    def init_window(self):
        self.setWindowTitle('fastwindow')
        self.resize(300, 400)

        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)

        self.fw_thread = FastWindowThread()
        self.fw_thread.show_signal.connect(self.unhide_window, QtCore.Qt.ConnectionType.QueuedConnection)

        keyboard.add_hotkey('win+f7', self.fw_thread.start)
    
    def unhide_window(self):
        # Showing window
        self.setWindowFlags(self.windowFlags() | 
                            QtCore.Qt.WindowType.WindowStaysOnTopHint | 
                            QtCore.Qt.WindowType.FramelessWindowHint |
                            QtCore.Qt.WindowType.Popup
                            )

        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.activateWindow()

        if settings.get('ui.fast_window_mode') == 'from_cursor':
            cursor = QCursor.pos()

            x = cursor.x() - 20
            y = cursor.y() - 20

            self.move(x, y)
        else:
            screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()

            x = screen_geometry.width() - self.width()
            y = screen_geometry.height() - self.height() - 10

            self.move(x, y)

        self.show()

