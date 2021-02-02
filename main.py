#!/usr/bin/python3.8

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import random

slownik = {}
plik = open('words.txt')
for line in plik:
	lista = line.split(' - ')
	lista[1] = lista[1].strip()
	slownik[lista[0]] = lista[1]
plik.close()

zleodp = {}
udzodp = {}

sm = ScreenManager()

class MainScreen(Screen):
	licznik = 0
	licznik_zlych = 0
	klucz = 0
	def on_text_validate():
		print('test')
	def inicjuj(self):
		global zleodp
		zleodp ={}
		MainScreen.licznik = 0 
		MainScreen.licznik_zlych=0
		MainScreen.klucz=0
		self.ids.status.max = int(self.ids.sliderslowek.value)
		self.ids.text_input.text = ''
		self.ids.opcje.visible = False
		index = random.randint(0, len(slownik)-1)
		MainScreen.klucz = list(slownik)[index]
		self.ids.mainlabel.text = slownik[MainScreen.klucz]
		canvas_color = ListProperty([1,1,1,1])

	def koncz_runde(self, dt):
		self.ids.mainlabel.color = 1, 1, 1, 1
		self.ids.mainlabel.bold = False
		del slownik[MainScreen.klucz]
		if MainScreen.licznik == int(self.ids.sliderslowek.value):
			self.ids.text_input.readonly=True
			self.ids.text_input.text = 'ustaw i zacznij wpisywać'
			self.ids.opcje.visible = True
			self.ids.mainlabel.text = ''
			self.ids.status.value = 0
			self.ids.text_input.readonly = False
			sm.get_screen('score').podsumowanie()
			sm.current = 'score'
		else:
			index = random.randint(0, len(slownik)-1)
			MainScreen.klucz = list(slownik)[index]
			self.ids.mainlabel.text = slownik[MainScreen.klucz]

	def runda(self):
		odp = self.ids.text_input.text
		self.ids.text_input.text = ''
		klucz = MainScreen.klucz
		MainScreen.licznik+=1
		self.ids.mainlabel.bold = True
		if odp != klucz:
			MainScreen.licznik_zlych+=1
			zleodp[klucz] = slownik[klucz]
			udzodp[klucz] = odp
			self.ids.mainlabel.color = 1, 0, 0, 1
		else:
			self.ids.mainlabel.color = 60/255, 179/255, 113/255, 1
		Clock.schedule_once(self.koncz_runde, .5)

class ScoreScreen(Screen):
	def podsumowanie(self):
		dobrych = MainScreen.licznik - MainScreen.licznik_zlych
		podsumowanie = '\n\n[b][size=24]KONIEC[/size][/b]\n\n[color=50f700]Poprawnych:[/color] {0}\n[color=ff3333]Blednych: [/color]{1}\n[color=d2e3ff]Procentowo: [/color]{2}%\n\n'.format(str(dobrych),
			str(MainScreen.licznik_zlych), str(100*dobrych/MainScreen.licznik)) + '\n\n[size=20]Złe odpowiedzi:[/size]\n\n'
		for i in zleodp:
			podsumowanie+= 50 * '{0} - [color=50f700]{1}[/color] / [color=ff3333]{2}[/color]\n\n'.format(zleodp[i],i,udzodp[i])
		self.ids.podsumowanie.text = podsumowanie

class WordsApp(App):
	def build(self):
		sm.add_widget(MainScreen(name='main'))
		sm.add_widget(ScoreScreen(name='score'))
		return sm

if __name__ == "__main__":
	WordsApp().run()
