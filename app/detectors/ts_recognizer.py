from imutils import paths
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import imutils
import numpy as np
import pickle
import cv2
import time
import sys
import os

frame_process_size = [(192,108), (256,144), (320,180), (300,300), (426,240), (640,360), (1280,720)][3]
face_process_size = [(48,48), (72,72), (96,96)][2]
conf_threshold = .2
font = cv2.FONT_HERSHEY_DUPLEX

database_path = "..\\..\\Data\\database\\train\\"

# load our serialized face detector from disk
proto_txt = "models\\deploy.prototxt.txt"
config_file = "models\\res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(proto_txt, config_file)

# load our serialized face embedding model from disk
embedder_file = "models\\openface_nn4.small2.v1.t7"
embedder = cv2.dnn.readNetFromTorch(embedder_file)

def serialize_database():
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    image_paths = list(paths.list_files(database_path))

    # initialize the list of known encodings and known names
    known_embeddings = []
    known_names = []

    total = 0
    # loop over the image paths
    for (i, image_path) in enumerate(image_paths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{} :: {}".format(i + 1, len(image_paths), image_path))
        name = image_path.split(os.path.sep)[-2]

        image = cv2.imread(image_path)
        image = imutils.resize(image, width=600)
        h, w = image.shape[:2]

        blob = cv2.dnn.blobFromImage(cv2.resize(image, frame_process_size), 1.0, frame_process_size, (104.0, 177.0, 123.0), swapRB=False, crop=False)
        net.setInput(blob)
        detections = net.forward()
        # ensure at least one face was found
        if len(detections) > 0:
            # we're making the assumption that each image has only ONE
            # face, so find the bounding box with the largest probability
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]

            # ensure that the detection with the largest probability also
            # means our minimum probability test (thus helping filter out
            # weak detections)
            if confidence > conf_threshold:
                # compute the (x, y)-coordinates of the bounding box for
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                # the face
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI and grab the ROI dimensions
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, face_process_size, (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # add the name of the person + corresponding face
                # embedding to their respective lists
                known_names.append(name)
                known_embeddings.append(vec.flatten())
                total += 1

    # dump the facial embeddings + names to disk
    print("[INFO] serializing {} encodings...".format(total))
    data = {"embeddings": known_embeddings, "names": known_names}
    f = open(database_path + "embeddings.pickle", "wb+")
    f.write(pickle.dumps(data))
    f.close()

    # encode the labels
    print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(known_names)

    # train the model used to accept the 128-d embeddings of the face and
    # then produce the actual face recognition
    print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(known_embeddings, labels)

    # write the actual face recognition model to disk
    f = open(database_path + "recognizer.pickle", "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    f = open(database_path + "le.pickle", "wb")
    f.write(pickle.dumps(le))
    f.close()

def load_database():
    print("[INFO] loading encodings...")
    database = pickle.loads(open(database_path + "embeddings.pickle", "rb").read())

    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open(database_path + "recognizer.pickle", "rb").read())
    le = pickle.loads(open(database_path + "le.pickle", "rb").read())
    return database, recognizer, le

def process(image, data, debug=False):
    database, recognizer, le = data

    # resize the frame to have a width of 600 pixels (while
    # maintaining the aspect ratio), and then grab the image
    # dimensions
    frame = imutils.resize(image, width=600)
    (h, w) = frame.shape[:2]

    # construct a blob from the image
    image_blob = cv2.dnn.blobFromImage(cv2.resize(frame, frame_process_size), 1.0, frame_process_size, (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    net.setInput(image_blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        if confidence > conf_threshold:
            # compute the (x, y)-coordinates of the bounding box for
            # the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype("int")

            # extract the face ROI
            face = frame[y1:y2, x1:x2]
            fH, fW = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            # construct a blob for the face ROI, then pass the blob
            # through our face embedding model to obtain the 128-d
            # quantification of the face
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, face_process_size, (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            # perform classification to recognize the face
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]

            # draw the bounding box of the face along with the
            # associated probability
            text = "{}: {:.2f}%".format(name.upper(), proba * 100)
            box_color = (0, 255*proba, 255*(1-proba))
            if confidence < conf_threshold:
                box_color = (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2, 8)
            cv2.rectangle(frame, (x1, int(y1 + (y1-y2)/8)), (x2, y1), box_color, -1, 8)
            cv2.putText(frame, text, (int(x1 + (x2-x1)/40), int(y1 + (y1-y2)/40)), font, (y2-y1)/420., (255,255,255), 1)
    return frame

def recognize():
    """Detects faces present in the video source and saves the video to file"""
    data = load_database()

    source = 0
    #By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    print("[INFO] started camera...")

    cap = cv2.VideoCapture(source)

    frame_count = 0
    tt = 0
    while True:
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        t = time.time()
        out_frame = process(frame, data)
        tt += time.time() - t
        fps = frame_count / tt
        label = "FPS : {:.2f}".format(fps)
        cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        cv2.imshow("Face detection using TensorFlow", out_frame)

        if frame_count == 1:
            tt = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()

#serialize_database()

#recognize()
