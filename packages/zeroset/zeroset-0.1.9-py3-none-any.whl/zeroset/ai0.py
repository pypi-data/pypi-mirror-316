import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# pip install tensorflow-cpu
# pip install deepface
# pip install tf-keras
# https://github.com/serengil/deepface
# from deepface import DeepFace


import cv0
import py0
import viz0
import cv2
import numpy as np
from tqdm import tqdm


def face_test():
    model_names = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace", ]
    detector_backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    distance_metrics = ["cosine", "euclidean", "euclidean_l2"]

    filename1 = "../data/my_04.jpg"
    filename2 = "../data/my_02.jpg"

    img1 = cv0.imread(filename1)
    img2 = cv0.imread(filename2)

    results = DeepFace.verify(img1, img2,
                              model_name="Facenet",
                              detector_backend="retinaface",
                              distance_metric="cosine"
                              )

    def get_face_rect(key):
        x = results["facial_areas"][key]["x"]
        y = results["facial_areas"][key]["y"]
        w = results["facial_areas"][key]["w"]
        h = results["facial_areas"][key]["h"]
        eye_x, eye_y = results["facial_areas"][key]["left_eye"]
        return {
            "opencv": {
                "tl": (x, y),
                "br": (x + w, y + h),
            }
        }

    rect1 = get_face_rect("img1")
    rect2 = get_face_rect("img2")

    img1 = cv2.rectangle(img1, rect1["opencv"]["tl"], rect1["opencv"]["br"], (0, 255, 0), 2)
    img2 = cv2.rectangle(img2, rect2["opencv"]["tl"], rect2["opencv"]["br"], (0, 255, 0), 2)

    py0.print.print_auto(results)

    img_all = cv0.hconcat(img1, img2)
    cv0.imshow("image", img_all).waitKey()


import onnxruntime as ort


class YoloV10:
    def __init__(self, model_scale: int | str):
        model_scale_dict = {
            0: "n",
            1: "s",
            2: "m",
            3: "b",
            4: "l",
            5: "x"
        }
        if isinstance(model_scale, int):
            model_scale = model_scale_dict.get(model_scale, "m")
        self.ort_sess = ort.InferenceSession(f"yolov10/yolov10{model_scale}.onnx", providers=['CPUExecutionProvider'])

    def __call__(self, img_original, threshold=0.4):
        h, w = img_original.shape[:2]
        SIZE = 640
        w_ratio = w / SIZE
        h_ratio = h / SIZE
        img_640 = cv2.resize(img_original, (SIZE, SIZE))
        img = np.transpose(img_640, (2, 0, 1))
        img = img / 255.0
        img = np.expand_dims(img, axis=0).astype(np.float32)
        output = self.ort_sess.run(
                None,
                {'images': img},
        )
        results = []
        for e in output[0][0]:
            x1, y1, x2, y2, conf, cls = e.tolist()
            pts = [x1 * w_ratio, y1 * h_ratio, x2 * w_ratio, y2 * h_ratio]
            pts = list(map(int, pts))

            if conf > threshold:
                results.append((pts, int(cls), conf))

        return results


def yolo_test():
    ort_sess = ort.InferenceSession("yolov10/yolov10x.onnx", providers=['CPUExecutionProvider'])

    img_original = cv0.imread("C:/Users/spring/Pictures/IMG_2194.png")
    h, w = img_original.shape[:2]
    SIZE = 640
    w_ratio = w / SIZE
    h_ratio = h / SIZE
    img_640 = cv2.resize(img_original, (SIZE, SIZE))
    img = np.transpose(img_640, (2, 0, 1))
    img = img / 255.0
    img = np.expand_dims(img, axis=0).astype(np.float32)
    output = ort_sess.run(
            None,
            {'images': img},
    )
    print(output[0].shape)
    threshold = 0.4
    for e in output[0][0]:
        x1, y1, x2, y2, conf, cls = e.tolist()
        pts = [x1 * w_ratio, y1 * h_ratio, x2 * w_ratio, y2 * h_ratio]
        pts = list(map(int, pts))

        if conf > threshold:
            viz0.draw_detection(img_original, pts, viz0.get_color_by_index(int(cls)), viz0.coco_labels[int(cls)])
    cv0.imshow("result", img_original).waitKey()


def test_video():
    model = YoloV10(1)

    vc = cv2.VideoCapture(0)

    while True:
        _, img = vc.read()
        r = model(img)

        for box in r:
            cls = box[1]
            conf = box[2]
            viz0.draw_detection(img, box[0], viz0.get_color_by_index(cls), viz0.coco_labels[cls])

        if cv0.imshow("result", img).waitKey(1) == 27:
            break


if __name__ == '__main__':
    test_video()
