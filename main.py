from config import *

from services.PreProcessing import PreProcessing
from services.Classification import Classification
from services.Reconstruction import Reconstruction

def process_image(img_path, accuracy):

	"""
	Pré-processamento da imagem
	"""
	preProcessing = PreProcessing(img_path)
	preProcessing.align_staff(
		preProcessing.BLUR_METHOD_NONE,
		preProcessing.BIN_METHOD_OTSU
	)

	"""
	Classificação dos símbolos musicais
	"""
	classification = Classification(preProcessing.img_processed_path)
	classification.detect_symbols()
	hits = classification.calculate_accuracy()

	accuracy['hits'] += hits['total']
	accuracy['expected'] += hits['expected']

	"""
	Codificação da representação final
	"""
	if hits['total'] / hits['expected'] == 1:
		reconstruction = Reconstruction(
			preProcessing.img_processed_path,
			classification.classified_symbols
		)
		reconstruction.convert_to_midi()


def get_directory_images(image_dir):
	classification_images = []

	all_file_names = os.listdir(image_dir)
	for file in all_file_names:
		if '_processed' not in file and '.semantic' not in file:
			classification_images.append(file)
	
	return classification_images

def main():

	try:
		image_dir = sys.argv[1]
	except IndexError:
		print('Informe o diretório das imagens.')
		exit()	

	classification_images = get_directory_images(image_dir)

	accuracy = {'hits': 0, 'expected': 0}
	for image_name in classification_images:
		process_image(image_dir + '/' + image_name, accuracy)

	total_accuracy = round((accuracy['hits'] / accuracy['expected']) * 100, 2)
	print(total_accuracy)

if __name__ == "__main__":
	main()