from kivy.uix.image import Image as KivyImage


class Image(KivyImage):
    def __init__(self, window, x, y, image_path, scale=1.0, visibility=True, tag=None):
        super().__init__(source=image_path, size_hint=(None, None), pos=(x, y))

        self.scale_factor = scale
        self.tag = tag

        # Set scaling and positioning
        self.set_scale(self.scale_factor)
        self.visibility = visibility  # Initialize visibility state
        self.set_visibility( self.visibility)

        window.add_widget(self)

    def set_scale(self, scale):
        """Scale the image based on the scale parameter."""
        self.width = self.texture_size[0] * scale
        self.height = self.texture_size[1] * scale

    def set_position(self, x, y):
        """Update the position of the image."""
        self.pos = (x, y)

    def set_image(self, image_path):
        """Set a new image."""
        self.source = image_path

    def set_visibility(self, visibility):
        """Show or hide the image."""
        if visibility:
            self.opacity = 1
        else:
            self.opacity = 0

        self.visibility = visibility
