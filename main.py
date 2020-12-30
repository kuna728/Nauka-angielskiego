from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
import random

slownik = {}
plik = open('words.txt')
for line in plik:
	lista = line.split(' - ')
	lista[1] = lista[1].strip()
	slownik[lista[0]] = lista[1]
plik.close()

zleodp = {}

class MainWidget(GridLayout):
	licznik = 0
	licznik_zlych = 0
	klucz = 0
	def on_text_validate():
		print('test')
	def inicjuj(self):
		self.ids.status.max = int(self.ids.sliderslowek.value)
		self.ids.text_input.text = ''
		self.ids.opcje.visible = False
		index = random.randint(0, len(slownik)-1)
		MainWidget.klucz = list(slownik)[index]
		self.ids.mainlabel.text = slownik[MainWidget.klucz]
		canvas_color = ListProperty([1,1,1,1])

	def koncz_runde(self, dt):
		self.ids.mainlabel.color = 1, 1, 1, 1
		del slownik[MainWidget.klucz]
		if MainWidget.licznik == int(self.ids.sliderslowek.value):
			self.podsumowanie()
		else:
			index = random.randint(0, len(slownik)-1)
			MainWidget.klucz = list(slownik)[index]
			self.ids.mainlabel.text = slownik[MainWidget.klucz]

	def runda(self):
		odp = self.ids.text_input.text
		self.ids.text_input.text = ''
		klucz = MainWidget.klucz
		MainWidget.licznik+=1
		if odp != klucz:
			MainWidget.licznik_zlych+=1
			zleodp[klucz] = slownik[klucz]
			self.ids.mainlabel.color = 1, 0, 0, 1
		else:
			self.ids.mainlabel.color = 60/255, 179/255, 113/255, 1
		Clock.schedule_once(self.koncz_runde, .5)

	def podsumowanie(self):
		dobrych = MainWidget.licznik - MainWidget.licznik_zlych
		self.ids.text_input.readonly=True
		self.ids.mainlabel.text = '''KONIEC\nPoprawnych: 
		{0}\nBłednych: {1}\n Procentowo: {2}%
		'''.format(str(dobrych), str(MainWidget.licznik_zlych), str(100*dobrych/MainWidget.licznik))


class WordsApp(App):
	def build(self):
		return MainWidget()

if __name__ == "__main__":
	WordsApp().run()