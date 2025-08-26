from manim import *

class GeneratedScene(Scene):
    def construct(self):
        last_obj = None
        if last_obj: self.remove(last_obj)
        txt_1 = Text("The sun is very bright!", color="yellow", font_size=48).move_to(ORIGIN)
        self.play(FadeIn(txt_1))
        self.wait(2.4)
        last_obj = txt_1

        if last_obj: self.remove(last_obj)
        txt_2 = Text("It sends out many colors!", color="orange", font_size=36).move_to(ORIGIN)
        self.play(Write(txt_2))
        self.wait(2.4)
        last_obj = txt_2

        if last_obj: self.remove(last_obj)
        txt_3 = Text("Like a rainbow!", color="red", font_size=36).move_to(ORIGIN)
        self.play(FadeIn(txt_3))
        self.play(Wiggle(txt_3))
        self.wait(1.56)
        last_obj = txt_3

        if last_obj: self.remove(last_obj)
        txt_4 = Text("Tiny air bits scatter light", color=ManimColor("#ADD8E6"), font_size=36).move_to(ORIGIN)
        self.play(GrowFromCenter(txt_4))
        self.wait(2.4)
        last_obj = txt_4

        if last_obj: self.remove(last_obj)
        txt_5 = Text("Blue scatters the most!", color="blue", font_size=36).move_to(ORIGIN)
        self.play(FadeIn(txt_5))
        self.play(Flash(txt_5))
        self.wait(1.98)
        last_obj = txt_5

        if last_obj: self.remove(last_obj)
        txt_6 = Text("That's why we see blue!", color="blue", font_size=48).move_to(ORIGIN)
        self.play(FadeIn(txt_6))
        self.play(ScaleInPlace(txt_6,1.4))
        self.wait(2.4)
        last_obj = txt_6

        if last_obj: self.remove(last_obj)
        txt_7 = Text("Red and orange go down!", color=ManimColor("#FFFFFF"), font_size=36).move_to(ORIGIN)
        self.play(FadeIn(txt_7))
        self.wait(2.4)
        last_obj = txt_7

        if last_obj: self.remove(last_obj)
        txt_8 = Text("So the sky is blue!", color=ManimColor("#FFFFFF"), font_size=48).move_to(ORIGIN)
        self.play(FadeIn(txt_8))
        self.wait(2.4)
        last_obj = txt_8
