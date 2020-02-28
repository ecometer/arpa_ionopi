Arpa IonoPi Tools
==========================

Setup
---------------------

  * sudo apt-get install python3-pip
  * sudo apt-get install git-core

  * mkdir -p ~/bin/pydas
  * git clone https://github.com/ecometer/arpa_ionopi.git ~/bin/pydas/
  * chmod +x ~/bin/pydas/*

  * pip3 install -r ~/bin/pydas/requirements.txt

  * python3 ~/bin/pydas/pydas.py
  * ~/bin/pydas/start_pydas.sh
  * ~/bin/pydas/stop_pydas.sh

Update Iono Lib
---------------------

  + git clone --recursive https://github.com/sfera-labs/iono-pi-c-lib.git
  + cd iono-pi-c-lib
  + sudo sh build
