"""Graph class module."""

from zmc.utils.deprecated import deprecated_component

from .core import DataSenderBaseComponent


__all__ = [
    "Graph",
    "LineGraph",
    "ScatterPlot",
    "Histogram",
    "Heatmap",
    "ContourPlot",
    "ImagePlot",
]

class Line:
    """Line class."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

class LineGraph(DataSenderBaseComponent):
    """Line Graph component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._lines = list[Line]()

    @property
    def data(self):
        return {
            "lines": [
                {
                    "x": list(line.x),
                    "y": list(line.y),
                }
                for line in self._lines
            ]
        }

    def _fill_missing_lines(self, new_length):
        for _ in range(len(self._lines), new_length):
            self._lines.append(Line([], []))

    def append_data(self, x, y, *, line_index=0):
        """Add a x, y pair to the graph and send data via server."""
        self._fill_missing_lines(line_index + 1)
        self._lines[line_index].x.append(x)
        self._lines[line_index].y.append(y)
        self._send_data()

    def plot(self, x, y, *, line_index=0):
        """Replace graph data entirely and send it."""
        self._fill_missing_lines(line_index + 1)
        self._lines[line_index].x = x
        self._lines[line_index].y = y
        self._send_data()


@deprecated_component(version="0.1.0", reason="Use LineGraph instead")
class Graph(LineGraph):
    """Line Graph component class."""


class ScatterPlot(DataSenderBaseComponent):
    """Scatter Plot component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._x = []
        self._y = []

    @property
    def data(self):
        return {
            "x": list(self._x),
            "y": list(self._y),
        }

    def plot(self, x, y):
        """Replace data entirely and send it."""
        self._x = x
        self._y = y
        self._send_data()


class Histogram(DataSenderBaseComponent):
    """Histogram component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._x = []

    @property
    def data(self):
        return {
            "x": list(self._x),
        }

    def plot(self, x):
        """Replace data entirely and send it."""
        self._x = x
        self._send_data()


class Heatmap(DataSenderBaseComponent):
    """Heatmap component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._x = []
        self._y = []
        self._z = []

    @property
    def data(self):
        return {
            "x": list(self._x),
            "y": list(self._y),
            "z": list(self._z),
        }

    @property
    def x(self):
        """x values, stored in a 1-D array"""
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        """y values, stored in a 1-D array"""
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def append_row(self, row):
        """Add a row to the heatmap and send it to the app."""
        self._z.append(row)
        self._send_data()

    # TODO: make it like matplotlib
    def plot(self, z, x=None, y=None):
        """Replace heatmap data entirely and send it."""
        self._z = z
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._send_data()

class ContourPlot(Heatmap):
    """Contour Plot component class."""

class ImagePlot(DataSenderBaseComponent):
    """Image Plot component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._image = []

    @property
    def data(self):
        return {
            "image": list(self._image),
        }

    def plot(self, image):
        """Replace image data entirely and send it."""
        self._image = image
        self._send_data()
