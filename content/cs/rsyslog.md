Title: Rsyslog and Letsencrypt
Tags: software, web, log
Date: 2020-10-19
Category: computer-science
Url: computer-science/rsyslog.html
slug: rsyslog.html
lang: en
translation: false
Header_Cover: cs
Headline: Secure configuration
Tags: admin-sys

# Introduction

Even if it's an hold software (started in 2004) it's still fairly used, and receiving new version.
It's also the default syslogd of some linux system.

Rsyslog receive logs from rsyslog client, which can be very usefull to backup logs or hunt bugs.

it can be used in udp, plain tcp or tcp with ssl, we will see how to setup a server
receiving syslog from many clients with tcp and ssl;

bonus we'll configure nginx to forward his log as well.

# Requirement

I'm using Debian10 with the lastest version of rsyslog (rsyslogd  8.2010.0 (aka 2020.10)), from
[OpenSuse Build
System](https://software.opensuse.org//download.html?project=home%3Argerhards&package=rsyslog),
there is a bug only present on debian10 where systemd timeout but rsyslogd has indeed (re)started.
But it has been tested on Ubuntu, Fedora and CentOS. you're alsoo gonna need to install others
packages.

The full list: `rsyslog rsyslog-ossl rsyslog-imptcp rsyslog-gnutls`

You'll need a server with a domain name pointing to it, you'll need letsencrypt (certbot) and to
generate the certificate for each server.
You'll also need the root issuer certificate. To check which is it you can use openssl.

```shell
 sudo openssl x509 -in /etc/letsencrypt/live/<domain>/chain.pem  -text -noout
Certificate:
    [...]
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: O = Digital Signature Trust Co., CN = DST Root CA X3
        Validity
            Not Before: Mar 17 16:40:46 2016 GMT
            Not After : Mar 17 16:40:46 2021 GMT

```

In this case you'll need DST Root CA X3 file, you should be able to find the issuer certificate at
[https://letsencrypt.org/certificates/](https://letsencrypt.org/certificates/) take the time to read until you find your certificate.

Right we ready to start.

# Server setup

Let's see our main configuration file, i've tried as much as possible to use the new notation.

```
$ cat /etc/rsyslog.conf

# Globals
# https://www.rsyslog.com/doc/v8-stable/rainerscript/global.html
global(
  defaultNetstreamDriver="ossl"
  defaultNetstreamDriverCAFile="/etc/letsencrypt/ca/dst-root-ca-x3.pem"
  defaultNetstreamDriverCertFile="/etc/letsencrypt/live/remote-server.example.tld/fullchain.pem"
  defaultNetstreamDriverKeyFile="/etc/letsencrypt/live/remote-server.example.tld/privkey.pem"
  workDirectory="/var/spool/rsyslog"
  preserveFQDN=on
  maxMessageSize="2k"
)

module(load="imuxsock")
module(load="imklog")

# https://www.rsyslog.com/doc/v8-stable/configuration/modules/imtcp.html
module(
  load="imtcp"
  MaxSessions="200"
  StreamDriver.Name="ossl"
  StreamDriver.Mode="1"
  StreamDriver.AuthMode="x509/fingerprint"
  PermittedPeer=["<FingerPrint Client>"]
)
input(
  type="imtcp"
  port="<PORT>"
)
include(
   file="/path/to/35-perhost.conf"
   mode="abort-if-missing"
)
include(
   file="/path/to/50-default.conf"
   mode="abort-if-missing"
)
```

On the server side we're going to use ossl module instead of gnutls (which is less accurate on error
messages.)

`PermittedPeer=["<FingerPrint Client>"]` You'll need also the fingerprint of the client certificate
you're gonna authorize (it's due to the x509/fingerprint option, which is the most recommended
authentification mode to use).

For that on the client certificate we're running the command:
```shell
 $ sudo openssl x509 -fingerprint -in /etc/letsencrypt/live/<domain_name>/fullchain.pem
SHA1 Fingerprint=<Fingerprint>
```
It should look like this into your config file `["SHA1:XX:XX:[..]:XX", "SHA1:XX:XX:[..]:XX"]`

# Per Host Config

Then in the folder `/etc/rsyslog.d` we're gonna create a file like `<priority>-<name-rule>.conf`
A good priority and name for this file could be `30-server-per-host.conf`

```
template (name="DynFile" type="string" string="/var/log/%HOSTNAME%/%syslogfacility-text%.log")
# template (name="DynNginxFile" type="string" string="/var/log/%HOSTNAME%/nginx-%programname%.log")

auth,authpriv.*         ?DynFile
cron.*                  ?DynFile
daemon.*                -?DynFile
kern.*                  ?DynFile
mail.*                  ?DynFile
user.*                  -?DynFile
# local7.*                ?DynNginxFile
```

It will simply put syslog received message in folder named after Hostname and in file named after
syslogfacility `cron.log daemon.log kern.log ...`.

If you also want to log Nginx logs uncomment both of these line, for other syslog compatible
you can inspire yourself from that.

# Default Client Configuration

There is nothing special about `rsyslog.conf`, just think to load all configuration files you're
creating, load basic module and let's start creating a file in `rsyslog.d`.

If you wish to get Nginx log to rsyslog you're gonna have to open a local rsyslog server.

Here we listen on udp, on localhost address (for Nginx if needed).
```
module(load="imudp")
input(type="imudp" address="127.0.0.1" port="1514")
```


Then it's time to forward everything to the server, in a file write down (for example
`49-remote.conf`).
```
global(
DefaultNetstreamDriver="ossl"
DefaultNetstreamDriverCAFile="/etc/ssl/ca/dst-root-ca-x3.pem"
DefaultNetstreamDriverCertFile="/etc/letsencrypt/live/client.example.tld/fullchain.pem"
DefaultNetstreamDriverKeyFile="/etc/letsencrypt/live/client.example.tld/privkey.pem"
)

action(
type="omfwd"
Target="remote-server.example.tld"
Port="124"
Protocol="tcp"
StreamDriver="ossl"
StreamDriverMode="1"
StreamDriverAuthMode="x509/fingerprint"
StreamDriverPermittedPeers="<FINGERPRINT_SERVER>"
queue.spoolDirectory="/var/log"
queue.filename="srvrfwd1"
queue.maxDiskSpace="1G"
queue.type="LinkedList"
queue.saveOnShutdown="on"
)
```

# Nginx configuration to write to syslogd

In your sites configuration for nginx you'll have to set the right configuration.
```
$ cat /etc/nginx/site-enable/default | grep log
access_log syslog:server=127.0.0.1:1514,facility=local7,tag=<TAG_NAME>,severity=info;
error_log  syslog:server=127.0.0.1:1514,facility=local7,tag=<TAG_NAME>,severity=info;
```

Note that in this configuration tag-name would end up being the filename for the log files.
` <TAG_NAME> = %programname%`


# Done

You should be able to see your logs file on the remote server.
```
lumy@server:/var/log/client$ ls
auth.log  authpriv.log  cron.log  nginx-<tag_name>.log
```

Now you can automate this process with something like [chef](https://cinc.sh) or ansible.

All documentation for rsyslog can be found on the official website:
[rsyslog documentation](https://www.rsyslog.com/doc/master/)
