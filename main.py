from config import *

from services.PreProcessing import PreProcessing
from services.Classification import Classification
# from services.Reconstruction import Reconstruction

def process_image(img_path, accuracy):

	"""
	Pré-processamento da imagem
	"""
	preProcessing = PreProcessing(img_path)
	preProcessing.align_staff(
		preProcessing.BLUR_METHOD_NONE,
		preProcessing.BIN_METHOD_OTSU
	)
	img_processed_path = preProcessing.img_processed_path

	"""
	Classificação dos símbolos musicais
	"""
	classification = Classification(img_processed_path)
	classification.detect_symbols()
	total_hits = classification.calculate_accuracy()

	accuracy[0] += total_hits[0]
	accuracy[1] += total_hits[1]

	"""
	Codificação da representação final
	"""

def get_directory_images(image_dir):
	classification_images = []

	all_file_names = os.listdir(image_dir)
	for file in all_file_names:
		if '_processed' not in file and '.semantic' not in file:
			classification_images.append(file)
	
	return classification_images

def main():

	if len(sys.argv) <= 1:
		print('Informe o diretório das imagens.')
		exit()

	image_dir = sys.argv[1]

	classification_images = get_directory_images(image_dir)

	total_accuracy = 0
	expected_accuracy = 0
	accuracy = [total_accuracy, expected_accuracy]
	for image_name in classification_images:
		process_image(image_dir + '/' + image_name, accuracy)

	result_accuracy = round((accuracy[0] / accuracy[1]) * 100, 2)
	print(result_accuracy)

if __name__ == "__main__":
	main()