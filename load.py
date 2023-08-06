# Path to image dataset
image_directory = ['/content/drive/MyDrive/NCVPRIG_dataset/val']

# Name of converted dataset file
datafile = 'dataset_copy.p'
word_id_file = 'NeuralNet/word_ids.p'

# Path to text file containing 1000 words to learn, one word per line
#words = set(open('/content/drive/MyDrive/NCVPRIG_dataset/val').read().split())

directory = '/content/drive/MyDrive/NCVPRIG_dataset/'

words = set()

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            words.update(file.read().split())

def load_data():
	regexp = '[a-zA-Z]+'
	word_data = {}

	try:
		# Attempts to load data from pickle
		word_data = pickle.load(open(datafile, "rb"))
		print('data loaded from {}'.format(datafile))
	except:
		for root, dirnames, filenames in os.walk(image_directory):
			for filename in fnmatch.filter(filenames, '*.jpg'):
				fname = os.path.splitext(filename)[0]
				m = re.search(regexp, fname)
				if(m):
					word = m.group(0).lower()
					if(word in words):
						image_path = os.path.join(root, filename)
						try:
							img = convert_to_pixel_array(image_path)
							if (word not in word_data):
								word_data[word] = {}
								word_data[word]['id'] = len(word_data) - 1
								word_data[word]['points'] = []
							point = {}
							point['filename'] = filename
							point['image_path'] = image_path
							point['pixel_array'] = img
							word_data[word]['points'].append(point)
						except:
							print('image not valid: ', filename)
		# Pickle data so this process doesn't need to be repeated
		pickle.dump(word_data, open(datafile, "wb"))
		print('data saved to {}'.format(datafile))
		word_ids = word_data.copy()
		for word, data in words_ids:
			data.pop('points')
		pickle.dump(word_ids, open(word_id_file, 'wb'))

	global NUM_CLASSES
	NUM_CLASSES = len(word_data)
	return word_data
