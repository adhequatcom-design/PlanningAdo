import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout

# --- 1. LES CLASSES ---

class EcranAdo(Screen):
    def on_enter(self):
        Clock.schedule_once(self.charger_liste_visuelle, 0.1)

    def charger_liste_visuelle(self, dt):
        if 'liste_taches' in self.ids:
            self.ids.liste_taches.clear_widgets()
            app = App.get_running_app()
            donnees = app.charger_donnees()
            missions = donnees.get("missions", [])
            
            for m in missions:
                jours_noms = ["L","M","Me","J","V","S","D"]
                actifs = [jours_noms[i] for i, v in enumerate(m['jours']) if v]
                jours_str = " ".join(actifs)
                
                layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
                info = f"[b]{m['nom']}[/b]\n[color=ff69b4]{m['heure']}[/color] ({jours_str})"
                lbl = Label(text=info, markup=True, color=(0.3, 0.3, 0.3, 1), font_size=16)
                
                btn = Button(text="PHOTO 📸", size_hint_x=0.3, background_color=(1, 0.5, 0.7, 1))
                btn.bind(on_release=lambda x: self.animer_validation())
                
                layout.add_widget(lbl)
                layout.add_widget(btn)
                self.ids.liste_taches.add_widget(layout)

    def animer_validation(self):
        msg = Label(text="MAGNIFIQUE ! 💖", font_size=30, color=(1, 0.2, 0.5, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(msg)
        anim = Animation(font_size=300, opacity=0, duration=1)
        anim.bind(on_complete=lambda x, y: self.remove_widget(msg))
        anim.start(msg)

class EcranParent(Screen):
    def verifier_pass(self):
        app = App.get_running_app()
        donnees = app.charger_donnees()
        return self.ids.pass_input.text == donnees.get("password", "1234")

    def ajouter_mission_custom(self):
        if self.verifier_pass():
            nom = self.ids.nouvelle_mission.text
            heure = self.ids.heure_mission.text or "07:00"
            jours = [
                self.ids.lundi.active, self.ids.mardi.active, self.ids.mercredi.active,
                self.ids.jeudi.active, self.ids.vendredi.active, self.ids.samedi.active, self.ids.dimanche.active
            ]
            if nom:
                app = App.get_running_app()
                donnees = app.charger_donnees()
                donnees["missions"].append({"nom": nom, "heure": heure, "jours": jours})
                app.sauvegarder_donnees(donnees)
                self.ids.nouvelle_mission.text = ""
                app.root.current = "ado"
        else:
            self.ids.pass_input.hint_text = "CODE REQUIS !"

    def changer_password(self):
        if self.verifier_pass():
            nouveau = self.ids.nouveau_pass.text
            if nouveau:
                app = App.get_running_app()
                donnees = app.charger_donnees()
                donnees["password"] = nouveau
                app.sauvegarder_donnees(donnees)
                self.ids.pass_input.text = ""
                self.ids.nouveau_pass.text = ""
                self.ids.pass_input.hint_text = "Code validé !"
        else:
            self.ids.pass_input.hint_text = "MAUVAIS CODE !"

class WindowManager(ScreenManager):
    pass

# --- 2. LE DESIGN (Hyper structuré) ---

kv = """
WindowManager:
    EcranAdo:
    EcranParent:

<EcranAdo>:
    name: "ado"
    canvas.before:
        Color:
            rgba: 1, 0.96, 0.98, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        Label:
            text: "🌸 MON PLANNING 🌸"
            font_size: 24
            bold: True
            color: 0.9, 0.2, 0.5, 1
            size_hint_y: 0.1
        ScrollView:
            BoxLayout:
                id: liste_taches
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 15
        Button:
            text: "ACCÈS PAPA"
            size_hint_y: 0.08
            background_color: 0.9, 0.5, 0.7, 1
            on_release: app.root.current = "parent"

<EcranParent>:
    name: "parent"
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        
        Label:
            text: "MENU PARENT"
            font_size: 22
            color: 1, 0.6, 0.8, 1
            size_hint_y: None
            height: 40
        
        TextInput:
            id: pass_input
            hint_text: "Code actuel"
            password: True
            size_hint_y: None
            height: 45

        BoxLayout:
            spacing: 5
            size_hint_y: None
            height: 45
            TextInput:
                id: nouvelle_mission
                hint_text: "Action"
            TextInput:
                id: heure_mission
                hint_text: "07:00"
                size_hint_x: 0.3
        
        GridLayout:
            cols: 7
            size_hint_y: None
            height: 60
            Label:
                text: "L"
                color: 1, 1, 1, 1
            Label:
                text: "M"
                color: 1, 1, 1, 1
            Label:
                text: "Me"
                color: 1, 1, 1, 1
            Label:
                text: "J"
                color: 1, 1, 1, 1
            Label:
                text: "V"
                color: 1, 1, 1, 1
            Label:
                text: "S"
                color: 1, 1, 1, 1
            Label:
                text: "D"
                color: 1, 1, 1, 1
            CheckBox:
                id: lundi
                active: True
            CheckBox:
                id: mardi
                active: True
            CheckBox:
                id: mercredi
                active: True
            CheckBox:
                id: jeudi
                active: True
            CheckBox:
                id: vendredi
                active: True
            CheckBox:
                id: samedi
                active: False
            CheckBox:
                id: dimanche
                active: False
        
        Button:
            text: "ENREGISTRER LA MISSION"
            background_normal: ''
            background_color: 0.2, 0.6, 0.3, 1
            size_hint_y: None
            height: 50
            on_release: root.ajouter_mission_custom()
            
        TextInput:
            id: nouveau_pass
            hint_text: "Nouveau Code"
            size_hint_y: None
            height: 45
            
        Button:
            text: "CHANGER CODE"
            size_hint_y: None
            height: 50
            on_release: root.changer_password()
            
        Button:
            text: "RETOUR"
            background_color: 0.5, 0.5, 0.5, 1
            size_hint_y: None
            height: 40
            on_release: app.root.current = "ado"
"""

class MissionApp(App):
    def build(self):
        return Builder.load_string(kv)

    def charger_donnees(self):
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r") as f:
                    return json.load(f)
            except: pass
        return {"password": "1234", "missions": []}

    def sauvegarder_donnees(self, donnees):
        with open("data.json", "w") as f:
            json.dump(donnees, f)

if __name__ == '__main__':
    MissionApp().run()