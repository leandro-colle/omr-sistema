from config import *

class Classification:

	def __init__(self, image_path):
		self.img_path = image_path
		self.img = cv.imread(self.img_path, 0)
		self.vocabulary_semantic = self.__get_vocabulary_semantic()
		self.sess = None
		self.classified_symbols = None

	def detect_symbols(self):
		graph = self.__get_model_default_graph()

		model_input = graph.get_tensor_by_name("model_input:0")
		seq_lengths = graph.get_tensor_by_name("seq_lengths:0")
		keep_prob = graph.get_tensor_by_name("keep_prob:0")
		input_height = graph.get_tensor_by_name("input_height:0")
		width_reduction = graph.get_tensor_by_name("width_reduction:0")
		logits = tf.get_collection("logits")[0]

		# Obtém constantes armazenadas no próprio modelo
		WIDTH_REDUCTION, HEIGHT = self.sess.run([width_reduction, input_height])

		decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_lengths)
		img = self.__normalize_image(self.img, HEIGHT)
		seq_len = [img.shape[2] / WIDTH_REDUCTION]

		prediction = self.sess.run(decoded,
			feed_dict={
				model_input: img,
				seq_lengths: seq_len,
				keep_prob: 1.0
			}
		)
		str_predictions = self.__sparse_tensor_to_strs(prediction)

		classified_symbols = []
		for w in str_predictions[0]:
			classified_symbols.append(self.vocabulary_semantic[w])

		self.classified_symbols = classified_symbols

	def calculate_accuracy(self):
		with open(self.img_path.replace('_processed.png', '.semantic'), 'r') as f:
			expected_vocabulary = f.readlines()

		vocabulary_length = len(expected_vocabulary)

		total_hits = 0
		i_expected = 0
		i_classified = 0

		while i_expected < vocabulary_length:
			i_expected += 1

			try:
				expected_word = expected_vocabulary[i_expected].rstrip()
			except IndexError:
				expected_word = ''

			while i_classified < vocabulary_length:
				i_classified += 1

				try:
					classified_word = self.classified_symbols[i_classified].rstrip()
				except IndexError:
					classified_word = ''

				if classified_word == expected_word:
					total_hits += 1

				break
		
		return {'total': total_hits, 'expected': i_expected}


	def __get_model_default_graph(self):
		tf.reset_default_graph()
		self.sess = tf.InteractiveSession()

		# Restaura os pesos
		model_path = self.__get_model_path()
		saver = tf.train.import_meta_graph(model_path)
		saver.restore(self.sess, model_path[:-5])

		return tf.get_default_graph()

	def __get_model_path(self):
		return os.path.join(BASE_DIR, 'data', 'semantic_model.meta')

	def __get_vocabulary_path(self):
		return os.path.join(BASE_DIR, 'data', 'vocabulary_semantic.txt')

	def __normalize_image(self, img, height):
		# Redimensiona a imagem
		width = int(float(height * img.shape[1]) / img.shape[0])
		img = cv.resize(img, (width, height))

		# Normaliza a imagem
		img = (255. - img) / 255.

		# Obtém uma nova forma para a imagem, sem alterar suas informações
		img = np.asarray(img).reshape(1, img.shape[0], img.shape[1], 1)

		return img

	def __sparse_tensor_to_strs(self, sparse_tensor):
		indexes = sparse_tensor[0][0]
		values = sparse_tensor[0][1]
		dense_shape = sparse_tensor[0][2]

		strs = [[] for i in range(dense_shape[0])]
		string = []
		ptr = 0
		b = 0

		for idx in range(len(indexes)):
			if indexes[idx][0] != b:
				strs[b] = string
				string = []
				b = indexes[idx][0]

			string.append(values[ptr])
			ptr = ptr + 1

		strs[b] = string
		return strs

	def __get_vocabulary_semantic(self):
		vocabulary_path = self.__get_vocabulary_path()
		vocabulary_semantic_file = open(vocabulary_path, 'r')
		vocabulary_semantic_list = vocabulary_semantic_file.read().splitlines()

		word_list = dict()
		for word in vocabulary_semantic_list:
			word_index = len(word_list)
			word_list[word_index] = word

		vocabulary_semantic_file.close()
		return word_list