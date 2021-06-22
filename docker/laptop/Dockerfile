FROM nvidia/cuda:11.3.0-cudnn8-runtime-ubuntu18.04


ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV ROS_DISTRO melodic

###################################### user #####################################

ENV SHELL=/bin/bash \
    USER=seadrone \
    UID=1000 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

ENV HOME=/home/${USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${UID} \
    ${USER} 

RUN echo "root:root" | chpasswd
RUN echo "${USER}:111111" | chpasswd

###################################### basic tools #####################################

RUN apt-get -o Acquire::ForceIPv4=true update && apt-get -yq dist-upgrade \
    && apt-get -o Acquire::ForceIPv4=true install -yq --no-install-recommends \
    locales \
    cmake \
    make \
    git \
    vim \
    gedit \
    wget \
    sudo \
    unzip \
    gcc-8 g++-8 \
    ca-certificates \
    curl \
    ffmpeg \
    net-tools \
    dirmngr \
    gnupg2 \
    mercurial \
    python-gtk2 \
    python-gobject \
    python-tk \
    python3-pip \
    python3-dev \
    python3-opencv \
    python3-setuptools \
    python3-rospkg -y \
    lsb-release \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    libignition-math4-dev \
    libmove-base-msgs-dev \
    ruby-full \
    libopencv-core-dev \
    libopencv-highgui-dev \
    libopencv-imgproc-dev \
    libopencv-video-dev \
    libopencv-calib3d-dev \
    libopencv-features2d-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

###################################### ROS #####################################

# setup sources.list
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# setup keys
# RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 \
#     && wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add -
RUN curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xC1CF6E31E6BADE8868B172B4F42ED6FBAB17C654' | sudo apt-key add -


# install packages
RUN apt-get -o Acquire::ForceIPv4=true update && apt-get -o Acquire::ForceIPv4=true install --no-install-recommends -y \
    ros-$ROS_DISTRO-desktop-full \
    ros-$ROS_DISTRO-joy \
    ros-$ROS_DISTRO-joystick-drivers \
    ros-$ROS_DISTRO-teleop-twist-joy \
    ros-$ROS_DISTRO-rviz-imu-plugin \
    ros-$ROS_DISTRO-roslint \
    ros-$ROS_DISTRO-rosserial \
    ros-$ROS_DISTRO-rosserial-arduino \
    ros-$ROS_DISTRO-controller-manager \
    ros-$ROS_DISTRO-twist-mux \
    ros-$ROS_DISTRO-interactive-marker-twist-server \
    ros-$ROS_DISTRO-perception \
    ros-$ROS_DISTRO-rgbd-launch \
    ros-$ROS_DISTRO-robot-localization \
    ros-$ROS_DISTRO-spacenav-node \
    ros-$ROS_DISTRO-tf2-sensor-msgs \
    ros-$ROS_DISTRO-pointcloud-to-laserscan \
    ros-$ROS_DISTRO-velodyne-simulator \
    ros-$ROS_DISTRO-serial \
    ros-$ROS_DISTRO-soem \
    ros-$ROS_DISTRO-openslam-gmapping \
    ros-$ROS_DISTRO-geodesy \
    ros-$ROS_DISTRO-cartographer-* \
    ros-$ROS_DISTRO-ddynamic-reconfigure \
    ros-$ROS_DISTRO-lms1xx \
    python-rosdep \
    python-rosinstall \
    python-rosinstall-generator \
    python-wstool \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

##################################### PIP ######################################

RUN pip3 install --upgrade pip setuptools

RUN pip3 install --upgrade \
    gym \
    numpy \
    tensorflow==1.14.0 \
    gast==0.2.2 \
    matplotlib \
    pandas \
    pypozyx \
    requests \
    jupyter \
    ipykernel \
    rospkg \
    mediapipe \
    catkin-tools \
    scikit-image \
    scikit-learn \
    zerorpc \
    cython \
    lxml \
    empy  \
    opencv-python \
    opencv-contrib-python==4.2.0.34 \
    wheel \
    future \
    six==1.14.0 \
    tf_slim \
    imutils \
    scipy

RUN pip install mediapipe

####################################### procman ###########################################

RUN cd ${HOME} && git clone https://github.com/lcm-proj/lcm \
    && cd lcm \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make install

RUN cd ${HOME} && git clone https://github.com/DiaboloKiat/procman \
    && cd procman \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make install

####################################### Install bazel ###########################################

ARG BAZEL_VERSION=3.7.2
RUN cd ${HOME} && mkdir /bazel \
    && wget --no-check-certificate -O /bazel/installer.sh "https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh" \
    && wget --no-check-certificate -O  /bazel/LICENSE.txt "https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE" \
    && chmod +x /bazel/installer.sh \
    && /bazel/installer.sh \
    && rm -f /bazel/installer.sh

######################################## realsense ########################################

RUN apt-get update && apt-get install -y \
    libsuitesparse-dev\
    software-properties-common \
    libusb-1.0-0-dev \
    libx11-dev \
    xorg-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# set the version of the realsense library
ENV LIBREALSENSE_VERSION 2.36.0
RUN wget https://github.com/IntelRealSense/librealsense/archive/v${LIBREALSENSE_VERSION}.tar.gz && \
    tar -xvzf v${LIBREALSENSE_VERSION}.tar.gz && \
    rm v${LIBREALSENSE_VERSION}.tar.gz && \
    mkdir -p librealsense-${LIBREALSENSE_VERSION}/build && \
    cd librealsense-${LIBREALSENSE_VERSION}/build && \
    cmake .. && \
    make && \
    make install && \
    rm -rf librealsense-${LIBREALSENSE_VERSION}

####################################### mediapipe ###########################################

RUN cd ${HOME} && git clone https://github.com/google/mediapipe.git
    # && cd mediapipe \
    # && sed -i "s/x86_64-linux-gnu/aarch64-linux-gnu/g" third_party/opencv_linux.BUILD

##################################### Setting #####################################

RUN chown -R ${USER}:${USER} ${HOME}/
RUN echo "seadrone ALL=(ALL)  ALL" > /etc/sudoers


# Support of nvidia-docker 2.0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

# setup entrypoint
COPY ./ros_entrypoint.sh /
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]


USER ${USER}

WORKDIR ${HOME}
