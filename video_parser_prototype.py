import numpy as np
import cv2
import time

vidcap = cv2.VideoCapture('videos/VID_20201127_135945.mp4')
curr_nframe = 0

while vidcap.isOpened():
    success, colored_frame = vidcap.read()
    if not success:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    curr_nframe += 1  # starting from 1

    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)

    if curr_nframe == 600:
        cv2.imwrite('figures/background.png', frame)

    x1, y1, x2, y2 = 270, 330, 280, 340
    cv2.rectangle(colored_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    print(np.mean(frame[x1:x2, y2:y2]))

    if cv2.waitKey(1) == ord(' '):
        time.sleep(0.5)

    if cv2.waitKey(1) == ord('q'):
        print(curr_nframe)
        break

    # cv2.imshow('B&W frames', frame)
    cv2.imshow('colored frames', colored_frame)

vidcap.release()
cv2.destroyAllWindows()
