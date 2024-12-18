from __future__ import annotations

import json
import typing as t

from traitlets import Bool, Dict, Enum, Integer, List, Unicode, default

from ..trait_types import Attribute, Event
from .hra_app import HraAppWidget


def _as_string_or_json(value, _widget) -> str:
    return value if value is None or isinstance(value, str) else json.dumps(value)


class NodeDistVis(HraAppWidget):
    """Displays the HRA node distance visualization."""

    _tag_name = "hra-node-dist-vis"
    _scripts = ["https://cdn.humanatlas.io/ui/node-dist-vis-wc/wc.js"]
    _styles = []

    @default("height")
    def _height_default(self) -> str:
        return "700px"

    mode = Attribute(
        Enum(["expore", "inspect", "select"], default_value=None, allow_none=True),
        help="View mode.",
    )
    nodes = Attribute(
        Unicode() | List(),
        required=True,
        help="Nodes to display, either an url or a list of nodes.",
    ).tag(to_json=_as_string_or_json)
    node_keys = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Mapping between expected columns and columns in the nodes data.",
    )
    node_target_selector = Attribute(
        Unicode(None, allow_none=True), help="Target type used when computing edges."
    )
    node_target_key = Attribute(
        Unicode(), required=False, help="DEPRECATED: Column name of node targets."
    )
    node_target_value = Attribute(
        Unicode(), required=False, help="DEPRECATED: Anchor node."
    )
    edges = Attribute(
        Unicode(None, allow_none=True) | List(),
        help="Edges between nodes, either an url or a list of edges.",
    ).tag(to_json=_as_string_or_json)
    edge_keys = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Mapping between expected columns and columns in the edges data.",
    )
    edges_disabled = Attribute(
        Bool(None, allow_none=True), help="Whether edges are shown."
    )
    max_edge_distance = Attribute(
        Integer(), help="Max distance between nodes when calculating edges."
    )
    color_map = Attribute(
        Unicode(None, allow_none=True) | List(), help="Color map url."
    )
    color_map_keys = Attribute(
        Unicode(None, allow_none=True) | Dict(),
        help="Mapping between expected columns and columns in the color map data.",
    )
    color_map_key = Attribute(
        Unicode(None, allow_none=True),
        help="DEPRECATED: Column name of the node targets.",
    )
    color_map_data = Attribute(
        Unicode(None, allow_none=True), help="DEPRECATED: Column name of colors."
    )
    node_filter = Attribute(
        Unicode(None, allow_none=True) | Dict(), help="Node filter object."
    )
    selection = Attribute(
        List(default_value=None, allow_none=True),
        help="DEPRECATED: Selection of nodes to display.",
    )

    on_node_click = Event(
        event_name="nodeClick", help="Event emitted when a cell is clicked."
    )
    on_node_hover = Event(
        event_name="nodeHover",
        help="Event emitted when a cell is hovered over. Emits None when the user stops hovering.",
    )
    on_node_selection_change = Event(
        event_name="nodeSelectionChange",
        help="Emits when the user selects one or more nodes in the 'select' view mode.",
    )
