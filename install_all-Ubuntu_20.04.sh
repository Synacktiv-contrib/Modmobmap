#!/usr/bin/bash

echo "[+] Installing Python3 requirements"
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install -r requirements.txt

echo "[+] Installing GNU Radio dependencies"
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt-get update
sudo apt-get install gnuradio

sudo apt install git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy \
python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev \
libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 \
liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins \
python3-zmq python3-scipy python3-gi python3-gi-cairo gobject-introspection gir1.2-gtk-3.0

echo "[+] Installing gr-osmosdr package"
sudo apt install gr-osmosdr

echo "[+] Downloading gr-gsm for Python3 and GNU Radio 3.8"
mkdir thirdparty
cd thirdparty
git clone -b maint-3.8 https://github.com/velichkov/gr-gsm.git
echo "[+] Building and installing gr-gsm for GNU Radio 3.8"
cd gr-gsm
mkdir build
cd build
cmake ../
make
sudo make install
sudo ln -s /usr/local/lib/python3/dist-packages/grgsm /usr/lib/python3/dist-packages/
sudo ln -s /usr/local/lib/x86_64-linux-gnu/libgrgsm.so.1.0.0git /usr/lib/x86_64-linux-gnu/libgrgsm.so.1.0.0git
cd ../../
echo "[+] Installing SDK tools"
sudo apt install openjdk-14-jdk
wget https://dl.google.com/android/repository/commandlinetools-linux-6609375_latest.zip
unzip commandlinetools-linux-6609375_latest.zip
sudo mkdir -p /opt/Android
cd tools
./bin/sdkmanager --sdk_root=/opt/Android --update
sudo ./bin/sdkmanager --sdk_root=/opt/Android --install platform-tools
echo "====END===="
