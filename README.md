# Scanagroempresa Docker Builder

This repo is used to build docker image for production server and also to
provide docker integration for local development.


What this stack includes:

- GeoNode stack as Scanagroempresa backend
- Scanagroempresa stack
- Transfer.sh stack (as big file uploader service)

# Development Setup

## Setting local environment

Clone this repo by typing one of these commands:

- `git clone https://github.com/kartoza/scanagroempresa-docker`
- `git clone git@github.com:kartoza/scanagroempresa-docker.git`

Go to the new folder: `cd scanagroempresa-docker`

Update submodules by typing these 4 commands:

- git remote update
- git submodule init
- git submodule sync
- git submodule update

Notice there is a new folder called submodules.

To use this repo locally as development environment, refer to [Ansible Guide](deployment/ansible/README.md).
The guide contains information on how the orchestration for local infrastructure works.
It contains a general idea of what is going on behind the scene to quickly setup the entire stack.

For more specific guide about customizing the setup, refer to [Advanced Setup Customization](deployment/README-deployment.md)

Note that we heavily used PyCharm to setup development environment (to Run Django, etc.)

You can run the server from pycharm by:

First, do these:

- `cd deployment/ansible/development/group_vars`
- `cp all.sample.yml all.yml`

Changes *all.yml* accordingly, particularly these fields:

- remote_user
- remote_group
- project_path

Then go to parent directory (scanagroempresa-docker).

- `cd deployment`
- `make setup-ansible`

If the configuration is correct, the server can now be started from pycharm.

Ansible setup will generate `docker-compose.override.yml` which in turn contains
services necessary for integration between services.

If you don't use pycharm, you must run `make build`.

`make up` command will start docker-compose service stack. Some of the services
were available for you to interact with:

1. `uwsgi` service contains GeoNode stack.
2. `scanagroempresa` service contains Scanagroempresa stack.

Docker-compose will start up above stack to allow SSH to it's containers. The ansible orchestration we
provided will generate PyCharm configuration files needed to run Django in DEBUG mode inside these containers.

In case you are not using PyCharm, you may run Django manually using `manage.py runserver` command.
But first, you need to go inside these containers by using SSH (for integration with IDE of your choice) or docker container shell.

Instructions below illustrate how to achieve this:

## Go inside containers using SSH

At the end of `make up` command there are two services available for SSH.

1. `uwsgi` in localhost port 63403
2. `scanagroempresa` in localhost port 63404

You can always check which ports are open for SSH (inside containers: 22),
by running `make status` command. It will lists all running services with open ports.

## Run GeoNode in Debug Mode manually

Use SSH or `make shell` to go inside `uwsgi` service container.

Run Django RunServer management command (run server for development):
```
python manage.py runserver 0.0.0.0:8080
```

If you are using the default configuration, GeoNode will be available at:
```
http://<site domain name>:63302/administration
```

With `site domain name` refer to a site domain name or ipaddress you set up at `all.yml` file.

## Run Scanagroempresa in Debug Mode manually

Use SSH or `make shell-scanagroempresa` to go inside `uwsgi` service container.

Run Django RunServer management command (run server for development):
```
python manage.py runserver 0.0.0.0:8000
```

If you are using the default configuration, Scanagroempresa will be available at:
```
http://<site domain name>:63306
```

With `site domain name` refer to a site domain name or ipaddress you set up at `all.yml` file.

# Developing custom theme

You can develop custom skin theme overrides for Scanagroempresa.
Since it is possible that there are several skin theme overrides, we didn't include
any particular skin theme in this repo. Rather you had to checkout the repo yourself.

Let's say you have a Git repository called `my_custom_theme` which
contains a django app to override themes. A typical django app may contains directory structure like this:

```
- my_custom_theme
  - models.py
  - admin.py
  - views.py
  - urls.py
  - settings.py
- .gitignore
- setup.py
- MANIFEST.in
```

You can clone this repository into `submodules` folder so these orchestration can detect it.

```
cd submodules
git clone git@github.com:lucernae/my_custom_theme.git scanagroempresa_custom_theme
```

Above command will clone your `my_custom_theme` repo and put it on a directory called `scanagroempresa_custom_theme`.
Directory name `scanagroempresa_custom_theme` are needed by the orchestration, so you had to use this name.

Your directory structures, if seen from `submodules` dir will look like:

```
- submodules
  - scanagroempresa_custom_theme
	- my_custom_theme
	  - models.py
	  - admin.py
	  - views.py
	  - urls.py
	  - settings.py
	- .gitignore
	- setup.py
	- MANIFEST.in
```

Next, you need to change `all.yml` file to tell that you used a custom theme app.
In `all.yml` file, in `scanagroempresa.environment` dict, modify these keys:

```
USE_THEME_APP: True
THEME_APP_PATH: /home/web/scanagroempresa_custom_theme
THEME_APP_NAME: my_custom_theme
```

Remember to set `THEME_APP_NAME` to the actual name of the package (what you will put in INSTALLED_APPS).
Also set `USE_THEME_APP` to boolean `True`. Then, rerun `make setup-ansible`.

Your docker-compose.override.yml file now includes settings to read these custom theme app.
