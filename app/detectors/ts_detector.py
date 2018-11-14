from __future__ import division
import cv2
import time
import sys

box_color = (0, 255, 0)
frame_process_size = (300,300)
conf_threshold = .7

modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

def process(frame):
    """Returns the boxes list of detected faces in the @frame"""
    global net
    out_frame = frame.copy()
    height = out_frame.shape[0]
    width = out_frame.shape[1]
    #We shrink the image down to size @frame_process_size
    blob = cv2.dnn.blobFromImage(out_frame, 1.0, frame_process_size, [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            boxes.append([x1, y1, x2, y2])
            cv2.rectangle(out_frame, (x1, y1), (x2, y2), box_color, int(round(height / 150)), 8)
    return out_frame, boxes

def detect():
    """Detects faces present in the video source and save video to file"""
    source = 0
    #By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    cap = cv2.VideoCapture(source)
    has_frame, frame = cap.read()

    vid_writer = cv2.VideoWriter('video-save-{}.avi'.format(str(source).split(".")[0]), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame.shape[1], frame.shape[0]))

    frame_count = 0
    tt = 0
    while (1):
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        t = time.time()
        out_frame, boxes = process(frame)
        tt += time.time() - t
        fps = frame_count / tt
        label = "OpenCV DNN ; FPS : {:.2f}".format(fps)
        cv2.putText(out_frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow("Face Detection Comparison", out_frame)

        vid_writer.write(out_frame)
        if frame_count == 1:
            tt = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()
    vid_writer.release()