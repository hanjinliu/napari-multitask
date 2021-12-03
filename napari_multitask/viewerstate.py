from __future__ import annotations
from typing import Any, TYPE_CHECKING
import napari
from napari.layers.base.base import Layer

if TYPE_CHECKING:
    from napari.components.layerlist import LayerList
    from napari._qt.widgets.qt_viewer_dock_widget import QtViewerDockWidget

_LAYERS = "layers"


def _translate_layers(layers: LayerList):
    n_layer = len(layers)
    return [layers.pop(0) for _ in range(n_layer)]
    
class ViewerState:
    count = 0
    def __init__(self, 
                 viewer_params: dict[str, Any] = None, 
                 layer_selection: tuple[int, str] = None,
                 dock_widgets: dict[str, QtViewerDockWidget] = None,
                 *,
                 name: str = None
                 ) -> None:
        if viewer_params is not None:
            self.layers = _translate_layers(viewer_params.pop(_LAYERS))
            self.viewer_params = viewer_params
        else:
            self.layers = []
            self.viewer_params = {}
        
        self.dock_widgets  = dock_widgets or {}
        
        if name is None:
            name = f"Task-{self.__class__.count}"
            self.__class__.count += 1
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def from_viewer(cls, viewer: napari.Viewer) -> ViewerState:
        return cls().save_state(viewer)
    
    def save_state(self, viewer: napari.Viewer) -> ViewerState:
        states: dict[str, Any] = viewer.dict()
        self.layers = _translate_layers(states.pop(_LAYERS))
        self.viewer_params = states
        self.dock_widgets = {k: v for k, v in viewer.window._dock_widgets.items() if v.isVisible()}
        return self
    
    def update_viewer(self, viewer: napari.Viewer) -> None:
        viewer.layers.clear()
        
        # Update camera, scale_bar etc.
        for name, value in self.viewer_params.items():
            if isinstance(value, dict):
                try:
                    getattr(viewer, name).update(value)
                except AttributeError:
                    pass
        
        # Update layer list
        for layer in self.layers:
            viewer.add_layer(layer)
        viewer.layers.selection = {}
            
        # Update dock widget visibility
        for dockname, dock in viewer.window._dock_widgets.items():
            dock.setVisible(dockname in self.dock_widgets.keys())
        