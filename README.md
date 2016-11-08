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

There are currently two paths to using this code: 1) run a purpose-built docker container, 2) install the dependencies yourself. The first option should be easiest if you seek to simply run the code. The second options is recommended if you want to change/expand or otherwise modify the code. 

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

---

# Licence

MIT License

Copyright (c) [2016] [Robbert Nicolai van de Velde]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

