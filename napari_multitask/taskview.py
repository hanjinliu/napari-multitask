from typing import Callable
from magicclass import magicclass, MagicTemplate, set_design, field, do_not_record
from magicgui.widgets import Label
import napari
from napari._qt.widgets.qt_viewer_dock_widget import QtViewerDockWidget

from .taskpanel import TaskPanel, WIDTH, HEIGHT



def find_dock_widget(widget):
    while not isinstance(widget, QtViewerDockWidget):
        widget = widget.parent()
    return widget

@magicclass(layout="horizontal", widget_type="scrollable")
class TaskView(MagicTemplate):
    def __post_init__(self):
        default_task = TaskPanel()
        default_task.callbacks.append(self._change_task)
        self.insert(0, default_task)
        self.current_index = 0
        self.margins = (0, 0, 0, 0)
        self.min_height = HEIGHT + 40

    def _change_task(self, new: TaskPanel):
        old: TaskPanel = self[self.current_index]
        if old is new:
            old._set_down(True)
            return
        old._set_screenshot(self.parent_viewer)
        old._set_down(False)
        current_state = old.viewer_state
        current_state.save_state(self.parent_viewer)

        self.current_index = self.index(new)
        
        new.viewer_state.update_viewer(self.parent_viewer)
        new._set_down(True)
        self.native.parent().setVisible(True)
    
    @set_design(text="+", font_size=48, 
                min_width=WIDTH, max_width=WIDTH, width=WIDTH, 
                min_height=HEIGHT, max_height=HEIGHT, height=HEIGHT
                )
    def add_new_task(self):
        """
        Open a new task panel.
        """        
        new_task = TaskPanel()
        self.insert(len(self)-1, new_task)
        self._change_task(new_task)
        new_task.callbacks.append(self._change_task)
        self.parent_viewer.dims.ndisplay = 2
    