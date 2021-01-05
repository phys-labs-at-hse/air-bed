import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

vidcap = cv2.VideoCapture('videos/VID_20201127_135945.mp4')
background = cv2.cvtColor(cv2.imread('figures/background.png'), cv2.COLOR_BGR2GRAY)
curr_nframe = 0

number_of_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
# Array of sums of squares or differences between current frame and the
# backgound frame
sums_of_squares = np.zeros(number_of_frames)

while vidcap.isOpened():
    success, colored_frame = vidcap.read()
    if not success:
        print("Can't receive frame (stream end?). Exiting.")
        break
    curr_nframe += 1  # starting from 1

    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)

    # Convert image into monochrome
    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)
    # Subtract the background image to see the rod (the major change)
    frame = cv2.add(frame, cv2.bitwise_not(background))

    sums_of_squares[curr_nframe - 1] = np.sum((frame - background)**2)

    if cv2.waitKey(1) == ord(' '):  # pause
        time.sleep(0.5)

    if cv2.waitKey(1) == ord('q'):  # quit
        print(curr_nframe)
        break

vidcap.release()
cv2.destroyAllWindows()

plt.scatter(range(number_of_frames), sums_of_squares)
