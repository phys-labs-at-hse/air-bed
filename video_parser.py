import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

data_file_path = 'csv_data/16.csv'
video_file_path = 'videos/VID_20201127_150515.mp4'
# Notch rectangle coordinates
x1, y1, x2, y2 = 280, 485, 285, 520

# I need to rotate this video
vidcap = cv2.VideoCapture(video_file_path)
fps = 30
curr_nframe = 0

angles = []
nframes = []

print('You will be prompted for which notch you see in the rectangle.\n'
      'Type an integer. Anything else would mean the notch was detected\n'
      'incorrectly. Type drop to discard the last input.\n')

while vidcap.isOpened():
    success, colored_frame = vidcap.read()
    if not success:
        print('Could not receive frame (stream end?). Exiting.')
        break
    curr_nframe += 1  # starting from 1

    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(colored_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Convert image into monochrome
    frame = cv2.cvtColor(colored_frame, cv2.COLOR_BGR2GRAY)
    # If pixel intensity is greater than 130, value set to 255, else set to 0.
    frame = cv2.threshold(frame, 140, 255, cv2.THRESH_BINARY)[1]
    # Invert colors so that notch pixels have maximal value.
    frame = cv2.bitwise_not(frame)

    if np.mean(frame[y1:y2, x1:x2]) == 255:
        cv2.imshow('frames with notches', colored_frame[100:600, 100:600])

        manual_degree = input(f'frame {curr_nframe}> ')
        if manual_degree.count('drop') > 0 and angles and nframes:
            nframes.pop()
            angles.pop()

        try:
            manual_degree = int(manual_degree)
        except ValueError:  # notch was detected incorrectly
            continue

        if 0 <= manual_degree <= 360:
            nframes.append(curr_nframe)
            angles.append(manual_degree)
        else:
            print('Input out of bounds, be careful.')

    cv2.waitKey(1)

vidcap.release()
cv2.destroyAllWindows()

# Count full turns, add 360 degrees for each one.
# Assumes 1) the values strictly increase 2) no full turn was skipped.
# Otherwise we're in trouble.
turn = 0
for i in range(1, len(angles)):
    angles[i] += 360 * turn
    if angles[i] < angles[i - 1]:
        turn += 1
        angles[i] += 360

# Convert to physically true units
angles = list(map(lambda angle: (angle - angles[0]) / 180 * np.pi, angles))
times = list(map(lambda nframe: (nframe - nframes[0]) / fps, nframes))

# Save the plot to temporary file to check the results visually
plt.scatter(times, angles)
plt.savefig('figures/tmp_plot.png')

# Write the data to the csv file
with open(data_file_path, 'w') as file:
   for i in range(len(angles)):
       file.write(f'{times[i]},{angles[i]}\n')
