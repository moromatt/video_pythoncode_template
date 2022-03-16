#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate env_video_something
#read -p "Input video path: " this
#read -p "variable contour? (Y/N): " this2
python ./video_something.py --input ${this} --contour ${this2}
rundll32 user32.dll,MessageBeep
read
