from imutils import paths
import face_recognition
import pickle
import cv2
import os

database_path = "..\\..\\Data\\database\\train\\"

def serialize_database():
	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	image_paths = list(paths.list_files(database_path))

	# initialize the list of known encodings and known names
	known_encodings = []
	known_names = []

	# loop over the image paths
	for (i, image_path) in enumerate(image_paths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))
		name = image_path.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(image_path)
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb_image, model='hog')

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb_image, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our database
			known_encodings.append(encoding)
			known_names.append(name)

	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	data = {"encodings": known_encodings, "names": known_names}
	file = open(database_path + "encodings.pickle", "wb")
	file.write(pickle.dumps(data))
	file.close()
	print("[INFO] encodings written to %s".format(database_path + "encodings.pickle"))

serialize_database()