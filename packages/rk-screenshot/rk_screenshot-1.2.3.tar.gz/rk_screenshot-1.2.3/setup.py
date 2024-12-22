from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2.3'
DESCRIPTION = 'Screenshot using Gesture hand detection'
LONG_DESCRIPTION =  """Screenshot Capture Using Hand Gestures

This project enables users to take screenshots using hand gestures detected via a webcam. It leverages the MediaPipe library for hand detection and OpenCV for video processing. The logic uses the transition of hand gestures (from an open palm to a fist) to trigger a screenshot.

## Features

- Real-time hand gesture recognition.
- Screenshot capture when an open palm transitions to a fist gesture.
- Configurable and extensible for other gesture-based controls.
"""
# Setting up
setup(
    name="rk_screenshot",
    version=VERSION,
    author="Rohit Kumar Yadav",
    author_email="<rohitkuyadav2003@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    license="MIT",  # Add the license type here
    license_files=("LICENSE",), 
    install_requires=['pyscreenshot', 'opencv-python', 'mediapipe'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ]
)