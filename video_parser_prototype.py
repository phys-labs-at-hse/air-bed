import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

vidcap = cv2.VideoCapture('videos/VID_20201127_135945.mp4')
curr_nframe = 0

angles = []
nframes = []

while vidcap.isOpened():
    success, colored_frame = vidcap.read()
    if not success:
        print("Can't receive frame (stream end?). Exiting.")
        break
    curr_nframe += 1  # starting from 1

    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)

    if curr_nframe == 600:
        cv2.imwrite('figures/background.png', frame)

    x1, y1, x2, y2 = 280, 300, 285, 330
    cv2.rectangle(colored_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    if cv2.waitKey(1) == ord(' '):  # pause
        time.sleep(0.5)

    if cv2.waitKey(1) == ord('q'):  # quit
        print(curr_nframe)
        break

    # Convert image into monochrome
    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)
    # If pixel intensity is greater than 130, value set to 255, else set to 0.
    frame = cv2.threshold(frame, 130, 255, cv2.THRESH_BINARY)[1]
    # Invert colors so that notch pixels have maximal value.
    frame = cv2.bitwise_not(frame)

    if np.mean(frame[y1:y2, x1:x2]) == 255:
        cv2.imshow('frames with notches', colored_frame[100:600, 100:600])
        manual_degree = input('> ')
        try:
            manual_degree = int(manual_degree)
        except ValueError:  # notch was detected incorrectly
            continue
        angles.append(int(manual_degree))
        nframes.append(curr_nframe)

plt.scatter(nframes, angles)
plt.savefig('figures/tmp_plot.png')
with open('prototype_raw_data.csv', 'w') as file:
    assert len(angles) == len(nframes)
    for i in range(len(angles)):
        file.write(f'{nframes[i]},{angles[i]}\n')

vidcap.release()
cv2.destroyAllWindows()
