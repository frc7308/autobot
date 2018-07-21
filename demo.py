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

_target_dist = 51.5 # Inches

while True:
    ret, im = cap.read()

    try:
        corners, ids, rejectedImgPoints = aruco.detectMarkers(im, aruco_dict)

        a0 = 0
        a1 = 0

        for corner, targetid in zip(corners, ids):
            centerX = 1280 - corner[0][0][0] - corner[0][1][0]
            relative_angle = centerX * _config_camera_angle / _config_camera_pixel_width + _camera_zero_offset

            if targetid[0] == 0:
                a1 = relative_angle
            elif targetid[0] == 1:
                a0 = relative_angle

        theta0 = a1 - a0
        theta1 = a0
        theta2 = 180 - theta0 - theta1

        c = theta2 / math.sin(math.radians(theta0))
        y = c * math.sin(math.radians(a0)) / 90 * _target_dist
        x = c * math.cos(math.radians(a0)) / 90 * _target_dist

        print "x: " + str(int(x)) + ", y: " + str(int(y))

        cv2.putText(im, "x: " + str(int(x)) + ", y: " + str(int(y)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), lineType=cv2.LINE_AA) 

#53
        aruco.drawDetectedMarkers(im, corners)
    except:
        print "Targets blocked!"

    cv2.imshow('Localization', im)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()