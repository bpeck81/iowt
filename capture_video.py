import numpy as np
import cv2
import uuid
import os
from analyze_videos import *
import time
import imageio

cwd = '/home/brandon/Projects/darknet/waste_data/videos/'
vid_len = 120
inp = ''


def capture_video(num_cams, item_name, distance_name):
    vid_len = 120
    caps = [cv2.VideoCapture(i) for i in range(num_cams)]
    for cam_num in range(num_cams):
        path_name = os.path.join(cwd, 'cam_' + str(cam_num))
        if not os.path.exists(path_name):
            os.mkdir(path_name)
        path_name = os.path.join(path_name, 'dist_' + str(distance_name))
        if not os.path.exists(path_name):
            os.mkdir(path_name)

    for i in range(num_cams):
        file_names = [os.path.join(cwd, 'cam_' + str(i) + '/dist_' + distance_name + '/cam_' + str(
            i) + '-dist_' + distance_name + '-name_' + item_name + '.avi') for i in range(num_cams)]
        #gif_writers = [imageio.get_writer(fn[:-3]+'gif', mode='I') for fn in file_names]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        outs = [cv2.VideoWriter(file_names[i], fourcc, 20.0, (640, 480)) for i in range(num_cams)]
        for i in range(vid_len):
            for j in range(num_cams):
                ret, frame = caps[j].read()
                if ret == True:
                    frame = cv2.flip(frame, 1)
                    outs[j].write(frame)
                   # gif_writers[j].append_data(frame)
                else:
                    break
        for i in range(num_cams):
            outs[i].release()
            caps[i].release()
            #gif_writers[i].close()
        cv2.destroyAllWindows()
        return file_names


if __name__ == '__main__':
    setup_analyze()
    item_name = 'DEFAULT'
    distance_name = "DEFAULT"

    while inp != 'q':
        change_name = raw_input('Would you like to change item name from ' + item_name + ' (y/n)')
        if change_name == 'y':
            item_name = raw_input('Enter item name: ')
        change_distance = raw_input('Would you like to change distance name from ' + distance_name + ' (y/n)')
        if change_distance == 'y':
            distance_name = raw_input('Enter distance: ')

        saved_file_names = capture_video(3, item_name, distance_name)
        for fn in saved_file_names:
            analyze_video(fn)
        inp = raw_input('Hit enter ')
