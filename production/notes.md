create user, add to sudoers, install ssh key

sudo apt-get update
sudo apt-get install nginx
sudo update-rc.d nginx defaults
sudo apt-get install git
mkdir -p /var/www
cd /var/www
git clone https://github.com/mediapublic/mediapublic.git
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/mediapublic
sudo ln -s /etc/nginx/sites-available/mediapublic /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo apt-get install python-pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper
# add virtual env stuff to bashrc, source bashrc
mkvirtualenv --python $(which python3) mediapublic
sudo chown -R gabe:gabe /var/www/mediapublic
sudo pip install -e .
pserve --daemon production.ini
