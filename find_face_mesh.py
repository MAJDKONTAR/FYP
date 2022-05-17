import math
import time

import cv2
import numpy as np
import mediapipe as mp


class FaceMeshDetector:
    def __init__(self, static_mode=False, min_detection_con=0.5, min_tracking_con=0.5):
        self.i = 0
        self.blink = 0
        self.blinked = False
        self.face = []
        self.static_mode = static_mode
        self.min_detection_con = min_detection_con
        self.min_tracking_con = min_tracking_con
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=self.static_mode, min_detection_confidence=self.min_detection_con,
                                                    min_tracking_confidence=self.min_tracking_con)
        self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)

    def find_face_mesh(self, frame, draw: bool = True):
        """
        :param frame:
        :param draw:
        :return:
        """
        self.frame = frame
        self.img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.face_mesh.process(self.img_rgb)
        self.face = []
        self.ih, self.iw, self.ic = frame.shape
        if self.results.multi_face_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(frame, self.results.multi_face_landmarks[0], self.mp_face_mesh.FACEMESH_CONTOURS, self.draw_spec,
                                            self.draw_spec)
            if self.results.multi_face_landmarks[0].landmark:
                self.face = self.results.multi_face_landmarks[0].landmark

    def get_head_position(self, thresh):
        face_3d = []
        face_2d = []
        action = 'nothing'
        direction = 'center'
        for idx, lm in enumerate(self.face):
            if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                if idx == 1:
                    nose_2d = (lm.x * self.iw, lm.y * self.ih)

                x, y = int(lm.x * self.iw), int(lm.y * self.ih)
                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])
                cv2.circle(self.frame, (x, y), 2, (0, 255, 0), 2)

        if len(face_2d) > 0:
            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = 1 * self.iw

            cam_matrix = np.array([[focal_length, 0, self.ih / 2],
                                   [0, focal_length, self.iw / 2],
                                   [0, 0, 1]])

            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            _, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            rot_matrix = cv2.Rodrigues(rot_vec)[0]
            angles = cv2.RQDecomp3x3(rot_matrix)[0]

            x = angles[0] * 360
            y = angles[1] * 360

            if x < -thresh:
                action = 'forward'
                if y < -thresh:
                    direction = 'right'
                elif y > thresh:
                    direction = 'left'
                else:
                    direction = 'center'
            elif x > thresh:
                action = 'backward'
                if y < -thresh:
                    direction = 'right'
                elif y > thresh:
                    direction = 'left'
                else:
                    direction = 'center'
            else:
                action = 'nothing'
                if y < -thresh:
                    direction = 'right'
                elif y > thresh:
                    direction = 'left'
                else:
                    direction = 'center'
            print('Action:\t', action)
            print('Direction:\t', direction)
            print('\n')
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
            cv2.line(self.frame, p1, p2, (255, 0, 0), 3)
        return self.frame, {'action': action, 'direction': direction}

    def blink_detector(self, frame):
        """
        :param frame:
        :return:
        """
        if len(self.face) > 0:
            thresh = 3.7
            open = thresh - 0.3
            rh_right = (self.face[33].x, self.face[33].y)
            rh_left = (self.face[133].x, self.face[133].y)
            rv_top = (self.face[159].x, self.face[159].y)
            rv_bottom = (self.face[145].x, self.face[145].y)
            lh_right = (self.face[263].x, self.face[263].y)
            lh_left = (self.face[362].x, self.face[362].y)
            lv_top = (self.face[386].x, self.face[386].y)
            lv_bottom = (self.face[374].x, self.face[374].y)
            rh_distance = euclidean_distance(rh_right, rh_left)
            rv_distance = euclidean_distance(rv_top, rv_bottom)
            lv_distance = euclidean_distance(lv_top, lv_bottom)
            lh_distance = euclidean_distance(lh_right, lh_left)
            re_ratio = rh_distance / rv_distance
            le_ratio = lh_distance / lv_distance

            if re_ratio > thresh and le_ratio > thresh:
                if not self.blinked:
                    cv2.putText(frame, 'Blink', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 255, 0), 3)
                    self.blinked = True
                    self.blink += 1
            else:
                self.blinked = False
            # print(re_ratio, le_ratio)
        return self.blink

    def reset_blink(self):
        self.blink = 0


def euclidean_distance(rh_right, rh_left):
    """
    calculates euclidean distance between right and left points on same axis
    :param rh_right: right position
    :param rh_left: left position
    :return: distance
    """
    x, y = rh_right
    x1, y1 = rh_left
    distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return distance


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(5, 60)
    detector = FaceMeshDetector()
    start_time = time.time()
    is_motion = False
    while True:
        end_time = time.time()
        success, frame = cap.read()
        detector.find_face_mesh(frame, draw=False)
        blink = detector.blink_detector(frame)
        if is_motion:
            detector.get_head_position(5)
        if end_time - start_time >= 1:
            print('Timer reset')
            start_time = time.time()
            detector.reset_blink()
        if blink >= 2 and end_time - start_time < 1:
            if is_motion:
                print('Motion Stopped')
                is_motion = False
            else:
                print('Motion Started')
                is_motion = True
            detector.reset_blink()
            start_time = time.time()
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)
