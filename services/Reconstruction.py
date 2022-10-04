from config import *

class Reconstruction:

	def __init__(self, image_path, symbols):
		self.midi_file = MIDIFile(1)
		self.img_path = image_path
		self.symbols = symbols
		self.volume = 100

	def convert_to_midi(self):
		score = self.Score()

		for symbol in self.symbols:
			if symbol.startswith('clef-'):
				score.add_clef(symbol)
			elif symbol.startswith('timeSignature-'):
				score.add_time_signature(symbol)
			elif symbol.startswith('note-'):
				score.add_note(symbol)
			elif symbol.startswith('rest-'):
				score.add_rest(symbol)

		track = 0
		time = 0
		channel = 0

		self.midi_file.addTrackName(
			track,
			time,
			self.img_path.replace('_processed.png', '')
		)

		self.midi_file.addTempo(
			track,
			time,
			score.bpm
		)

		self.midi_file.addTimeSignature(
			track,
			time,
			score.time_signature[0],
			score.time_signature[1],
			24
		)

		for sound in score.melody:
			duration = 0

			if 'note' in sound:
				note = sound['note']
				self.midi_file.addNote(
					track,
					channel,
					note['pitch'],
					time,
					score.time_signature[1],
					self.volume
				)
				duration = note['duration']
			elif 'rest' in sound:
				rest = sound['rest']
				duration = rest['duration']

			time += score.time_signature[1] / duration
		
		self.__save_midi_file()

	def __save_midi_file(self):
		midi_name = self.img_path.replace('_processed.png', '.mid').split('/')[-1]
		midi_path = 'outputs/' + midi_name

		with open(midi_path, 'wb') as output_file:
			self.midi_file.writeFile(output_file)

	class Score:

		CLEFS = {
			'clef-G2': 'treble',
			'clef-F4': 'bass'
		}

		TIME_SIGNATURES = {
			'timeSignature-3/2': [3, 2],
			'timeSignature-2/4': [2, 4],
			'timeSignature-3/4': [3, 4],
			'timeSignature-4/4': [4, 4],
			'timeSignature-6/4': [6, 4],
			'timeSignature-6/8': [6, 8]
		}

		PITCHS = {
			'C': [24, 36, 48, 60, 72],
			'D': [26, 38, 50, 62, 74],
			'E': [28, 40, 52, 64, 76],
			'F': [29, 41, 53, 65, 77],
			'G': [31, 43, 55, 67, 79],
			'A': [33, 45, 57, 69, 81],
			'B': [35, 47, 59, 71, 83]
		}

		OCTAVES = [1, 2, 3, 4, 5]

		DURATIONS = {
			'whole': 1,
			'half': 2,
			'quarter': 4,
			'eighth': 8,
			'sixteenth': 16,
			'thirty_second': 32,
			'sixty_fourth': 64
		}

		DOTS = {
			'.': 1/2
		}

		def __init__(self):
			self.bpm = 120
			self.clef = None
			self.time_signature = []
			self.melody = []

		def add_clef(self, symbol):
			self.clef = self.CLEFS[symbol]

		def add_time_signature(self, symbol):
			self.time_signature = self.TIME_SIGNATURES[symbol]

		def add_note(self, symbol):
			note_params = self.__get_note_params(symbol)

			self.melody.append({
				'note': note_params
			})

		def __get_note_params(self, symbol):
			pitch = None
			octave = None
			duration = None
			increase = None

			for p in self.PITCHS:
				if p in symbol:
					pitch = p
					break

			for o in self.OCTAVES:
				if str(o) in symbol:
					octave = o
					break

			for d in self.DURATIONS:
				if d in symbol:
					duration = d
					break

			for inc in self.DOTS:
				if inc in symbol:
					increase = inc
					break

			pitch = self.PITCHS[pitch][octave-1]
			duration = self.DURATIONS[duration] + int(
				self.DURATIONS[duration] * (self.DOTS[inc] if increase else 0)
			)

			return {
				'pitch': pitch,
				'duration': duration
			}

		def add_rest(self, symbol):
			rest_params = self.__get_rest_params(symbol)

			self.melody.append({
				'rest': rest_params
			})

		def __get_rest_params(self, symbol):
			duration = None

			for d in self.DURATIONS:
				if d in symbol:
					duration = d
					break

			return {
				'duration': self.DURATIONS[duration]
			}