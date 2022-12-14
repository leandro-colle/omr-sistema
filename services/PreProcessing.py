from config import *

class PreProcessing:

	BIN_METHOD_GLOBAL = 1
	BIN_METHOD_OTSU = 2

	BLUR_METHOD_NONE = 0
	BLUR_METHOD_GAUSS = 1

	MORPH_METHODS_NONE = 0
	MORPH_METHODS_EROSION_DILATION = 1

	DEGREES_LIMIT = 15
	DEGREES_STEP = 0.25

	def __init__(self, image_path):
		self.img_path = image_path
		self.img = cv.imread(self.img_path, 0)
		self.img_sizes = self.img.shape[:2]
		self.img_sizes_center = (self.img_sizes[1] // 2, self.img_sizes[0] // 2)
		self.img_processed_path = None

	def align_staff(self, bin_method, blur_method, morphological_methods):
		best_image = self.img
		maximum_projection = 0
		rotation_scale = 1

		for degree in np.arange(-self.DEGREES_LIMIT, self.DEGREES_LIMIT, self.DEGREES_STEP):
			M = cv.getRotationMatrix2D(self.img_sizes_center, degree, rotation_scale)
			img_transformed = cv.warpAffine(self.img, M, self.img_sizes[::-1], borderValue=(255, 255, 255))

			if blur_method == self.BLUR_METHOD_GAUSS:
				img_transformed = self.__apply_gauss_filter(img_transformed)

			if bin_method == self.BIN_METHOD_GLOBAL:
				img_transformed = self.__apply_global_binarization(img_transformed)
			elif bin_method == self.BIN_METHOD_OTSU:
				img_transformed = self.__apply_otsu_binarization(img_transformed)

			if morphological_methods == self.MORPH_METHODS_EROSION_DILATION:
				img_transformed = self.__apply_morphological_operations(img_transformed)

			max_projection = self.__get_horizontal_projection(img_transformed)
			if max_projection > maximum_projection:
				best_image = img_transformed
				maximum_projection = max_projection

		self.save_img_processed(best_image)
	
	def __get_horizontal_projection(self, img):
		"""
		Obtém a soma da projeção horizontal da imagem
		- mask:
			Matriz de cor em formato binário (0 e 1)
		- dimension_index: 
			0 - Matriz é reduzida para 1 linha
			1 - Matriz é reduzida para 1 coluna

		:param img: image

		:return int max_h_projection:
		"""

		mask = np.uint8(np.where(img == 0, 1, 0))
		dimension_index = 1

		h_projection = cv.reduce(mask, dimension_index, cv.REDUCE_SUM, dtype=cv.CV_32SC1)
		return max(h_projection)

	def __apply_gauss_filter(self, img, mask = (3, 3)):
		img_filt = cv.GaussianBlur(img, mask, 0)
		return img_filt

	def __apply_global_binarization(self, img):
		ret, img_bin = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
		return img_bin

	def __apply_otsu_binarization(self, img):
		ret, img_bin = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
		return img_bin

	def __apply_morphological_operations(self, img, mask = (3, 3)):
		img_transformed = img
		kernel = np.ones(mask, np.uint8)
		img_transformed = cv.erode(img_transformed, kernel, iterations=1)
		img_transformed = cv.dilate(img_transformed, kernel, iterations=1)
		return img_transformed

	def save_img_processed(self, img):
		index = self.img_path.find('.png')
		if not index:
			index = self.img_path.find('.jpg')
		if not index:
			index = self.img_path.find('.jpeg')

		self.img_processed_path = self.img_path[:index] + '_processed' + self.img_path[index:]
		cv.imwrite(self.img_processed_path, img)