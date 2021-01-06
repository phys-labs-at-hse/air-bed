import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

data_file_path = 'prototype_raw_data.csv'
video_file_path = 'videos/VID_20201127_135945.mp4'

# Notch rectangle coordinates
x1, y1, x2, y2 = 280, 300, 285, 330

vidcap = cv2.VideoCapture(video_file_path)
fps = 30
curr_nframe = 0

angles = []
nframes = []

print('You will be prompted for which notch you see in the rectangle.\n'
      'Type an integer. Anything else would mean the notch was detected\n'
      'incorrectly.')

while vidcap.isOpened():
    success, colored_frame = vidcap.read()
    if not success:
        print("Can't receive frame (stream end?). Exiting.")
        break
    curr_nframe += 1  # starting from 1

    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)

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

# Write the data to the csv file
with open(data_file_path, 'w') as file:
   for i in range(len(angles)):
       file.write(f'{nframes[i]},{angles[i]}\n')

vidcap.release()
cv2.destroyAllWindows()
