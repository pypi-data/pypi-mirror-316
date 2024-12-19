from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Line

class CircleShape(Widget):
    def __init__(self, window, x, y, radius, color=(1, 1, 1, 1), border_color=None, border_width=1, visibility=True, tag=None):
        super().__init__(size_hint=(None, None), pos=(x, y))

        self.radius = radius
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.tag = tag
        self.visibility = visibility

        # Add the circle to the canvas
        with self.canvas:
            self.color_instruction = Color(*self.color)  # RGBA color
            self.circle = Ellipse(size=(self.radius * 2, self.radius * 2), pos=self.pos)

            if self.border_color:
                self.border_color_instruction = Color(*self.border_color)  # RGBA border color
                self.border = Line(circle=(self.center_x, self.center_y, self.radius), width=self.border_width)

        # Set initial visibility
        self.set_visibility(self.visibility)

        # Add the widget to the window
        window.add_widget(self)

    @property
    def center_x(self):
        return self.x + self.radius

    @property
    def center_y(self):
        return self.y + self.radius

    def set_radius(self, radius):
        """Update the radius of the circle."""
        self.radius = radius
        self.circle.size = (self.radius * 2, self.radius * 2)

        if self.border_color:
            self.border.circle = (self.center_x, self.center_y, self.radius)

    def set_position(self, x, y):
        """Update the position of the circle."""
        self.pos = (x, y)
        self.circle.pos = self.pos

        if self.border_color:
            self.border.circle = (self.center_x, self.center_y, self.radius)

    def set_color(self, color):
        """Update the color of the circle."""
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
            self.border.width = self.border_width

    def set_visibility(self, visibility):
        """Show or hide the circle."""
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

    # Create a circle with a border
    circle = CircleShape(window, 50, 50, 75,
                         color=(1, 0, 0, 1), border_color=(0, 1, 0, 1), border_width=5, visibility=True, tag="circle1")

    window.show()
