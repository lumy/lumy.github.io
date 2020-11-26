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

Even if it is an old software (started in 2004 by [Rainer Gerhards](https://rainer.gerhards.net/))
it is still receiving new version and fairly used as it is the default [syslogd service for some linux system](https://en.wikipedia.org/wiki/Rsyslog#Distribution).

Rsyslog receive logs from syslog compatible client, usefull for monitoring.

it can be used in udp, plain tcp or tcp with ssl, we will see how to setup a server and clients with tcp and ssl using Let'sencrypt certificates;

**_bonus_** we'll configure nginx to forward his log as well.

# Requirement

I an using Debian10 with the lastest version of rsyslog (rsyslogd  8.2010.0 aka 2020.10), from
[OpenSuse Build
System](https://software.opensuse.org//download.html?project=home%3Argerhards&package=rsyslog), but
any Unix system should work.

_A bug is present on debian10_ where `systemctl` timeout but `rsyslogd` has indeed (re)started.

The packages list to install: `rsyslog rsyslog-ossl rsyslog-gnutls`

You will need a server and a client with a domain name pointing to them and certificates generated
by certbot ([letsencrypt](https://letsencrypt.org)),
and the root issuer certificate.

You will find the name of your issuer with the command `openssl`.

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

In this case you'll need `DST Root CA X3` file, you should be able to find the [issuer certificate there](https://letsencrypt.org/certificates/) take the time to read until you find your certificate.

**Right** we ready to start.

# Server setup

 The main configuration file will look like this, I tried as much as possible to use the new notation.

```
$ cat /etc/rsyslog.conf

# Globals
# https://www.rsyslog.com/doc/v8-stable/rainerscript/global.html
global(
  defaultNetstreamDriver="ossl"
  defaultNetstreamDriverCAFile="/etc/letsencrypt/ca/dst-root-ca-x3.pem"
  defaultNetstreamDriverCertFile="/etc/letsencrypt/live/remote-server.example.tld/fullchain.pem"
  defaultNetstreamDriverKeyFile="/etc/letsencrypt/live/remote-server.example.tld/privkey.pem"
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
   file="/path/to/30-per-host.conf"
   mode="abort-if-missing"
)
```

### Global options

The [global](https://www.rsyslog.com/doc/v8-stable/rainerscript/global.html) options can be changed
at your will.

- `defaultNetstreamDriver.*` this enable tls, if use it will except one of `ossl|gtls` module with
  the right ssl configuration (chain, cert and key).
- `maxMessageSize` Anything above the maximum Configured message size allowed will be truncated
  raise if your receive truncated messages.

### modules options

You will probably want to keep the `imklog` ([reads kernel log and submits them to
 syslogd](https://www.rsyslog.com/doc/v8-stable/configuration/modules/imklog.html)) and `imuxsock`
([provides the ability to accept messages via Unix sockets](https://www.rsyslog.com/doc/v8-stable/configuration/modules/imuxsock.html)) with default system configuration.

Then comes our [imtcp configuration](https://www.rsyslog.com/doc/v8-stable/configuration/modules/imtcp.html),
on the server side we are using the module `ossl` instead of `gtls` (which is less explicit on error).

- `MaxSessions` Sets the maximum number of sessions supported default. is 200 which should be enough.
- `StreamDriver.*` [ssl
  configuration](https://www.rsyslog.com/doc/v8-stable/configuration/modules/imtcp.html#streamdriver-name),
  ossl is pretty picky. I would advice to [look at the documentation before changing anything](https://www.rsyslog.com/doc/master/concepts/ns_ossl.html).
- `PermittedPeer=["<FingerPrint Client>"]` You'll need also the fingerprint of the client
  certificate you're gonna authorize. It is due to the `x509/fingerprint` option, which is the [most
  recommended authentification mode](https://www.rsyslog.com/doc/master/concepts/ns_ossl.html).

To get the Certificate Fingerprint the `openssl` command will be used.
```shell
 $ sudo openssl x509 -fingerprint -in /etc/letsencrypt/live/<domain_name>/fullchain.pem
SHA1 Fingerprint=XX:XX:XX:XX:XX
```
It should look like this in your configuration file `["SHA1:XX:XX:[..]:XX", "SHA1:XX:XX:[..]:XX"]`

### Input and Include options

- `Input` will start a server on `address` and `port`, if address is not specified it will listen on
all address.
- `Include` another configuration file.

## Per Host Config

Then in the folder `/etc/rsyslog.d`, create a new file like `<priority>-<name-rule>.conf`.
A good filename could be `30-server-per-host.conf`

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

It will simply wrote received message in folder named after `hostname` and in file named after
`facility`; if you want to gather `Nginx` logs,  remove the `#`.

### `template` options:

- `name`: template name.
- `type`: parameter specifies differents template types.
- `string`: mandatory parameter because of type string. it will specify the file to use.

[all `template` options can be found
here](https://www.rsyslog.com/doc/v8-stable/configuration/templates.html), as well as an example of
per-host template file.
You will only use template to create Dynamic File but you have to know that it can be used to
modify the content of received messages.

### `selectors` options:

- `facility.priority`: a facility here would be `cron` and a priority would be `debug` or `info` but
  `*` mean every priority [more information](https://www.rsyslog.com/doc/v8-stable/configuration/sysklogd_format.html#selectors).
- `?`: Dynamic filenames are indicated by specifying a questions mark “?” instead of a slash.
  [Follow this link for more informations on dynamic and static file](https://www.rsyslog.com/doc/v8-stable/configuration/actions.html)
- `-`: omit syncing the file after every logging.


# Client Configuration

There is nothing special about `rsyslog.conf`, just think to load all configuration files you're
creating, here's a sample.

```
global(
DefaultNetstreamDriver="ossl"
DefaultNetstreamDriverCAFile="/etc/ssl/ca/dst-root-ca-x3.pem"
DefaultNetstreamDriverCertFile="/etc/letsencrypt/live/client.example.tld/fullchain.pem"
DefaultNetstreamDriverKeyFile="/etc/letsencrypt/live/client.example.tld/privkey.pem"
preserveFQDN=on # should we preserve the FQDN (`hostname --fqdn`), you could set to `off` and use localhostname.
# localHostname="mylocalhostname" # change the hostname sent by rsyslog.

)

module(load="imuxsock")
module(load="imklog")

include(
   file="/path/to/49-remote.conf"
   mode="abort-if-missing"
)
```

## Forward configuration

Then it is time to forward everything to the server, in a file write down (for example
`49-remote.conf`).
```
action(
type="omfwd"
Target="remote-server.example.tld"
Port=<PORT>
Protocol="tcp"
StreamDriver="ossl"
StreamDriverMode="1"
StreamDriverAuthMode="x509/fingerprint"
StreamDriverPermittedPeers="<FINGERPRINT_SERVER>"
queue.spoolDirectory="/var/log"
queue.filename="srvrfwd1"
queue.maxDiskSpace="1G"
queue.type="Disk"
queue.saveOnShutdown="on"
)
```

### `action` Options

- `target,port,protocol`: It should be pointing at the server with same protocol and port value.
- `StreamDriver.*`: Client ssl configuration. `PermittedPeers` should match server certificate fingerprint.
- `queue.*`: [Queue configuration](https://www.rsyslog.com/doc/v8-stable/concepts/queues.html).
  My queue configuration is a file on the disk `/var/log/srvrfwd1.00000001` it's not the fastest,
  there's in-memory configuration available.

## *Bonus* Nginx configuration

In your site configuration you just have to set the right configuration.
```
$ cat /etc/nginx/site-enable/default | grep log
access_log syslog:server=unix:/dev/log,facility=local7,tag=<TAG_NAME>,severity=info;
error_log  syslog:server=unix:/dev/log,facility=local7,tag=<TAG_NAME>,severity=info;
```

Remember the module `imuxsock` ? Well here we are using it, forwarding our log directly to `syslogd` socket.

**Note**: In this configuration tag-name would end up being the filename for the log files.
` <TAG_NAME> = %programname%`, if you want to change that, you would have to modify the template `DynNginxFile`.

# Done

You should be able to see your log file on the remote server. After a restart of rsyslog.
You can verify the configuration file with `sudo rsyslogd -N 1 -f /etc/rsyslog.conf`.
```
lumy@server:~$ ls /var/log/<hostname>/
auth.log  authpriv.log  cron.log  nginx-<tag_name>.log
```

Now you can automate this process with something like [cinc](https://cinc.sh)/[chef](https://www.chef.io) or ansible.

All documentations for [rsyslog can be found on the official website](https://www.rsyslog.com/doc/master/)
