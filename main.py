from config import *

from services.PreProcessing import PreProcessing
from services.Classification import Classification
# from services.Reconstruction import Reconstruction

def main():

	img_name = 'primus_example.png'
	# img_name = 'camera-primus_example.png'
	# img_name = 'staff_example01.png'
	# img_name = 'staff_example02.png'

	img_path = 'images/' + img_name

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
	classified_vocabulary = classification.classified_vocabulary

	"""
	Codificação da representação final
	"""


if __name__ == "__main__":
	main()