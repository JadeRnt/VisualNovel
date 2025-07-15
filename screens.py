from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader

from stories.alex_story import AlexStory
from stories.lisa_story import LisaStory

class MessageBubble(BoxLayout):
    def __init__(self, text=None, image_path=None, color=(0.9, 0.9, 0.9, 1), **kwargs):
        super().__init__(orientation='horizontal',
                         size_hint_y=None,
                         height=120 if image_path else 50,
                         padding=10,
                         spacing=10,
                         **kwargs)

        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(radius=[15, ])
            self.bind(pos=self.update_rect, size=self.update_rect)

        if image_path:
            self.add_widget(Image(source=image_path, size_hint=(None, None), size=(100, 100)))
        else:
            lbl = Label(text=text, color=(0, 0, 0, 1), halign='left', valign='middle')
            lbl.bind(size=lambda inst, val: lbl.setter('text_size')(lbl, val))
            self.add_widget(lbl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PhoneAppLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background table
        self.bg = Image(
            source="assets/background_table.jpg",
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.bg)

        # Phone frame (toujours visible)
        self.phone_img = Image(
            source="assets/phone_frame.png",
            size_hint=(None, None),
            size=(360, 640),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.phone_img)

        # Phone screen layout
        self.phone_screen = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(340, 620),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=10,
            padding=10
        )

        # ✅ Fond blanc DANS phone_screen
        with self.phone_screen.canvas.before:
            Color(1, 1, 1, 1)  # blanc opaque
            self.rect_bg = RoundedRectangle(radius=[40,])

        self.phone_screen.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(self.phone_screen)

    def update_rect(self, *args):
        self.rect_bg.pos = self.phone_screen.pos
        self.rect_bg.size = self.phone_screen.size



class ContactsScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.layout = PhoneAppLayout()
        self.add_widget(self.layout)

        self.title = Label(text="📱 Mes conversations", font_size=24, size_hint=(1, None),
                           height=50, color=(0, 0, 0, 1))
        self.layout.phone_screen.add_widget(self.title)

        self.list_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.list_box)
        self.layout.phone_screen.add_widget(scroll)

        self.refresh_contacts()

    def refresh_contacts(self):
        self.list_box.clear_widgets()

        for name, char in self.game.characters.items():
            btn = Button(
                text=f"{name} (Amitié : {char.friendship})",
                size_hint=(1, None),
                height=60,
                background_normal='',
                background_color=char.color
            )
            btn.bind(on_release=lambda instance, name=name: self.open_chat(name))
            self.list_box.add_widget(btn)

    def on_enter(self):
        self.refresh_contacts()

    def open_chat(self, name):
        self.game.active_character = name
        self.manager.transition.direction = "left"
        self.manager.current = "chat"


class ChatScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        # Chargement des histoires
        self.story_instances = {
            "Alex": AlexStory(),
            "Lisa": LisaStory()
        }

        self.layout = PhoneAppLayout()
        self.add_widget(self.layout)

        self.header = Label(text="", size_hint=(1, None), height=40, color=(0, 0, 0, 1))
        self.layout.phone_screen.add_widget(self.header)

        self.scroll = ScrollView(size_hint=(1, 0.65))
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=10)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll.add_widget(self.chat_box)
        self.layout.phone_screen.add_widget(self.scroll)

        self.buttons_box = BoxLayout(size_hint=(1, None), height=100, spacing=5, padding=5)
        self.layout.phone_screen.add_widget(self.buttons_box)

        self.back_btn = Button(text="⬅ Retour", size_hint=(1, None), height=50,
                               background_color=(0.7, 0.7, 0.7, 1))
        self.back_btn.bind(on_release=self.go_back)
        self.layout.phone_screen.add_widget(self.back_btn)

        self.sounds = {
            "message_received": SoundLoader.load("assets/message_received.wav"),
            "message_sent": SoundLoader.load("assets/message_sent.wav"),
        }

    def on_enter(self):
        self.clear_chat()
        self.char = self.game.characters[self.game.active_character]
        self.story = self.story_instances[self.char.name]
        self.header.text = f"Chat avec {self.char.name}"

        if self.char.current_scene == "intro":
            self.show_message(f"{self.char.name} : {self.story.get_intro()}", self.char.color)
            choices = self.story.get_choices(self)
            self.show_choices(choices)
        elif self.char.current_scene in ["secret", "passion"]:
            self.story.continue_scene(self)
        elif self.char.current_scene == "photo":
            self.story.final_scene(self)

    def continue_story(self):
        self.on_enter()

    def show_message(self, text, color):
        bubble = MessageBubble(text=text, color=color)
        self.chat_box.add_widget(bubble)
        self.scroll.scroll_y = 0

    def show_photo(self, path):
        bubble = MessageBubble(image_path=path, color=(1, 1, 1, 1))
        self.chat_box.add_widget(bubble)
        self.scroll.scroll_y = 0

    def show_choices(self, choices):
        self.buttons_box.clear_widgets()
        for text, callback in choices:
            btn = Button(
                text=text,
                background_normal='',
                background_color=(0.2, 0.6, 1, 1),
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=50
            )
            def make_cb(cb):
                return lambda instance: self.on_choice(cb)
            btn.bind(on_release=make_cb(callback))
            self.buttons_box.add_widget(btn)


    def on_choice(self, callback):
        self.play_sound("message_sent")
        self.buttons_box.clear_widgets()
        callback()

    def clear_chat(self):
        self.chat_box.clear_widgets()

    def end_story(self):
        self.show_message("🎮 [Fin de la démo pour l’instant.]", (0, 0, 0, 1))

    def go_back(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "contacts"

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.stop()
            sound.play()
