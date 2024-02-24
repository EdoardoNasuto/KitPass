Packaging for android :

!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip3 install --user --upgrade Cython==0.29.33 virtualenv

!git clone https://github.com/kivy/buildozer
%cd buildozer
!python setup.py build
!pip install -e .
%cd ..

!buildozer -v android debug

!buildozer android release

Packaging for windows :

pyinstaller Kitpass.spec

Android debug :

C:\Users\edoar\desktop\platform-tools\adb.exe logcat