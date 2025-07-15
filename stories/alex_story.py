class AlexStory:
    def __init__(self):
        # Chaque élément est :
        # (réplique d'Alex, [ (texte choix, méthode), ... ])
        self.steps = [
            ("Salut ! Dis, tu te souviens du parc où on allait gamin ?", [
                ("Oui bien sûr.", self.step2_yes),
                ("Non pas vraiment.", self.step2_no)
            ]),
            ("Il paraît qu’ils ont tout changé là-bas…", [
                ("Ça me rend nostalgique.", self.step3_yes),
                ("Ça m’est égal.", self.step3_no)
            ]),
            ("Moi aussi. J’ai encore la vieille photo…", [
                ("Tu me la montres ?", self.step4_yes),
                ("Garde-la pour toi.", self.step4_no)
            ]),
            ("Bon d’accord, mais… ça me fait bizarre.", [
                ("Pourquoi ?", self.step5_yes),
                ("Ok je comprends.", self.step5_no)
            ]),
            ("Parce que sur cette photo… il y a aussi quelqu’un d’autre.", [
                ("Qui ça ?", self.step6_yes),
                ("Laisse tomber.", self.step6_no)
            ]),
            ("Mon grand frère. Tu ne l’as jamais rencontré.", [
                ("Tu m’en parles ?", self.step7_yes),
                ("Pas obligé.", self.step7_no)
            ]),
            ("Il vivait loin… Mais c’était mon héros.", [
                ("Il te manque ?", self.step8_yes),
                ("C’est la vie.", self.step8_no)
            ]),
            ("Énormément. J’aurais aimé qu’il te connaisse.", [
                ("C’est touchant.", self.step9_yes),
                ("Oublie ça.", self.step9_no)
            ]),
            ("Il m’a appris la guitare.", [
                ("Tu joues encore ?", self.step10_yes),
                ("C’est cool.", self.step10_no)
            ]),
            ("Oui, surtout quand je pense à lui.", [
                ("Tu me joueras un jour ?", self.step11_yes),
                ("Tu devrais arrêter.", self.step11_no)
            ]),
            ("Je suis trop timide. J’ai peur que tu trouves ça nul.", [
                ("Impossible.", self.step12_yes),
                ("Bof.", self.step12_no)
            ]),
            ("Tu crois vraiment ?", [
                ("Évidemment.", self.step13_yes),
                ("Je plaisantais.", self.step13_no)
            ]),
            ("Merci, ça me rassure.", [
                ("Toujours là pour toi.", self.step14_yes),
                ("Bon, on change de sujet.", self.step14_no)
            ]),
            ("Ça me fait du bien de parler avec toi.", [
                ("Pareil.", self.step15_yes),
                ("Je dois y aller.", self.step15_no)
            ]),
            ("Attends, regarde la photo.", [
                ("Super !", self.step16_yes),
                ("C’est pas la peine.", self.step16_no)
            ]),
            ("Trop tard, je te l’envoie quand même.", [
                ("Hâte de la voir !", self.step17_yes),
                ("Bon… ok.", self.step17_no)
            ]),
            ("Prêt(e) ?", [
                ("Oui !", self.step18_yes),
                ("Non.", self.step18_no)
            ]),
            ("Tadaaaa !", [
                ("Magnifique.", self.step19_yes),
                ("Mouais.", self.step19_no)
            ]),
            ("C’est mon meilleur souvenir.", [
                ("Merci de le partager.", self.step20_yes),
                ("C’est trop perso.", self.step20_no)
            ]),
        ]
        self.index = 0

    def get_intro(self):
        self.index = 0
        return self.steps[self.index][0]

    def get_choices(self, chat_screen):
        return [(text, lambda cb=cb: cb(chat_screen)) for text, cb in self.steps[self.index][1]]

    def default_step(self, chat_screen, message, delta_friendship, next_step=True):
        chat_screen.show_message(f"Toi : {message}", (0.7, 0.7, 0.7, 1))
        chat_screen.char.friendship += delta_friendship

        if next_step:
            self.index += 1
            # ✅ CORRIGE : sauvegarde le step
            chat_screen.char.current_scene = f"{chat_screen.char.name.lower()}_step{self.index}"
            chat_screen.game.save()
            chat_screen.story.continue_scene(chat_screen)
        else:
            chat_screen.char.current_scene = "photo"
            chat_screen.game.save()
            self.final_scene(chat_screen)


    def step2_yes(self, cs): self.default_step(cs, "Oui bien sûr.", +5)
    def step2_no(self, cs): self.default_step(cs, "Non pas vraiment.", -5)
    def step3_yes(self, cs): self.default_step(cs, "Ça me rend nostalgique.", +5)
    def step3_no(self, cs): self.default_step(cs, "Ça m’est égal.", -5)
    def step4_yes(self, cs): self.default_step(cs, "Tu me la montres ?", +5)
    def step4_no(self, cs): self.default_step(cs, "Garde-la pour toi.", -5)
    def step5_yes(self, cs): self.default_step(cs, "Pourquoi ?", +5)
    def step5_no(self, cs): self.default_step(cs, "Ok je comprends.", 0)
    def step6_yes(self, cs): self.default_step(cs, "Qui ça ?", +5)
    def step6_no(self, cs): self.default_step(cs, "Laisse tomber.", -5)
    def step7_yes(self, cs): self.default_step(cs, "Tu m’en parles ?", +5)
    def step7_no(self, cs): self.default_step(cs, "Pas obligé.", -5)
    def step8_yes(self, cs): self.default_step(cs, "Il te manque ?", +5)
    def step8_no(self, cs): self.default_step(cs, "C’est la vie.", -5)
    def step9_yes(self, cs): self.default_step(cs, "C’est touchant.", +5)
    def step9_no(self, cs): self.default_step(cs, "Oublie ça.", -5)
    def step10_yes(self, cs): self.default_step(cs, "Tu joues encore ?", +5)
    def step10_no(self, cs): self.default_step(cs, "C’est cool.", 0)
    def step11_yes(self, cs): self.default_step(cs, "Tu me joueras un jour ?", +5)
    def step11_no(self, cs): self.default_step(cs, "Tu devrais arrêter.", -5)
    def step12_yes(self, cs): self.default_step(cs, "Impossible.", +5)
    def step12_no(self, cs): self.default_step(cs, "Bof.", -5)
    def step13_yes(self, cs): self.default_step(cs, "Évidemment.", +5)
    def step13_no(self, cs): self.default_step(cs, "Je plaisantais.", -5)
    def step14_yes(self, cs): self.default_step(cs, "Toujours là pour toi.", +5)
    def step14_no(self, cs): self.default_step(cs, "Bon, on change de sujet.", -5)
    def step15_yes(self, cs): self.default_step(cs, "Pareil.", +5)
    def step15_no(self, cs): self.default_step(cs, "Je dois y aller.", -5)
    def step16_yes(self, cs): self.default_step(cs, "Super !", +5)
    def step16_no(self, cs): self.default_step(cs, "C’est pas la peine.", -5)
    def step17_yes(self, cs): self.default_step(cs, "Hâte de la voir !", +5)
    def step17_no(self, cs): self.default_step(cs, "Bon… ok.", 0)
    def step18_yes(self, cs): self.default_step(cs, "Oui !", +5)
    def step18_no(self, cs): self.default_step(cs, "Non.", -5)
    def step19_yes(self, cs): self.default_step(cs, "Magnifique.", +5)
    def step19_no(self, cs): self.default_step(cs, "Mouais.", -5)
    def step20_yes(self, cs): self.default_step(cs, "Merci de le partager.", +5, next_step=False)
    def step20_no(self, cs): self.default_step(cs, "C’est trop perso.", -5, next_step=False)


    def continue_scene(self, chat_screen):
        if self.index < len(self.steps):
            question = self.steps[self.index][0]
            chat_screen.show_message(f"Alex : {question}", chat_screen.char.color)
            choices = self.get_choices(chat_screen)
            chat_screen.show_choices(choices)
        else:
            self.final_scene(chat_screen)

    def final_scene(self, chat_screen):
        chat_screen.show_message("Alex : Voilà la photo du parc...", chat_screen.char.color)
        chat_screen.show_photo(chat_screen.char.photo_path)
        chat_screen.end_story()
