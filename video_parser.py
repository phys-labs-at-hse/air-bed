import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

data_file_path = 'csv_data/friction_check.csv'
video_file_path = 'videos/friction_check.mp4'
# Notch rectangle coordinates
x1, y1, x2, y2 = 500, 165, 510, 210

vidcap = cv2.VideoCapture(video_file_path)
fps = 30
curr_nframe = 0

angles = []
nframes = []

print('Press space every time you see the metal rod passing through '
      'the rectangle')

while vidcap.isOpened():
    success, colored_frame = vidcap.read()
    if not success:
        print('Could not receive frame (stream end?). Exiting.')
        break
    curr_nframe += 1  # starting from 1

    cv2.rectangle(colored_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow('frames with notches', colored_frame)
    if cv2.waitKey(70) == ord(' '):
        if angles:
            angles.append(angles[-1] + 180)
        else:
            angles.append(0)
        nframes.append(curr_nframe)

vidcap.release()
cv2.destroyAllWindows()

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
