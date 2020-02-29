Arpa IonoPi Tools
==========================

Setup
---------------------

  * sudo apt-get install python3-pip
  * sudo apt-get install git-core

  * mkdir -p $HOME/bin/pydas
  * git clone https://github.com/ecometer/arpa_ionopi.git $HOME/bin/pydas/
  * chmod +x $HOME/bin/pydas/*.py
  * chmod +x $HOME/bin/pydas/*.sh

  * pip3 install -r $HOME/bin/pydas/requirements.txt

  * python3 $HOME/bin/pydas/pydas.py
  * $HOME/bin/pydas/start_pydas.sh
  * $HOME/bin/pydas/stop_pydas.sh

Update Iono Lib
---------------------

  + git clone --recursive https://github.com/sfera-labs/iono-pi-c-lib.git
  + cd iono-pi-c-lib
  + sudo sh build
