import argparse
import os
import sys
import shutil
import cv2
from PIL import Image


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

    while True:

        success, frame = capture.read()

        if success:
            cv2.imwrite(f'{frame_dir}/frame_{frameNr}.jpg', frame)

        else:
            break

        frameNr = frameNr + 1

    capture.release()

    return len(os.listdir(frame_dir))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='Vid2Gif')
    parser.add_argument('-v', '--video', help='Path to the video file', required=True)
    parser.add_argument('-g', '--gif', help='Path to save the gif', default='converted.gif')
    parser.add_argument('-l', '--loop', default=0,
                        help='Number of times the GIF should loop (0 = infinite)')
    parser.add_argument('-d', '--duration', default=100,
                        help='Number of milliseconds to display each frame')

    args = parser.parse_args()

    # Verify video file exists
    if not os.path.isfile(args.video):
        print(f'Video file at path \'{args.video}\' does not exist.')
        sys.exit(1)

    # Verify gif file name
    gif_good = False
    if '.' in args.gif:
        tmp = args.gif.split('.')
        if tmp[-1] == 'gif':
            gif_good = True
    if not gif_good:
        print(f'GIF name \'{args.gif}\' is invalid.')
        sys.exit(1)

    # Validate loop
    loop_good = True
    if type(args.loop) == int:
        if args.loop < 0:
            loop_good = False
    elif type(args.loop) == str:
        if not args.loop.isdigit():
            loop_good = False
    else:
        print(f'Type error for loop arg ({type(args.loop)})')
        sys.exit(1)
    if not loop_good:
        print('Loop must be a natural number.')
        sys.exit(1)

    # Validate duration
    dur_good = True
    if type(args.duration) == int:
        if args.duration < 1:
            dur_good = False
    elif type(args.duration) == str:
        if not args.duration.isdigit():
            dur_good = False
    else:
        print(f'Type error for duration arg ({type(args.duration)})')
        sys.exit(1)
    if not dur_good:
        print('Duration must be a positive integer.')
        sys.exit(1)

    # Update this to be based off the file location rather than cwd
    frame_dir = os.path.join(os.getcwd(), 'tmp')

    if os.path.isdir(frame_dir):
        print('Temporary directory already exists.')
        sys.exit(1)
    else:
        os.mkdir(frame_dir)

    # Extract frames from video
    get_frames(args.video, frame_dir)

    # Make frame path template
    template = frame_dir + '/{}'

    # Setup frames
    frames = [Image.open(template.format(frame)) for frame in os.listdir(frame_dir)]

    # Save GIF
    frames[0].save(
        args.gif,
        format="GIF",
        append_images=frames[1:], # Append the rest of the frames
        save_all = True,
        duration=int(args.duration), # Milliseconds per frame
        loop=int(args.loop) # Infinite loop
    )

    # Cleanup temp frames directory
    shutil.rmtree(frame_dir)
    sys.exit(0)
