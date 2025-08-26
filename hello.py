from manim import *

class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello, AI Video Generator!")
        self.play(Write(text))
        self.wait(2)
