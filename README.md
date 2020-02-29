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

  ° nano $HOME/bin/pydas/config.py
  * python3 $HOME/bin/pydas/pydas.py
  
  * $HOME/bin/pydas/start_pydas.sh
  * $HOME/bin/pydas/stop_pydas.sh

Update Iono Lib
---------------------

  + git clone --recursive https://github.com/sfera-labs/iono-pi-c-lib.git
  + cd iono-pi-c-lib
  + sudo sh build

  + wget -O $HOME/bin/pydas/start_pydas.sh https://raw.githubusercontent.com/ecometer/arpa_ionopi/master/start_pydas.sh


Crontab
---------------------
# run python script
@reboot /bin/sleep 120; $HOME/bin/pydas/start_pydas.sh
@reboot /bin/sleep 120; $HOME/bin/webserver/start_webapp.sh

# purge old files once per day
@daily $HOME/bin/pydas/purge_files.sh >> $HOME/bin/pydas/log/purge_files_`/bin/date +\%Y\%m`.log 2>&1
@daily $HOME/bin/webserver/purge_files.sh >> $HOME/bin/webserver/log/purge_files_/bin/date +\%Y\%m.log 2>&1
