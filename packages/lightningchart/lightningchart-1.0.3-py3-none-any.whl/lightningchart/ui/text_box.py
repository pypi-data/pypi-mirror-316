from __future__ import annotations
import lightningchart
from lightningchart.ui import UIEWithPosition, UIElement


class TextBox(UIEWithPosition):
    """UI Element for adding text annotations on top of the chart."""

    def __init__(
            self,
            chart,
            text: str = None,
            x: int = None,
            y: int = None,
            position_scale: str = 'axis'
    ):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'textBox', {'chart': self.chart.id, 'positionScale': position_scale})

        if text:
            self.set_text(text)
        if x and y:
            self.set_position(x, y)

    def set_text(self, text: str):
        """Set the content of the text box.

        Args:
            text (str): Text string.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setText', {'text': text})
        return self

    def set_padding(self,  *args, **kwargs):
        """Set padding around object in pixels.

        Usage:
            - `set_padding(5)`: Sets uniform padding for all sides (integer or float).
            - `set_padding(left=10, top=15)`: Sets padding for specific sides only.
            - `set_padding(left=10, top=15, right=20, bottom=25)`: Fully define padding for all sides.

        Args:
            *args: A single numeric value (int or float) for uniform padding on all sides.
            **kwargs: Optional named arguments to specify padding for individual sides:
                - `left` (int or float): Padding for the left side.
                - `right` (int or float): Padding for the right side.
                - `top` (int or float): Padding for the top side.
                - `bottom` (int or float): Padding for the bottom side.

        Returns:
            The instance of the class for fluent interface.
        """
        if len(args) == 1 and isinstance(args[0], (int, float)):
            padding = args[0]
        elif kwargs:
            padding = {}
            for key in ['left', 'right', 'bottom', 'top']:
                if key in kwargs:
                    padding[key] = kwargs[key]
        else:
            raise ValueError(
                "Invalid arguments. Use one of the following formats:\n"
                "- set_padding(5): Uniform padding for all sides.\n"
                "- set_padding(left=10, top=15): Specify individual sides.\n"
                "- set_padding(left=10, top=15, right=20, bottom=25): Full padding definition."
            )

        self.instance.send(self.id, 'setPadding', {'padding': padding})
        return self

    def set_text_fill_style(self, color: lightningchart.Color):
        """Set the color of the text.

        Args:
            color (Color): Color of the text.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFillStyle', {'color': color.get_hex()})
        return self

    def set_text_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set the font style of the text.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_text_rotation(self, rotation: int | float):
        """Set the rotation of the text.

        Args:
            rotation (int | float): Rotation in degrees.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextRotation', {'rotation': rotation})
        return self
