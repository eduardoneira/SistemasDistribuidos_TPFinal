#!/bin/bash

# 1. INSTALL THE DEPENDENCIES

dnf install -y cmake
dnf install -y python-devel numpy python3-devel
dnf install -y gcc gcc-c++

dnf install -y gtk2-devel
dnf install -y libdc1394-devel
dnf install -y libv4l-devel
dnf install -y gstreamer-plugins-base-devel

dnf install -y libpng-devel
dnf install -y libjpeg-turbo-devel
dnf install -y jasper-devel
dnf install -y openexr-devel
dnf install -y libtiff-devel
dnf install -y libwebp-devel

dnf install -y tbb-devel
dnf install -y eigen3-devel
dnf install -y doxygen


# 2. INSTALL THE LIBRARY (YOU CAN CHANGE '3.2.0' FOR THE LAST STABLE VERSION)

mkdir OpenCV
cd OpenCV

git clone https://github.com/Itseez/opencv.git

git clone https://github.com/opencv/opencv_contrib.git

mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local .. -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 ../opencv
make -j4
sudo make install