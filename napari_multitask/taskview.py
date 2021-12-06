from magicclass import magicclass, MagicTemplate, set_design
from magicclass.utils import show_messagebox
from napari_plugin_engine import napari_hook_implementation
from .taskpanel import TaskPanel, WIDTH, HEIGHT

@magicclass(layout="horizontal", widget_type="scrollable")
class TaskView(MagicTemplate):        
    def __post_init__(self):
        default_task = TaskPanel()
        self.insert(0, default_task)
        default_task.callbacks.append(self._change_task)
        default_task._taskpanel.on_delete = lambda: self._remove_task(default_task)
        default_task._set_down(True)
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
        self.parent_dock_widget.setVisible(True)
    
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
        new_task._taskpanel.on_delete = lambda: self._remove_task(new_task)
        self.parent_viewer.dims.ndisplay = 2
    
    def _remove_task(self, task: TaskPanel):
        if len(self) == 2:
            show_messagebox("error", "Error", "This is the last task. You cannot delete it.",
                            self.native)
        else:
            if task is self[self.current_index]:
                # if current task is about to be deleted, we should change the task before
                # the task deletion.
                if self.current_index == 0:
                    next_task = self[1]
                else:
                    next_task = self[self.current_index - 1]
                self._change_task(next_task)
            
            # decrement current index if younger task is about to be deleted.
            index = self.index(task)
            if index < self.current_index:
                self.current_index -= 1

            self.remove(task)
            task.viewer_state.layers.clear()
            task._taskpanel.deleteLater()
            del task

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    widget_options = {
        "name": "napari-multitask",
        "area": "bottom",
    }
    return TaskView, widget_options