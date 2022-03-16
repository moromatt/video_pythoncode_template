#!/usr/bin/env python
"""video_keypoints_draw.py."""
__author__ = "amxrfe"
__copyright__ = "2022, Planet Earth"


import os
import sys
import pathlib
import argparse
import cv2 as cv
import numpy as np



def foo(img, img_path_jpg):
    """this is the fun zone"""
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.int0(corners)
    for i in corners:
        x,y = i.ravel()
        cv.circle(img,(x,y),3,255,-1)
    cv.imwrite(img_path_jpg, img)


def delete_shit(tmp_dir):
    """this funciton removes whatever is in tmp_dir that has an extention listen in ext_list_remove"""
    img_list_remove = []
    ext_list_remove = [".jpg", ".png", ".svg"]  # populate as needed
    for format in ext_list_remove:
        img_list_remove_tmp = [f for f in os.listdir(tmp_dir) if f.endswith(format)]
        img_list_remove += img_list_remove_tmp
    for rm_img in img_list_remove:
        os.remove(tmp_dir + rm_img)


def baseline(args):
    """this function creates tmp_dir and outpath_video folders wherever this script is placed"""
    video_name = "{}_output".format(pathlib.Path(args.input).stem)
    script_dir = os.path.dirname(__file__)  # directory of script
    tmp_dir = r'{}/tmp_image/'.format(script_dir)  # path to be created
    outpath_video = r'{}/output_video/'.format(script_dir)  # path to be created
    try:
        os.makedirs(tmp_dir, exist_ok=True)
        os.makedirs(outpath_video, exist_ok=True)
    except OSError:
        print("WARNING: OSError raised")
    return video_name, tmp_dir, outpath_video
    
    
def progressBar(current, total, barLength=20):
    """just a nice progress bar printed on cmd line"""
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    print("Progress: [%s%s] | Frame: %d / %d" % (arrow, spaces, current, total), end='\r')


def get_name(count_frame, size_img_counter, tmp_dir, ext_file):
    """this function gets the image name, filled with zeros, for a correct sorting"""
    number_str = str(count_frame)
    zero_filled_number = number_str.zfill(size_img_counter)
    return f"{tmp_dir}im{zero_filled_number}{ext_file}"


def main(args, video_name, tmp_dir, outpath_video):
    # img vars
    ext_file=".png"     # output tmp imgs ext
    size_img_counter=8  # number of digits during creation of tmp imgs

    # get video info: number of frames, frame rate
    video_file = cv.VideoCapture(args.input)
    total_frame = int(video_file.get(cv.CAP_PROP_FRAME_COUNT))
    frame_rate = video_file.get(cv.CAP_PROP_FPS)

    for count_frame in range(total_frame):
        _, img = video_file.read()
        img_path_jpg = get_name(count_frame, size_img_counter, tmp_dir, ext_file)
        progressBar(count_frame, total_frame)
        
        try: # here the stuff to try
            foo(img, img_path_jpg)
        except:
            print("RAISED EXCEPTION, NO VIDEO SORRY\nCLEANING DIRT AND BYE BYE\n")
            delete_shit(tmp_dir)
            os._exit(1)
            
    # if luckily everything went ok, then create video
    create_video = f"ffmpeg -y -start_number 0 -i {tmp_dir}im%0{size_img_counter}d{ext_file} -c:v libx264 -r {frame_rate} {outpath_video}_{video_name}.mp4"
    os.system(create_video)

    # fix i frame, re-encoding
    fix_frame = "ffmpeg -y -i " + outpath_video + "_" + video_name + ".mp4" + " -c:v libx264 -r " + str(frame_rate) + " " + outpath_video + video_name + ".mp4"
    os.system(fix_frame)
    
    # clean up mess
    os.remove(outpath_video + "_" + video_name + ".mp4")
    delete_shit(tmp_dir)
    print("done")


    
if __name__ == "__main__":
    # parser if necessary
    parser = argparse.ArgumentParser(description='text_keypoints_draw.py')
    parser.add_argument("-i", "--input", type=str, default="", help='input mp4 video')
    args = parser.parse_args()
    
    # get video path if not specified
    #if args.input == "":
        #args.input = input("Enter the path of your file: ") 
    
    # get temporary video for tests
    default_test_video="D:\\Users\\stuff\\my_code\\_source_video_test\\1.mp4"
    args.input = default_test_video

    while not os.path.exists(args.input) :
        print(f"I did not find the file at, {args.input}")    
        args.input = input("Path not exists! Please enter the path of your file: ") 

    # create tmp folder for tmp files, inside script folder
    video_name, tmp_dir, outpath_video = baseline(args)    

    try:
        main(args, video_name, tmp_dir, outpath_video)
    except:
        print("RAISED EXCEPTION, NO VIDEO SORRY\nCLEANING DIRT AND BYE BYE\n")
        delete_shit()
        os._exit(1)
