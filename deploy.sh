#!/usr/bin/env bash

projectname="webopt"
projecturl="webopt.duckdns.org"

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
# alter the SECRET_KEY
if [ ! -f ~/.secret_key ]; then
    echo "Create new salt"
	echo date +%s | sha256sum | base64 | head -c 32 > ~/.secret_key	
	chmod 700 ~/.secret_key
fi
secret_key=`cat ~.secret_key`

sed -i 's/^\(SECRET_KEY = \).*/\1$secret_key/' ~/www/$projectname/settings.py

# set `DEBUG = False`
sed -i 's/^\(DEBUG = \).*/\1True/' ~/www/$projectname/settings.py

# create or update the database ################################################
python manage.py makemigrations
python manage.py migrate

# set permissions ##############################################################
chown :www-data ~/www/db.sqlite3
chmod 774 ~/www/db.sqlite3

chown :www-data ~/www
chmod 774 ~/www

# collect static files #########################################################
cd ~/www
manage.py collectstatic


# create an apache virtualhost file ############################################
echo "<VirtualHost *:80>

	Alias /static /home/$projectname/www/static
	<Directory /home/$projectname/www/static>
		Require all granted
	</Directory>
	
	<Directory /home/$projectname/www/$projectname>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>
	
</VirtualHost>" > ~/$projecturl".conf"

