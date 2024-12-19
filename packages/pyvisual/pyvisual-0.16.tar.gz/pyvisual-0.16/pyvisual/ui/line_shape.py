from kivy.uix.widget import Widget
from kivy.graphics import Line, Color

class LineShape(Widget):
    def __init__(self, window, points, width=1, color=(1, 1, 1, 1), visibility=True, tag=None):
        super().__init__(size_hint=(None, None))

        self.points = points  # List of (x, y) coordinates for the line
        self.width = width
        self.color = color
        self.tag = tag
        self.visibility = visibility

        # Add the line to the canvas
        with self.canvas:
            self.color_instruction = Color(*self.color)  # RGBA color
            self.line = Line(points=self.points, width=self.width)

        # Set initial visibility
        self.set_visibility(self.visibility)

        # Add the widget to the window
        window.add_widget(self)

    def set_points(self, points):
        """Update the points of the line."""
        self.points = points
        self.line.points = self.points

    def set_width(self, width):
        """Update the width of the line."""
        self.width = width
        self.line.width = self.width

    def set_color(self, color):
        """Update the color of the line."""
        self.color = color
        self.color_instruction.rgba = self.color

    def set_visibility(self, visibility):
        """Show or hide the line."""
        if visibility:
            self.opacity = 1
            self.canvas.opacity = 1
        else:
            self.opacity = 0
            self.canvas.opacity = 0

        self.visibility = visibility


if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()

    # Create a line
    line = LineShape(window, points=[0, 0, 100, 100], width=5, color=(0, 1, 0, 1),
                     visibility=True, tag="line1")
    window.show()
