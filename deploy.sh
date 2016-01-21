#!/usr/bin/env bash

projectname="webopt"
projecturl"webopt.duckdns.org"

# activate the virtualenv ######################################################
source ~/env/bin/activate

# install django ###############################################################
pip install django

# install other required packages ##############################################
# numpy
pip install numpy

# pyipopt
cd ~/tmp
git clone https://github.com/BrechtBa/pyipopt.git
cd ~/tmp/pyipopt
python setup.py install

# parsenlp
cd ~/tmp
git clone https://github.com/BrechtBa/parsenlp.git
cd ~/tmp/parsenlp
python setup.py install


# deactivate the virtualenv ####################################################
deactivate

# copy all files ###############################################################
cp  ~/tmp/$projectname/django ~/www/

# change values in settings.py #################################################
# ~/www/$projectname/settings.py
# alter the salt


# set `DEBUG = False`



# create the database ##########################################################


# set permissions ##############################################################
chown :www-data ~/www/db.sqlite3
chmod 774 ~/www/db.sqlite3

chown :www-data ~/www
chmod 774 ~/www

# collect static files #########################################################
cd ~/www
manage.py collectstatic

# create an apache virtualhost file ############################################


