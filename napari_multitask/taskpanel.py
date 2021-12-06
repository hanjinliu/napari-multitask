
from magicclass.widgets import FreeWidget
from qtpy.QtGui import QPixmap, QFont
from qtpy.QtCore import Qt, QPoint, QSize
from qtpy.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QLabel, QMenu, QAction

import napari

from .viewerstate import ViewerState

WIDTH = 161
HEIGHT = 100

class QtTaskPanel(QPushButton):
    """
    This widget is appended to list every time new task is created.
    Looks like:
    
    [  task name  ]
     -------------
    [             ]
    [ screen shot ]
    [  of viewer  ]
    
    """    
    count: int = 0
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._contextmenu)
        
        self.setLayout(QVBoxLayout())
        self.line_edit = QLineEdit(f"Task-{self.__class__.count + 1}", self)
        self.line_edit.setFont(QFont("Arial"))
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setStyleSheet("""QLineEdit {
                                            border: none
                                            background-color: rgba(0, 0, 0, 0);
                                        }
                                     """)
        
        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.line_edit)
        self.layout().addWidget(self.image)
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.setFixedHeight(self.line_edit.height() + HEIGHT)
        self.setFixedWidth(WIDTH)
        self.__class__.count += 1
        
        self.on_delete = None
    
    def _set_pixmap(self, pixmap: QPixmap):
        size = QSize(WIDTH*1.6, HEIGHT*1.6)
        self.image.setPixmap(
            pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
    
    def _contextmenu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        
        activate = QAction("Activate", menu)
        @activate.triggered.connect
        def _(e):
            self.click()
        menu.addAction(activate)
        
        rename = QAction("Rename", menu)
        @rename.triggered.connect
        def _(e):
            self.line_edit.setFocus()
            self.line_edit.selectAll()
        menu.addAction(rename)
        
        delete = QAction("Delete", menu)
        delete.triggered.connect(lambda e: self._delete())
        menu.addAction(delete)
        
        menu.exec_(self.mapToGlobal(pos))
        
        return None
    
    def _delete(self):
        self.on_delete()
            
class TaskPanel(FreeWidget):
    def __init__(self):
        super().__init__()
        self.viewer_state = ViewerState()
        self._taskpanel = QtTaskPanel()
        self.set_widget(self._taskpanel)
        
        self.max_width = WIDTH
        
        self.callbacks = []
        self._taskpanel.clicked.connect(lambda e: self._on_click())
    
    def _set_screenshot(self, viewer: napari.Viewer):
        image = viewer.window._screenshot(False)
        pixmap = QPixmap.fromImage(image)
        self._taskpanel._set_pixmap(pixmap)
        
    def _set_down(self, down: bool):
        self._taskpanel.setDown(down)
    
    def _on_click(self):
        for callback in self.callbacks:
            callback(self)