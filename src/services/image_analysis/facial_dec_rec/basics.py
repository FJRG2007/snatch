from PIL import Image, ImageFile
import numpy as np, cv2, mediapipe as mp
from scipy.spatial.distance import euclidean

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Initialize Mediapipe Face Detection and Face Mesh.
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.2)

def load_image_file(file, mode="RGB"):
    im = Image.open(file)
    if mode: im = im.convert(mode)
    return np.array(im)

def face_locations(img):
    results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.detections: return []
    boxes = []
    for detection in results.detections:
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = img.shape
        x, y, w, h = (bboxC.xmin * iw, bboxC.ymin * ih, bboxC.width * iw, bboxC.height * ih)
        boxes.append((int(y), int(x + w), int(y + h), int(x)))
    return boxes

def face_landmarks(face_image):
    results = face_mesh.process(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks: return []
    landmarks = []
    for face_landmarks in results.multi_face_landmarks:
        landmarks.append({
            "nose_tip": [(landmark.x, landmark.y) for landmark in face_landmarks.landmark[1:2]],
            "left_eye": [(landmark.x, landmark.y) for landmark in face_landmarks.landmark[33:36]],
            "right_eye": [(landmark.x, landmark.y) for landmark in face_landmarks.landmark[263:266]],
        })
    return landmarks

def face_encodings(face_image):
    encodings = []
    for landmark in face_landmarks(face_image):
        encodings.append(np.array([0] * 128))
    return encodings

def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    return [distance <= tolerance for distance in [euclidean(encoding, face_encoding_to_check) for encoding in known_face_encodings]]