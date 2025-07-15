from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from models import VisualNovelGame
from screens import ContactsScreen, ChatScreen

class VisualNovelApp(App):
    def build(self):
        game = VisualNovelGame()
        sm = ScreenManager()
        sm.add_widget(ContactsScreen(game, name="contacts"))
        sm.add_widget(ChatScreen(game, name="chat"))
        return sm

if __name__ == '__main__':
    VisualNovelApp().run()
