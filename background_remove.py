import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

#panel = np.zeros([100, 400], np.uint8)
panel = np.zeros([100, 700], np.uint8)
cv.namedWindow('panel')

def nothing(x):
    pass

cv.createTrackbar('L-h', 'panel', 0, 360, nothing)
cv.createTrackbar('L-s', 'panel', 0, 255, nothing)
cv.createTrackbar('L-v', 'panel', 95, 255, nothing)

cv.createTrackbar('U-h', 'panel', 360, 360, nothing)
cv.createTrackbar('U-s', 'panel', 59, 255, nothing)
cv.createTrackbar('U-v', 'panel', 255, 255, nothing)

cv.createTrackbar('S ROWS', 'panel', 0, 480, nothing)
cv.createTrackbar('E ROWS', 'panel', 480, 480, nothing)

cv.createTrackbar('S COL', 'panel', 0, 640, nothing)
cv.createTrackbar('E COL', 'panel', 640, 640, nothing)

while True:
    _, frame = cap.read()
    # print(frame.shape)

    s_r = cv.getTrackbarPos('S ROWS', 'panel')
    e_r = cv.getTrackbarPos('E ROWS', 'panel')
    s_c = cv.getTrackbarPos('S COL', 'panel')
    e_c = cv.getTrackbarPos('E COL', 'panel')

    roi = frame[s_r:e_r, s_c:e_c] # read only interest

    hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    l_odcien = cv.getTrackbarPos('L-h', 'panel')
    l_nasycenie = cv.getTrackbarPos('L-s', 'panel')
    l_wartosc_jas = cv.getTrackbarPos('L-v', 'panel')

    u_odcien = cv.getTrackbarPos('U-h', 'panel')
    u_nasycenie = cv.getTrackbarPos('U-s', 'panel')
    u_wartosc_jas = cv.getTrackbarPos('U-v', 'panel')

    lower_color = np.array([l_odcien, l_nasycenie, l_wartosc_jas])
    upper_color = np.array([u_odcien, u_nasycenie, u_wartosc_jas])

    mask = cv.inRange(hsv, lower_color, upper_color)
    mask_inv = cv.bitwise_not(mask)

    bg = cv.bitwise_and(roi, roi, mask=mask)
    fg = cv.bitwise_and(roi, roi, mask=mask_inv)

    cv.imshow(' ', fg)
    # cv.imshow('', roi)
    # cv.imshow('frame', frame)
    # cv.imshow('mask', mask)
    # cv.imshow('panel', panel)

    k = cv.waitKey(30)
    if k == 27 & 0xFF:
        break

cap.release()
cv.destroyAllWindows()
