#!/bin/sh
echo ":: Configuring Pynitus"
echo "Pynitus directory: $1"
echo "Music library directory: $2"
echo "Server IP: $3"
echo "Server Port: $4"

echo ":: Installing required python packages"

install_python_dependencies=n
[[ -t 0 ]] &&
read -n 1 -p $"\e[1;32m
Install python dependencies? (Y/n)\e[0m " install_python_dependencies
if [[ $install_python_dependencies =~ ^(y|Y)$ ]]
then
    echo "> installing cherrypy"
    sudo pip install cherrypy

    echo "> installing jinja2"
    sudo pip install jinja2
fi

echo ":: Doing static configuration"
echo "> cd into Pynitus directory..."
cd "$1"

do_static_configuration=n
[[ -t 0 ]] &&
read -n 1 -p $"\e[1;32m
Do static configuration? (Y/n)\e[0m " do_static_configuration
if [[ $do_static_configuration =~ ^(y|Y)$ ]]
then
    sed -i 's@THEWDIR@'"$1"'@g' *.py
    sed -i 's@THEMDIR@'"$2"'@g' *.py
    sed -i 's@THEIPADDR@'"$3"'@g' *.py
    sed -i 's@THEPORT@'"$4"'@g' *.py
fi

echo ":: Starting user configuration"
username=""
userpasswd=""
admin="admin"
adminpasswd="admin"

do_user_configuration=n
[[ -t 0 ]] &&
read -n 1 -p $"\e[1;32m
Do user configuration? (Y/n)\e[0m " do_user_configuration
if [[ $do_user_configuration =~ ^(y|Y)$ ]]
then
    echo -n "Enter the admin's login name: "
    read admin

    echo -n "Enter the admin's password: "
    read adminpasswd

    echo -n "Enter the user's login name: "
    read username

    echo -n "Enter the user's password: "
    read userpasswd

    sed -i 's@THEUSER@'"$username"'@g' *.py
    sed -i 's@THEPASSWD@'"$userpasswd"'@g' *.py
    sed -i 's@THEADMINNAME@'"$admin"'@g' *.py
    sed -i 's@THEADMINPASSWD@'"$adminpasswd"'@g' *.py
fi

echo ":: Done configuring Pynitus"
echo "Please make sure the following software is installed:"
echo "* mpv"
echo "* mplayer"
