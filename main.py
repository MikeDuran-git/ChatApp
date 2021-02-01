from typing import Text
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty


Window.keyboard_anim_args = {'d': .1, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"



class MyBoxLayout(BoxLayout):
    scrollview=ObjectProperty(None)
    msg=ObjectProperty(None)
    msg_output=ObjectProperty(None)

    def send(self):
        if self.msg.text != "":
            self.msg_output.text+=self.msg.text+"\n"            
            print(self.msg.text)
            self.msg.text=""


class MyApp(App):
    
    def build(self):

        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
