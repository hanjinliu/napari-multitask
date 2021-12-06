from __future__ import annotations
from typing import Any, TYPE_CHECKING
import napari
from napari.layers import Image, Labels, Points, Shapes

_HasMode = (Labels, Points, Shapes)
_HasInterpolation = (Image, Labels)

if TYPE_CHECKING:
    from napari.components.layerlist import LayerList
    from napari._qt.widgets.qt_viewer_dock_widget import QtViewerDockWidget

_LAYERS = "layers"
_NEAREST = "nearest"

def _translate_layers(layers: LayerList):
    n_layer = len(layers)
    return [layers.pop(0) for _ in range(n_layer)]
    
class ViewerState:
    """
    This object stores (almost) all the information of viewer.
    """    
    def __init__(self, 
                 viewer_params: dict[str, Any] = None, 
                 dock_widgets: dict[str, QtViewerDockWidget] = None
                 ) -> None:
        if viewer_params is not None:
            self.layers = _translate_layers(viewer_params.pop(_LAYERS))
            self.viewer_params = viewer_params
        else:
            self.layers = []
            self.viewer_params = {}
        
        self.dock_widgets  = dock_widgets or {}
            
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
                if name == "dims":
                    # TODO: Bug in dims. Don't update all the dims for now.
                    value = {"ndisplay": value.get("ndisplay", 2)}
                try:
                    getattr(viewer, name).update(value)
                except AttributeError:
                    pass
        
        # Update layer list
        for layer in self.layers:
            if isinstance(layer, _HasInterpolation):
                interp = layer.interpolation
                layer.interpolation = _NEAREST
            viewer.add_layer(layer)
            if isinstance(layer, _HasInterpolation):
                layer.interpolation = interp
        
        # Events should be emitted here to update layer control.
        for layer in viewer.layers.selection:
            if isinstance(layer, _HasMode):
                layer.events.mode(mode=layer.mode)
                
        # Update dock widget visibility
        for dockname, dock in viewer.window._dock_widgets.items():
            dock.setVisible(dockname in self.dock_widgets.keys())
        