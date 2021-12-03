from magicclass import magicclass, MagicTemplate, field
import napari

from .viewerstate import ViewerState
from .taskview import MainWidget


@magicclass(layout="horizontal", labels=False)
class MultiTaskWidget(MagicTemplate):
    _taskview = MainWidget()
    def change_task(self):
        self._taskview.visible = True
    
    current_task = field(str, options={"enabled": False})