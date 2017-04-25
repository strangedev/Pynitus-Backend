Pynitus
======

_...who's doing the music?_
Everyone is. Meet Pynitus, the collaborative music playlist, where anyone can join in.

What is Pynitus?
----------------------

With Pynitus, you can hook up your PC to any sound system, and let the crowd take control.
Using the Mobile Web App, anyone in your network can upload their music to Pynitus, browse your Pynitus Library and vote on what's playing next.

> **Work in Progress!**

> We're currently still building Pynitus. 
> However, you can already get the Development version of it, [and here's how.](https://github.com/Pynitus-Universe/Pynitus-Backend#getting-pynitus)


Easy to use
---------------

With the Mobile Web App, anyone can join.

The Pynitus Mobile Web App runs in your browser and requires no installation. Just share your Pynitus URL with anyone you want to join in and sit back.

With the Mobile Web App, your guests can browse your Pynitus Library, upload new Music to it, create their own playlists and vote to skip a track, if they don't like it.

Easy to set up
------------------

Pynitus will be available as a container, possibly a snap package.



Flexible
----------

Pynitus is built on top of [tinnitus](https://github.com/strangedev/tinnitus), an extendable media player service.
Because tinnitus is easy to extend, Pynitus can be extended to support _any_ source of music, from MP3s to streaming services and beyond.

With the built-in permission management, you can take control over what your guest are allowed to do, right within the App.


Getting Pynitus
---------------------

## Prerequisites

Pynitus works on Unixoid Systems, like GNU/Linux, BSD and Mac OS. There is no support for Windows at the moment.

First of all, you have to install the prerequisites _memcached_, _virtualenv_ and _taglib_.

### Mac OS

Get [homebrew](https://brew.sh/).

```
brew install memcached

brew install taglib
```

### GNU/Linux

[memcached installation instructions](https://github.com/memcached/memcached/wiki/Install)

For installing taglib, please see the documentation for your OS's package management system. The source can be found [here.](https://github.com/taglib/taglib)


## Installing Pynitus

To get Pynitus, you need to clone the [Pynitus_Backend](https://github.com/Pynitus-Universe/Pynitus-Backend) repository.
The repository contains a bootstrapping script to get Pynitus up and running:

```
# Clone the repository
git clone https://github.com/Pynitus-Universe/Pynitus-Backend.git

cd Pynitus_Backend

# Run the server
./pynitus.sh
```

Also, make sure tinnitusd is running on your system:

```
# Pynitus installs itself and tinntius to a virtualenv.
# Activate the virtualenv

. .pynitus_venv/bin/activate

# Run tinnitusd

tinnitusd

```

