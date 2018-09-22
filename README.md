# automatic-ssl-renewal
Renew SSL certificate for website automatically using shell and python

SSL certificates these days are important for a website. However, SSL certificates are costly and difficult to maintain. I found one very widely used open source project that has an aim to secure the web and hence provides free SSL certificates - <b>Let's Encrypt</b>.
You can navigate to Let's Encrypt project <a href="https://letsencrypt.org/">here</a>.
The free SSL certificates come with an expiry date which is 3 months of date of issue of SSL certificate from Let's Encrypt.

The code solves the purpose of manually renewing SSL certificates every three months. You can make changes is this code according to your website and hosting and then simply create a cron job to automatically renew SSL certificates for your website without human interference.

The code is divided into two parts:

<b>1. auto_ssl_renewal.sh</b> - which is a shell script.

This shell script will take care of downloading new SSL certificate from Let's Encrypt and completing the ACME challenges required by Let's Encrypt to verify your domain. Also, this shell script will be sending you relevant emails(Success/Failure) with logs for debugging purposes.

<em>NOTE : You will need to first install certbot. You can use pip to install certbot </em>
<pre>pip install certbot</pre>
<em>certbot is expected to be run from a root user. However, this creates an issue for people using shared hosting as they won't get access to root user. The certbot command used in this script is a workaround, so that shared hosting users can generate SSL certificates with certbot.</em>

<b>2. install_ssl_cpanel.py</b> - a python script to automate certificate installation in cpanel with selenium.

This python script uses browser automation with selenium to navigate into the cpanel of your domain and log in to it. Once logged in, it will navigate to the certificate installation page and install the newly obtained SSL certificate and key. It will also verify the existing and the new SSL expiry date to check if certificate installation was successful.

<em>NOTE : You will need to install selenium library for python. Use pip to install selenium.</em>
<pre>pip install selenium</pre>
<em>This python uses PhantomJS as a browser for selenium to perform "headless" browsing. Websites usually are hosted on some unix server due to which browsers like Firefox or Chrome cannot be used by selenium. PhantomJS is a light weight browser which is perfect for this task.
Download PhantomJS <a href="http://phantomjs.org/download.html">here</a>.</em>

Create a cron job to execute <b>auto_ssl_renewal.sh</b> and let it take care of renewing your free SSL certificates :)