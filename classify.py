class WordClassifier:
	def __init__(self, modelPath=None, model=None):
		if (model is not None):
			self.model = model
		elif (modelPath is not None):
			self.model = keras.models.load_model(modelPath)
		else:
			raise ValueError('either model or modelPath must be given')
		self.word_ids = pickle.load(open(word_id_file, 'rb'), encoding='latin1')

	def classify_image(self, image_path):
		try:
			image_pixels = convert_to_pixel_array(image_path)
			image_pixels = np.array(image_pixels)
			inp = np.array([image_pixels])
			inp = inp.reshape(inp.shape[0], 32, 100, 1)

			outp = self.model.predict(inp)[0]
			outp = np.array(outp)

			top_idx = outp.argsort()[-1:]

			top1_words = [(k, outp[v['id']]) for k, v in self.word_ids.items() if v['id'] in top_idx]
			top1_words = sorted(top1_words, key=lambda x: x[1], reverse=True)

			top1 = np.asarray(top1_words)

			if top1[0, 1].astype(np.float) < 0.5:
				top1[0, 0] = "(N/A)"

			return top1
		except FileNotFoundError:
			print('Image not found at path {}'.format(image_path))
