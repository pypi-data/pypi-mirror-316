from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class Text(AnchorLayout):
    def __init__(self, window, x, y, text, font_size=20, text_color=(1, 1, 1, 1), bg_color=(0, 0, 0, 1),
                 alignment="center", rect_width=None, visibility=True, tag=None, font_name=None):
        super().__init__(anchor_x="center", anchor_y="center", size_hint=(None, None), size=(rect_width, font_size), pos=(x, y))

        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.rect_width = rect_width or 200
        self.rect_height = font_size or 50
        self.visibility = visibility
        self.tag = tag
        self.alignment = alignment
        self.font_name = font_name

        # Add the background rectangle
        with self.canvas.before:
            self.bg_color_instruction = Color(*self.bg_color)  # Background color
            self.rectangle = Rectangle(size=(self.rect_width, self.rect_height), pos=self.pos)

        # Add the label
        self.label = Label(
            text=self.text,
            font_size=self.font_size,
            color=self.text_color,
            size_hint=(None, None),
            size=(self.rect_width, self.rect_height),
            halign=self.alignment,
            valign="middle",
            font_name=self.font_name
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.update_label_alignment()
        self.add_widget(self.label)

        # Set initial visibility
        self.set_visibility(self.visibility)

        # Add the widget to the window
        window.add_widget(self)

    def update_label_alignment(self):
        """Recalculate text alignment for the label."""
        self.label.text_size = (self.rect_width, self.rect_height)
        self.label.halign = self.alignment
        self.label.valign = "middle"

    def set_text(self, text):
        """Update the text."""
        self.text = text
        self.label.text = self.text

    def set_font_size(self, font_size):
        """Update the font size of the text."""
        self.font_size = font_size
        self.label.font_size = self.font_size

    def set_text_color(self, text_color):
        """Update the text color."""
        self.text_color = text_color
        self.label.color = self.text_color

    def set_bg_color(self, bg_color):
        """Update the background color."""
        self.bg_color = bg_color
        self.bg_color_instruction.rgba = self.bg_color

    def set_alignment(self, alignment):
        """Update the text alignment (left, right, center)."""
        self.alignment = alignment
        self.update_label_alignment()

    def set_rect_size(self, rect_width, rect_height):
        """Update the size of the rectangle."""
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.rectangle.size = (self.rect_width, self.rect_height)
        self.label.size = (self.rect_width, self.rect_height)
        self.update_label_alignment()

    def set_visibility(self, visibility):
        """Show or hide the text and rectangle."""
        if visibility:
            self.opacity = 1
            self.canvas.opacity = 1
        else:
            self.opacity = 0
            self.canvas.opacity = 0

        self.visibility = visibility

    def set_font_name(self, font_name):
        """Update the custom font."""
        self.font_name = font_name
        self.label.font_name = self.font_name

if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()

    # Create a text with background
    text_bg = Text(
        window, x=50, y=50, text="Hello", font_size=24, text_color=(0, 0, 0, 1),
        bg_color=(0, 0, 0, 0), alignment="left", rect_width=600, visibility=True, tag="text1",
        font_name="../assets/fonts/anton/Anton-Regular.ttf"  # Provide the path to your custom font here
    )

    window.show()
