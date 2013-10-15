# NullNet

## Overview
NullNet is a p2p based, distributed, simple API for a message board. It was built for those that want private, underground, simple, communication network.

## Goals
- Distributed Article Indexes
- Distributed Articles + Comments
- Ability to gnupg/sign articles
- Ability to hash or obfuscate articles within a network (stage 2)
- Simple Python API for creating clients.

## Implementation

### Networks
A network is simply a URL to a tracker. The tracker provides a list of articles within the system. To add an article, the user posts the magnet information for the article and the file will be propagated. 

### Tracker
- / = Stats, and config for the message board
- /q = Queryable interface (figure this out)
- /announce = Usual bt announce protocol
- /scrape = usual bt scrape protocol