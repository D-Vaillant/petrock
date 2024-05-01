# petrock
Make your Raspberry Pi, into a pet rock. That can see.

## Developer Setup
Use poetry.

`poetry install --with=dev`

Right now we're running `llama.cpp` with `guidance` as the LLM interface. `llama.cpp` should be installed with poetry.

### Camera_setup, openCV, tensorflow lite

sudo apt install -y python3-picamera2
sudo apt install -y python3-pyqt5 python3-opengl

sudo apt-get update && sudo apt-get upgrade 

//python version 3.11.2

//i'm isolating these packages in a virtual environment for this demo

sudo apt-get install python3-pip python3-virtualenv
mkdir openCV_demo
cd openCV_demo
python3 -m pip install virtualenv
python3 -m virtualenv env
source env/bin/activate

sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev

//I am using piCamera (different if USB webcam)

sudo apt-get install python3-pip 
pip install "picamera[array]"

//now for OpenCV (made by Intel)

pip install opencv-contrib-python  //this is the full package, still light, but can be lighter

python
import cv2
cv2.__version__

//INSTALL COMPLETE! openCV v.4.9.0

## Deployment
This assumes you're using Raspbian Lite, circa 2024-05-01. Adjust parameters as you need.

First, you need poetry:
`sudo apt install python3-poetry`

Then:
`poetry install --with=pi`

Run the script in `models` to download the models.
This will set up the poetry virtual environment. To serve a WebUI, do TODO: WRITE THIS.

### Troubleshooting
Sometimes you'll run into a DBus error when trying to use `poetry`. Do this, and `source ~/.bashrc`, and things should work properly.
`echo "export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring" >> ~/.bashrc`

