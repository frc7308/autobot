import numpy as np
import cv2
import cv2.aruco as aruco
import math
 
cap = cv2.VideoCapture(0)

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters_create()

_config_camera_angle = 74
_config_camera_pixel_width = 1280
_camera_zero_offset = (180 - _config_camera_angle) / 2

_target_dist = 39 # Inches

while True:
    ret, frame = cap.read()

    im = np.zeros((650, 1000, 3), dtype=np.uint8)

    im[0:frame.shape[0], 0:frame.shape[1]] = frame

    try:
        corners, ids, rejectedImgPoints = aruco.detectMarkers(im, aruco_dict)

        if len(corners) < 2:
            print "Targets not found"
            cv2.putText(im, "Targets not found", (40, 575), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), lineType=cv2.LINE_AA) 
        else:

            a0 = 0
            a1 = 0

            for corner, targetid in zip(corners, ids):
                centerX = 1280 - corner[0][0][0] - corner[0][1][0]
                relative_angle = math.radians(centerX * _config_camera_angle / _config_camera_pixel_width + _camera_zero_offset)

                if targetid[0] == 0:
                    a1 = relative_angle
                elif targetid[0] == 1:
                    a0 = relative_angle

            theta0 = a1 - a0
            theta1 = a0
            theta2 = math.pi - theta0 - theta1

            c = theta2 / math.sin(theta0)
            y = c * math.sin(a0) / (math.pi / 2) * _target_dist
            x = c * math.cos(a0) / (math.pi / 2) * _target_dist

            print "x: " + str(x) + ", y: " + str(y)

            cv2.putText(im, "(" + str(int(x)) + ", " + str(int(y)) + ")", (40, 575), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), lineType=cv2.LINE_AA)

            xDraw = (_target_dist - int(x)) * 4 + 750
            yDraw = int(y) * 4 + 40

            cv2.rectangle(im, (730, 20), (_target_dist * 4 + 770, 500), (200, 200, 200), 3)

            cv2.circle(im, (750, 40), 4, (255, 0, 0), 8)
            cv2.circle(im, (_target_dist * 4 + 750, 40), 4, (255, 0, 0), 8)

            cv2.circle(im, (xDraw, yDraw), 4, (0, 0, 255), 8)

            cv2.line(im, (750, 40), (xDraw, yDraw), (255, 0, 255), 2)
            cv2.line(im, (_target_dist * 4 + 750, 40), (xDraw, yDraw), (255, 0, 255), 2)
            cv2.line(im, (750, 40), (_target_dist * 4 + 750, 40), (255, 0, 255), 2)

            cv2.line(im, (frame.shape[1] / 2, 0), (frame.shape[1] / 2, frame.shape[0] - 1), (255, 255, 255), 1)

            aruco.drawDetectedMarkers(im, corners)
    except:
        print "Targets not found"

    cv2.imshow('Localization', im)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()