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

# copy all files ###############################################################
cp -R ~/tmp/$projectname/django ~/
mv ~/django ~/www

# change values in settings.py #################################################
# ~/www/$projectname/settings.py
# alter the SECRET_KEY
if [ ! -f ~/.secret_key ]; then
    echo "Create new salt"
	echo date +%s | sha256sum | base64 | head -c 32 > ~/.secret_key	
	chmod 700 ~/.secret_key
fi
secret_key=`cat ~/.secret_key`

sed -i "s/^\(SECRET_KEY = \).*/\1'$secret_key'/" ~/www/$projectname/settings.py

# set `DEBUG = False`
sed -i "s/^\(DEBUG = \).*/\1False/" ~/www/$projectname/settings.py

# create or update the database ################################################
cd ~/www
python manage.py makemigrations
python manage.py migrate

# set permissions ##############################################################
chmod 774 ~/www/db.sqlite3
chmod 775 ~/www

# collect static files #########################################################
cd ~/www
python manage.py collectstatic


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

	WSGIDaemonProcess $projectname python-path=/home/$projectname/www:/home/$projectname/env/lib/python3.4/site-packages
	WSGIProcessGroup $projectname
	WSGIScriptAlias / /home/$projectname/www/$projectname/wsgi.py

	
</VirtualHost>" > ~/$projecturl".conf"

# deactivate the virtualenv ####################################################
# a super user still needs to be created
python manage.py createsuperuserdeactivate

deactivate

# the owners need to be set with sudo rights
# sudo chown :www-data ~/www/db.sqlite3
# sudo chown :www-data ~/www

# restart the apache server
# sudo /etc/init.d/apache2 restart
