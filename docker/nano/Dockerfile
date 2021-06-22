FROM nvcr.io/nvidia/l4t-pytorch:r32.4.2-pth1.5-py3


############################ USER ###############################
# setup environment
ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash \
    USER=seadrone \
    NB_UID=1000 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

ENV HOME=/home/${USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${USER}

RUN echo "root:root" | chpasswd
RUN echo "${USER}:111111" | chpasswd

###################################### basic tools #####################################

RUN apt-get update && apt-get install --no-install-recommends -y \
    libusb-1.0 \
    gtk+-3.0 \
    build-essential \
    make \
    cmake \
    g++ \
    tzdata \
    dirmngr \
    lsb-release \
    gnupg2 \
    libpcap-dev \
    libglfw3-dev \
    python3-pip \
    python3-opencv  \
    python3-scipy   \
    python-vcstools \
    python-scipy \
    python-gobject \
    python-gtk2 \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    libfltk1.3-dev \ 
    freeglut3-dev \ 
    libpng-dev \ 
    libjpeg-dev \
    libxft-dev \ 
    libxinerama-dev \ 
    libtiff5-dev \ 
    netbase \ 
    fluid \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

###################################### ROS #####################################

# setup keys and source.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
    echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros1-latest.list

# install ros packages
ENV ROS_DISTRO melodic
RUN apt-get update && apt-get install -y \ 
    ros-${ROS_DISTRO}-desktop-full \
    ros-$ROS_DISTRO-joy \
    ros-$ROS_DISTRO-serial \
    ros-$ROS_DISTRO-soem \
    ros-$ROS_DISTRO-openslam-gmapping \
    ros-$ROS_DISTRO-geodesy \
    ros-$ROS_DISTRO-cartographer-* \
    ros-$ROS_DISTRO-ddynamic-reconfigure \
    ros-$ROS_DISTRO-perception \
    ros-$ROS_DISTRO-rgbd-launch \
    ros-$ROS_DISTRO-joystick-drivers \
    ros-$ROS_DISTRO-pointcloud-to-laserscan \
    ros-$ROS_DISTRO-robot-localization \
    ros-$ROS_DISTRO-spacenav-node \
    ros-$ROS_DISTRO-tf2-sensor-msgs \
    ros-$ROS_DISTRO-controller-manager \
    ros-$ROS_DISTRO-twist-mux \
    ros-$ROS_DISTRO-velodyne-simulator \
    ros-$ROS_DISTRO-gazebo-ros \
    ros-$ROS_DISTRO-move-base-msgs \
    ros-$ROS_DISTRO-lms1xx \
    ros-$ROS_DISTRO-rviz-imu-plugin \
    ros-$ROS_DISTRO-interactive-marker-twist-server \
    ros-$ROS_DISTRO-teleop-twist-joy \
    ros-$ROS_DISTRO-rosserial-arduino \
    ros-$ROS_DISTRO-rosserial \
    python-rosdep \
    python-rosinstall \
    python-rosinstall-generator \
    python-wstool \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

##################################### PIP ######################################

RUN pip3 install --upgrade pip setuptools

RUN pip3 install \
    gym \
    numpy \
    --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow_gpu==1.14.0+nv19.7 \
    gast==0.2.2 \
    matplotlib \
    pandas \
    pypozyx \
    requests \
    jupyter \
    ipykernel \
    rospkg \
    catkin-tools \
    scikit-image \
    scikit-learn \
    zerorpc \
    cython \
    lxml \
    empy  \
    opencv-python \
    wheel \
    future \
    six==1.14.0 \
    tf_slim \
    imutils \
    scipy

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
RUN wget https://github.com/IntelRealSense/librealsense/archive/v${LIBREALSENSE_VERSION}.tar.gz --no-check-certificate && \
    tar -xvzf v${LIBREALSENSE_VERSION}.tar.gz && \
    rm v${LIBREALSENSE_VERSION}.tar.gz && \
    mkdir -p librealsense-${LIBREALSENSE_VERSION}/build && \
    cd librealsense-${LIBREALSENSE_VERSION}/build && \
    cmake .. && \
    make && \
    make install && \
    rm -rf librealsense-${LIBREALSENSE_VERSION}

####################################### mediapipe ###########################################

RUN cd ${HOME} && git clone https://github.com/google/mediapipe.git \
    && cd mediapipe \
    && sed -i "s/x86_64-linux-gnu/aarch64-linux-gnu/g" third_party/opencv_linux.BUILD

##################################### Setting #####################################

RUN chown -R ${USER}:${USER} ${HOME}/
RUN echo "seadrone ALL=(ALL)  ALL" > /etc/sudoers

# Support of nvidia-docker 2.0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

# setup entrypoint
COPY ./ros_entrypoint.sh /
RUN chmod 777 /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]

USER ${USER}

WORKDIR ${HOME}

