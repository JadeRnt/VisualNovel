class LisaStory:
    def __init__(self):
        self.steps = [
            ("Coucou ! Je viens de finir une peinture énorme !", [
                ("Je veux la voir !", self.step2_yes),
                ("Cool, c’est quoi ?", self.step2_no)
            ]),
            ("C’est un paysage marin avec des nuances roses.", [
                ("Trop beau !", self.step3_yes),
                ("Bizarre…", self.step3_no)
            ]),
            ("Tu trouves ? J’ai mis trois semaines dessus.", [
                ("Ça vaut la peine.", self.step4_yes),
                ("Tu perds ton temps.", self.step4_no)
            ]),
            ("Oh, ça me touche. Parfois je me demande si je suis faite pour ça…", [
                ("T’es hyper douée !", self.step5_yes),
                ("Tu devrais trouver un autre hobby.", self.step5_no)
            ]),
            ("Tu crois vraiment ?", [
                ("Bien sûr !", self.step6_yes),
                ("Bof…", self.step6_no)
            ]),
            ("J’aimerais exposer un jour…", [
                ("Tu devrais foncer !", self.step7_yes),
                ("Trop de stress.", self.step7_no)
            ]),
            ("Je me demande si ça intéresserait quelqu’un.", [
                ("Moi déjà !", self.step8_yes),
                ("Pas sûr.", self.step8_no)
            ]),
            ("Tu viendrais si j’exposais ?", [
                ("Évidemment !", self.step9_yes),
                ("Ça dépend.", self.step9_no)
            ]),
            ("Je peins surtout la nuit.", [
                ("T’es une artiste.", self.step10_yes),
                ("Tu dors jamais ?", self.step10_no)
            ]),
            ("La nuit, tout est plus inspirant.", [
                ("C’est beau dit comme ça.", self.step11_yes),
                ("C’est flippant.", self.step11_no)
            ]),
            ("J’écoute de la musique en même temps.", [
                ("Quel style ?", self.step12_yes),
                ("Silence, c’est mieux.", self.step12_no)
            ]),
            ("Surtout du piano.", [
                ("J’adore le piano.", self.step13_yes),
                ("Boring.", self.step13_no)
            ]),
            ("Tu joues d’un instrument ?", [
                ("Guitare.", self.step14_yes),
                ("Non, aucun.", self.step14_no)
            ]),
            ("La guitare, c’est sexy !", [
                ("Haha merci.", self.step15_yes),
                ("Pas d’accord.", self.step15_no)
            ]),
            ("Faudra qu’on fasse un duo peinture-musique.", [
                ("Grave !", self.step16_yes),
                ("Trop chelou.", self.step16_no)
            ]),
            ("Je rigole, mais ça serait marrant.", [
                ("On tente.", self.step17_yes),
                ("Non merci.", self.step17_no)
            ]),
            ("Bon… tu veux la voir ma toile ?", [
                ("OUI !", self.step18_yes),
                ("Pas spécialement.", self.step18_no)
            ]),
            ("Elle est hyper grande.", [
                ("Tant mieux.", self.step19_yes),
                ("Ça doit être moche.", self.step19_no)
            ]),
            ("Je t’envoie une photo.", [
                ("Avec plaisir.", self.step20_yes),
                ("Pas la peine.", self.step20_no)
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


    def step2_yes(self, cs): self.default_step(cs, "Je veux la voir !", +5)
    def step2_no(self, cs): self.default_step(cs, "Cool, c’est quoi ?", +3)
    def step3_yes(self, cs): self.default_step(cs, "Trop beau !", +5)
    def step3_no(self, cs): self.default_step(cs, "Bizarre…", -5)
    def step4_yes(self, cs): self.default_step(cs, "Ça vaut la peine.", +5)
    def step4_no(self, cs): self.default_step(cs, "Tu perds ton temps.", -5)
    def step5_yes(self, cs): self.default_step(cs, "T’es hyper douée !", +5)
    def step5_no(self, cs): self.default_step(cs, "Tu devrais trouver un autre hobby.", -5)
    def step6_yes(self, cs): self.default_step(cs, "Bien sûr !", +5)
    def step6_no(self, cs): self.default_step(cs, "Bof…", -5)
    def step7_yes(self, cs): self.default_step(cs, "Tu devrais foncer !", +5)
    def step7_no(self, cs): self.default_step(cs, "Trop de stress.", -5)
    def step8_yes(self, cs): self.default_step(cs, "Moi déjà !", +5)
    def step8_no(self, cs): self.default_step(cs, "Pas sûr.", -5)
    def step9_yes(self, cs): self.default_step(cs, "Évidemment !", +5)
    def step9_no(self, cs): self.default_step(cs, "Ça dépend.", -5)
    def step10_yes(self, cs): self.default_step(cs, "T’es une artiste.", +5)
    def step10_no(self, cs): self.default_step(cs, "Tu dors jamais ?", 0)
    def step11_yes(self, cs): self.default_step(cs, "C’est beau dit comme ça.", +5)
    def step11_no(self, cs): self.default_step(cs, "C’est flippant.", -5)
    def step12_yes(self, cs): self.default_step(cs, "Quel style ?", +5)
    def step12_no(self, cs): self.default_step(cs, "Silence, c’est mieux.", -5)
    def step13_yes(self, cs): self.default_step(cs, "J’adore le piano.", +5)
    def step13_no(self, cs): self.default_step(cs, "Boring.", -5)
    def step14_yes(self, cs): self.default_step(cs, "Guitare.", +5)
    def step14_no(self, cs): self.default_step(cs, "Non, aucun.", -5)
    def step15_yes(self, cs): self.default_step(cs, "Haha merci.", +5)
    def step15_no(self, cs): self.default_step(cs, "Pas d’accord.", -5)
    def step16_yes(self, cs): self.default_step(cs, "Grave !", +5)
    def step16_no(self, cs): self.default_step(cs, "Trop chelou.", -5)
    def step17_yes(self, cs): self.default_step(cs, "On tente.", +5)
    def step17_no(self, cs): self.default_step(cs, "Non merci.", -5)
    def step18_yes(self, cs): self.default_step(cs, "OUI !", +5)
    def step18_no(self, cs): self.default_step(cs, "Pas spécialement.", -5)
    def step19_yes(self, cs): self.default_step(cs, "Tant mieux.", +5)
    def step19_no(self, cs): self.default_step(cs, "Ça doit être moche.", -5)
    def step20_yes(self, cs): self.default_step(cs, "Avec plaisir.", +5, next_step=False)
    def step20_no(self, cs): self.default_step(cs, "Pas la peine.", -5, next_step=False)


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