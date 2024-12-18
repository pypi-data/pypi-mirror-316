from traitlets import Bool, Dict, Float, List, Tuple, Unicode, default

from ..trait_types import Attribute, Event
from .hra_app import HraAppWidget


class BodyUi(HraAppWidget):
    """Displays the Body UI application."""

    _tag_name = "hra-body-ui"
    _scripts = [
        "https://cdn.humanatlas.io/ui/body-ui/polyfills.js",
        "https://cdn.humanatlas.io/ui/body-ui/main.js",
    ]
    _styles = []

    @default("height")
    def _height_default(self) -> str:
        return "700px"

    scene = Attribute(Unicode() | List(), required=True, help="Url to scene.")
    rotation = Attribute(
        Float(), default_value=None, allow_none=True, help="Rotation of the scene."
    )
    rotation_x = Attribute(
        Float(), default_value=None, allow_none=True, help="X rotation of the scene."
    )
    zoom = Attribute(
        Float(), default_value=None, allow_none=True, help="Zoom of the scene."
    )
    target = Attribute(
        Tuple(Float(), Float(), Float()),
        default_value=None,
        allow_none=True,
        help="Target of the scene.",
    )
    bounds = Attribute(
        Dict(per_key_traits={"x": Float(), "y": Float(), "z": Float()}),
        default_value=None,
        allow_none=True,
        help="Bounds of the scene.",
    )
    camera = Attribute(
        Unicode(),
        default_value=None,
        allow_none=True,
        help="Camera to use. Orthographic or orbit.",
    )
    interactive = Attribute(
        Bool(), default_value=True, help="Whether the scene is interactive."
    )

    on_rotation_change = Event(
        event_name="rotationChange",
        help="Event emitted when the model rotation changes.",
    )
    on_node_click = Event(
        event_name="nodeClick", help="Event emitted when a cell is clicked."
    )
    on_node_drag = Event(
        event_name="nodeDrag", help="Event emitted when a cell is dragged."
    )
    on_node_hover_start = Event(
        event_name="nodeHoverStart", help="Event emitted when a cell is hovered."
    )
    on_node_hover_end = Event(
        event_name="nodeHoverEnd",
        help="Event emitted when a cell is no longer hovered.",
    )
