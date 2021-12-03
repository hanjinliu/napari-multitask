from magicclass import magicclass, MagicTemplate, field
from magicclass.widgets import ListWidget
import napari

from .viewerstate import ViewerState


@magicclass
class MainWidget(MagicTemplate):
    tasks = field(ListWidget, name="Tasks")
    
    def __post_init__(self):
        self._current: int = 0
        
        @self.tasks.register_callback(ViewerState)
        def _on_click(viewer_state: ViewerState, i: int):
            self._change_task(self._current, i)
        self.tasks.append(ViewerState())
            
    
    def New_Task(self):
        self.tasks.append(ViewerState())
        self._change_task(self._current, len(self.tasks) - 1)
    
    def _change_task(self, old: int, new: int):
        current_state: ViewerState = self.tasks[old]
        current_state.save_state(self.parent_viewer)
        self._current = new
        next_state: ViewerState = self.tasks[new]
        next_state.update_viewer(self.parent_viewer)
        self.native.parent().setVisible(True)