def convert_to_pixel_array(image_path):
	pixels = []

	im = Image.open(image_path, 'r').resize((WIDTH, HEIGHT), Image.BICUBIC).convert('L')
	pixels = list(im.getdata())

	# Normalize and zero center pixel data
	std_dev = np.std(pixels)
	img_mean = np.mean(pixels)

	pixels = [(pixels[offset:offset+WIDTH]-img_mean)/std_dev for offset in range(0, WIDTH*HEIGHT, WIDTH)]
	pixels = np.array(pixels).astype(np.float32)

	return pixels
