# scrapy-examples

A collection of scrapy examples in TOR with header and IP rotation.

To use, follow the instructions to setup tor and privoxy. These instructions are (for the most part) provided [here](https://www.khalidalnajjar.com/stealthy-crawling-using-scrapy-tor-and-privoxy/), nevertheless additional/different steps are needed to get a working installation:

## Installing and configuring Tor and Privoxy

On Ubuntu, you should be able to install it using the commands below:
```
sudo apt-get update
sudo apt-get install tor tor-geoipdb privoxy
```

### Configuring Tor

If you just want to set up tor, you don’t need to perform any edits. However, in case you’d like to be able to automatically control Tor from a script, you’d need to set the control port and password. First, generate a hash for your secure password using (replace `PASSWORDHERE` with your password):

```
tor --hash-password PASSWORDHERE
```

Next, add the following lines to the end of `/etc/tor/torrc`, while replacing `GENERATEDHASH` on the last line with the hash generated by the above command.

```
SocksPort 9050
ControlPort 9051
HashedControlPassword GENERATEDHASH
```

Finally, add the following lines at the end of `/etc/tor/torsocks.conf`.

```
AllowOutboundLocalhost 1
```
### Configuring Privoxy

Add the following lines at the end of `/etc/privoxy/config`
```
forward-socks5t / 127.0.0.1:9050 .

# Optional
keep-alive-timeout 600
default-server-timeout 600
socket-timeout 600
```

### Testing that everything works
Now that everything is configured, start the services by running:
```
sudo service privoxy start
sudo service tor start
```

Next, run the following commands
```
curl http://ifconfig.me
torify curl http://ifconfig.me
curl -x 127.0.0.1:8118 https://ifconfig.me
```

If everything works as expected, the first IP (your current IP) should be different than the second and third one.

### Running a scraper

To use a scraper, make a new virtual environment, install all dependencies, and simply run it:
```
python3 -m venv venv
source venv/bin/activate
pip install -U brotli scrapy stem random_header_generator requests[socks]
torify scrapy crawl <projectName>
```

## Available scrapers

So far (this is always a work in progress) the following scrapers are fully functional:

* quotes: https://quotes.toscrape.com/
