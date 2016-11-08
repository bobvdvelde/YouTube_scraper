# YouTube_scraper

Scrapes youtube videos and comments based on search terms. Uses python 3 and elasticsearch 2.X

---

# Installation 

## Docker container

Make sure you have docker ('docker.io' for linux, the docker native client for win/mac) installed. 

```bash
docker run -it --name 'youtube_scraper' -v "$(pwd)":/data rnvdv/youtube_scraper /bin/bash
$youtube_scraper> python /youtube/termfinder.py
```

## Generic installation

### 1. Pull this repo

```bash
git pull https://github.com/bobvdvelde/YouTube_scraper.git
```

### 2. Install python dependencies 

Preferably in a virtualenvironment

```bash
pip install -r Requirements
```

### 3. Run elasticsearch 2.X

If you don't already have it:

```bash
wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.0/elasticsearch-2.4.0.tar.gz
tar -zxvf elasticsearch-2.4.0.tar.gz
```

And run it

```
./elasticsearch-2.4.0/bin/elasticsearch
```

### 4. Run the termfinder

```bash
python termfinder.py
```

enjoy
