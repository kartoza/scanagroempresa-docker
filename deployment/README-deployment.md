# Advanced Setup Customization for local deployment

This docs serves as a devops guide to customize settings in `all.yml` file to 
suit needs of the developer. This guide assumes that you have read [Ansible Guide](deployment/ansible/README.md) 
for a general idea of the architecture.

Some knowledge that might help when reading this guide:

- How docker works
- Nginx as reverse proxy
- Haproxy as reverse proxy and load balance
- How Ansible works
- General knowledge of how HTTP works

## Motivation

This repo is able to setup and deploy locally, a mini stacks of the production 
architecture in your machine. This can be achieved by using a combination of 
docker, docker-compose configuration file, and ansible to automatically generate 
necessarry configuration from a central config file called `all.yml`

This repo uses and integrate some numbers of software stack together. 
Some of it is not hosted in this repo. Obviously, there were loads of configuration 
file involved between different software stack, to make sure they talk properly to each other.
This huge gap of different knowledge leads to a steep learning curve.

However for developers, they just want to code specific to the parts they assigned to, of course.
They don't care about other stack, unless they need to work on that too.

This repo aims to hides those complexity and store all the relevant/overrideable config, 
in a file called `all.yml`, which is just a YAML file (dictionary based). 
It is easy to understand the structure of the file and browse through which config that might interests you.

Some developers need to spin up all the stack in their machine, because they work 
to make sure these parts connect properly in production servers.

Some developers do not need to do that, or they need some specific configuration 
for themselves to test something.

This is a collective work, so each developer needs to make sure their needs were handled, 
and can be communicated easily to other developers, if they work on the same thing.

For this reason, the motivation of this guide is to store some FAQ or pointers 
on how to do some specific things related with this repo.


## FAQ

### Customizing domain names

For huge interconnected system like this, a name resolver is necessary to give a meaningful names 
for each software stack. The configuration file in `all.yml` uses domain name with `.test` TLD
to indicate that those service is going to be spin up from the local machine.

If you have name resolver setup in your machine (like dnsmasq), then things would be very easy.
Just set that all `.test` TLD will resolve to your own machine. This way, 
you have a meaningful domain name for each software stack that you use.

If you don't have those (we still recommend that you do), you can provide the 
ipaddress of your machine for each services. Obviously each software stack needs 
to know to whom they need to talk to. For example, ScanAgroempresa uses GeoNode as their auth backend.
We need to tell ScanAgroempresa the location of GeoNode URL. All settings have default value (resolved to your local machine), 
but in case you want to specify different location, just change the relevant domain name accordingly.
Let's say you want to use actual testing server over the internet, then you need to change any occurence of 
`http://geonode.test` to the actual location, like `http://testing.geonode.kartoza.com`, etc.
If you only have ipaddress, you should change it to an ipaddress, like `http://111.222.111.222`


### Customizing exposed port

As with other docker service, you can expose the port of the container to your host.
A general docker logic applies here.
The configuration section is located on `docker_port_forward` entry.
For example, in this repo, we exposed several port, because we want to test each software individually.
`scanagroempresa` have default port for ssh open in the entry, and also http. 
You can change the number as you wish. Just change the corresponding entry.

For a web container, this is a simulated reverse proxy of every service to be served as one host.
So, for one domain name, you can access different part of the stack from the url.
For example, because http port for web is exposed on port 80 by default, we can access this:
`http://scanagroempresa.test/scanagroempresa` and served a ScanAgroempresa page.
`http://scanagroempresa.test/administration` and served a GeoNode page.
`http://scanagroempresa.test/geoserver` and served a GeoServer page.

This is to simulate and test URL redirection/handling in prod server, similar with prod environment.

### Customizing credentials

You can see several variables with `USER` and `PASSWORD` on it. This is the default value for development use.
If you change any of relevant credentials, you also need to change it in the config so the service will use the correct values.

Of course this is a security risk because the credentials are stored in plain text view.
But how else are we going to share it for development use?
Always try to use strong credentials in actual deployed service on prod/testing server.

### Celery settings (GeoNode)

Some of the GeoNode services use Celery. We uses `CELERY_TASK_ALWAYS_EAGER` settings to `True` by default for dev uses and debugging purposes.
To simulate Celery with real workers setup, change it to `False`.
