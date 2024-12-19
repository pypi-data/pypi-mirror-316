from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line


class RectangleShape(Widget):
    def __init__(self, window, x, y, width, height, radius=0, visibility=True,
                 color=(1, 1, 1, 1), border_color=None, border_width=1,
                 tag=None):
        super().__init__(size_hint=(None, None), pos=(x, y))

        self.width = width
        self.height = height
        self.radius = radius
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.tag = tag
        self.visibility = visibility

        # Add the rounded rectangle and optional border to the canvas
        with self.canvas:
            self.color_instruction = Color(*self.color)  # RGBA color
            self.rounded_rect = RoundedRectangle(size=(self.width, self.height), pos=self.pos, radius=[self.radius])

            if self.border_color:
                self.border_color_instruction = Color(*self.border_color)  # RGBA border color
                self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius),
                                        width=self.border_width)

        # Set initial visibility
        self.set_visibility(self.visibility)

        # Add the widget to the window
        window.add_widget(self)

    def set_size(self, width, height):
        """Update the size of the rounded rectangle."""
        self.width = width
        self.height = height
        self.rounded_rect.size = (self.width, self.height)

        if self.border_color:
            self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)

    def set_position(self, x, y):
        """Update the position of the rounded rectangle."""
        self.pos = (x, y)
        self.rounded_rect.pos = self.pos

        if self.border_color:
            self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)

    def set_radius(self, radius):
        """Update the corner radius of the rounded rectangle."""
        self.radius = radius
        self.rounded_rect.radius = [self.radius]

        if self.border_color:
            self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)

    def set_color(self, color):
        """Update the color of the rounded rectangle."""
        self.color = color
        self.color_instruction.rgba = self.color

    def set_border_color(self, border_color):
        """Update the color of the border."""
        self.border_color = border_color
        if self.border_color:
            self.border_color_instruction.rgba = self.border_color

    def set_border_width(self, border_width):
        """Update the width of the border."""
        self.border_width = border_width
        if self.border_color:
            self.border_line.width = self.border_width

    def set_visibility(self, visibility):
        """Show or hide the rounded rectangle."""
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

    # Create a rounded rectangle with a border
    rectangle = RectangleShape(
        window, 50, 50, 150, 100, 10,
        color=(0.5, 0.5, 1, 1), border_color=(1, 0, 0, 1), border_width=2,
        visibility=True, tag="rounded1"
    )

    window.show()
