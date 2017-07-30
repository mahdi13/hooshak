# Hooshak
A social intelligent recommender in order to make your apps smarter

Thanks to [Julian McAuley, UCSD](http://cseweb.ucsd.edu/~jmcauley/), we are using Amazon rating dataset.

## Branches

### master

[![Build Status](https://travis-ci.org/mahdi13/hooshak.svg?branch=master)](https://travis-ci.org/mahdi13/hooshak)

## Installation of graph-tools

### Debian & Ubuntu

For Debian, add the following lines to your /etc/apt/sources.list,

```
deb http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION main
deb-src http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION main
```

where DISTRIBUTION can be any one of

```
stretch, sid
```

For Ubuntu, add the following lines

```
deb http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION universe
deb-src http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION universe
```

where DISTRIBUTION can be any one of

```
xenial, yakkety, zesty
```

After running apt-get update, the package can be installed with

```
apt-get install python-graph-tool
```

or if you want to use Python 3

```
apt-get install python3-graph-tool
```

If you want to verify the packages, you should use the public key 612DEFB798507F25, which can be done with the command:

```
apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25
Afterwards, you can run apt-key list, which should give you the following details about the key:

pub   4096R/98507F25 2013-10-17 [expires: 2018-10-16]
uid                  Tiago de Paula Peixoto <tiago@skewed.de>
uid                  Tiago de Paula Peixoto <t.peixoto@bath.ac.uk>
uid                  Tiago de Paula Peixoto <tiago@itp.uni-bremen.de>
sub   4096R/1A7ECE03 2013-10-17 [expires: 2018-10-16]
sub   4096R/23F08CAF 2013-10-17 [expires: 2018-10-16]
sub   4096R/52B46290 2017-03-19 [expires: 2022-03-18]
sub   4096R/EF5E8538 2017-03-19 [expires: 2022-03-18]
sub   4096R/628150AC 2017-03-19 [expires: 2022-03-18]
```

## Installation of i-graph (deprecated)

Before installing the package, you should install igraph:
```
sudo apt-get install -y libigraph0-dev
```

And run setup:
```
pip install -e .
```
