import argparse
import os
import sys
import shutil
import cv2
from PIL import Image

TEST_VID = '/Users/bengarber/Downloads/SDH.mp4'


def get_frames(video_path: str, frame_dir: str) -> int:
    """Get frames of a video to a specified directory

    Args:
        video_path (str): Path to video file
        frame_dir (str): Path to directory to save frames

    Returns:
        int: Number of frames saved
    """

    capture = cv2.VideoCapture(video_path)

    frameNr = 0

    while (True):

        success, frame = capture.read()

        if success:
            cv2.imwrite(f'{frame_dir}/frame_{frameNr}.jpg', frame)

        else:
            break

        frameNr = frameNr + 1

    capture.release()

    return len(os.listdir(frame_dir))


if __name__ == "__main__":
    print(os.getcwd())
    print(__file__)

    # Update this to be based off the file location rather than cwd
    frame_dir = os.path.join(os.getcwd(), 'tmp')

    if os.path.isdir(frame_dir):
        print('Temporary directory already exists.')
        sys.exit(1)
    else:
        os.mkdir(frame_dir)

    # Extract frames from video
    get_frames(TEST_VID, frame_dir)
    # print(os.listdir(frame_dir))

    # Make frame path template
    template = frame_dir + '/{}'

    # Setup frames
    frames = [Image.open(template.format(frame)) for frame in os.listdir(frame_dir)]

    # Save GIF
    frames[0].save(
        "test.gif",
        format="GIF",
        append_images=frames[1:], # Append the rest of the frames
        save_all = True,
        duration=300, # 100 milliseconds per frame
        loop=0 # Infinite loop
    )

    # Cleanup temp frames directory
    shutil.rmtree(frame_dir)
    sys.exit(0)
