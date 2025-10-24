# Vid2Gif
A tool to convert videos to GIFs

## Environment Setup
This tool includes a virtual environment to run. <br>
To setup the virtual environment, run `./setup.sh` from the top level directory of the repository. <br>
This tool can also be run outside of the virtual environment if the dependencies listed in `requirements.txt` are installed.

## Usage
### Arguments
- `-v`, `--video`: Path to the video file to convert
  - Required: True
  - Default: `None`
- `-g`, `--gif`: Path to save the gif (including the name)
  - Required: False
  - Default: `converted.gif`
- `-l`, `--loop`: Number of times the gif should loop (0 = infinite)
  - Required: False
  - Default: `0` (infinite)
- `-d`, `--duration`: Number of milliseconds to display each frame
  - Required: False
  - Default: `100`
### Example
`python vid2gif.py -v ~/Downloads/video.mp4 -g test.gif -d 300 -l 0`
