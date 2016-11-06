#!/bin/sh

Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White


echo -e "${Purple}::${Color_Off} Configuring ${Green}Py${Color_Off}nitus"
echo -e "Pynitus directory: $1"
echo -e "Music library directory: $2"
echo -e "Server IP: $3"
echo -e "Server Port: $4"

echo -e "${Purple}::${Color_Off} Installing required python packages"

install_python_dependencies=n
[[ -t 0 ]] &&
echo -e -n "$Green Install python dependencies? (Y/n) $Color_Off"
read -n 1 install_python_dependencies

echo -e ""
if [[ $install_python_dependencies =~ ^(y|Y)$ ]]
then
    echo -e "> installing cherrypy"
    sudo pip install cherrypy

    echo -e "> installing jinja2"
    sudo pip install jinja2
fi

echo -e "${Purple}::${Color_Off} Doing static configuration"
echo -e "> cd into Pynitus directory..."
cd "$1"

do_static_configuration=n
[[ -t 0 ]] &&
echo -e -n "$Green Do static configuration? (Y/n) $Color_Off"
read -n 1 do_static_configuration

echo -e ""
if [[ $do_static_configuration =~ ^(y|Y)$ ]]
then
    sed -i 's@THEWDIR@'"${1%/}"'@g' *.py
    sed -i 's@THEMDIR@'"${2%/}"'@g' *.py
    sed -i 's@THEIPADDR@'"$3"'@g' *.py
    sed -i 's@THEPORT@'"$4"'@g' *.py
fi

echo -e "${Purple}::${Color_Off} Starting user configuration"
username=""
userpasswd=""
admin="admin"
adminpasswd="admin"

do_user_configuration=n
[[ -t 0 ]] &&
echo -e -n "$Green Do user configuration? (Y/n) $Color_Off"
read -n 1 do_user_configuration

echo -e ""
if [[ $do_user_configuration =~ ^(y|Y)$ ]]
then
    echo -e -n "Enter the admin's login name: "
    read -e admin

    echo -e -n "Enter the admin's password: "
    read -e adminpasswd

    echo -e -n "Enter the user's login name: "
    read -e username

    echo -e -n "Enter the user's password: "
    read -e userpasswd

    sed -i 's@THEUSER@'"$username"'@g' *.py
    sed -i 's@THEPASSWD@'"$userpasswd"'@g' *.py
    sed -i 's@THEADMINNAME@'"$admin"'@g' *.py
    sed -i 's@THEADMINPASSWD@'"$adminpasswd"'@g' *.py
fi

echo -e "${Purple}::${Color_Off} Done configuring Pynitus"
echo -e "Please make sure the following software is installed:"
echo -e "${Blue}*${Color_Off} mpv"
echo -e "${Blue}*${Color_Off} mplayer"
