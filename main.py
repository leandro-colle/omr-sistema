from services.PreProcessing import PreProcessing
# from services.Classification import Classification
# from services.Reconstruction import Reconstruction

def main():
	img_path = 'images/'
	# img_name = 'primus_example.png'
	# img_name = 'camera-primus_example.png'
	img_name = 'staff_example01.png'
	# img_name = 'staff_example02.png'

	"""
	Pré-processamento da imagem
	"""
	preProcessing = PreProcessing(img_path + img_name)
	preProcessing.align_staff(
		preProcessing.BLUR_METHOD_NONE,
		preProcessing.BIN_METHOD_OTSU
	)

	"""
	Classificação dos símbolos musicais
	"""


	"""
	Codificação da representação final
	"""


if __name__ == "__main__":
	main()