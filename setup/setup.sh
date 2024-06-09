#/bash
sudo apt-get install python3-pip -y

pip3 install virtualenv
virtualenv -p python3 steam_analysis_env

source steam_analysis_env/bin/activate

pip3 install -r setup/requirements.txt