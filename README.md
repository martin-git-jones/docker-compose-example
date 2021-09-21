# mailpony SRE Challenge

**Getting Started**

You need to have rights to bind to port 80. It is suggested that this is run as *root*.

If you run SELinux, the Nginx container will show a permission denied error when trying to copy the sre.conf configuration file. Check your syslog, for example, /var/log/messages, for details on how to create and run a policy file to allow access.

From the directory where you have copied these files, run:
*docker-compose up*

It was also tested using:
*podman-compose up*

If you are presented with a choice of repositories for the images, choose docker.io.
To stop the containers, press Ctrl-C and then run:
*docker-compose down*

**Background**

This project is provided by mailpony as an SRE Challenge.
The Nginx container serves as a reverse proxy, forwarding requests on port 80 to the application container, which listens on port 4567.
*First attempt*
Networking was configured as 'host' to allow Nginx to see localhost:4567 as a port on the host and not on itself. These containers are 'sidecars' in the sense that they should be run on the same host.
*Second attempt*
I found https://docs.docker.com/compose/networking/ and reconfigured the networking to put the containers in a network called slicenet where they could communicate.
See the github commits for the difference.

The monitor container outputs the min, max and average metrics from the app to Stdout. If monitor does not receive a 200 code from Nginx, it will exit with errorlevel 1. The average is calculated without maintaining an array of all previous values in order to reduce the memory overhead.

