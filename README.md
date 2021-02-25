# fhmediacollector
> A Python package to help gather and sort media from e621 for easier video/slideshow creation.

## Setup

From source:

```
$ git clone https://github.com/oddpawsx/fhmediacollector
$ cd fhmediacollector
$ pip install .
```

From PyPI:

```
$ pip install fhmediacollector
```

## Usage
```
$ fhcollector -h
   __ _               _ _           _             
  / _| |__   ___ ___ | | | ___  ___| |_ ___  _ __ 
 | |_| '_ \ / __/ _ \| | |/ _ \/ __| __/ _ \| '__|
 |  _| | | | (_| (_) | | |  __/ (__| || (_) | |   
 |_| |_| |_|\___\___/|_|_|\___|\___|\__\___/|_|   


        Author:         OddPawsX
        Discord:        OddPawsX#6969
	      Version: 	v1.1.4


==================================================
usage: fhcollector [-h] [--search SEARCH] [--searchconf SEARCHCONF] [--config CONFIG] [--avoid AVOID] [--no-safe]
                   [--no-questionable] [--no-explicit] [--no-api-key] [--version]

Gathers posts from e621 matching the specified tags,
 then organizes for ease in video/slideshow creation.

optional arguments:
  -h, --help            show this help message and exit
  --search SEARCH, -s SEARCH
                        The e621 search string to use
  --searchconf SEARCHCONF, -f SEARCHCONF
                        Path to a file containing multiple e621 search strings
  --config CONFIG, -c CONFIG
                        Path to env file with config variables. Default: ~/.fhcollector.env
  --avoid AVOID, -a AVOID
                        Path to file with list of tags to avoid. One per line. 
  --no-safe             If present, exclude posts with the rating 'safe'
  --no-questionable     If present, exclude posts with the rating 'questionable'
  --no-explicit         If present, exclude posts with the rating 'explicit'
  --no-api-key, -l      If present, make requests to e621 without API key
  --version             show program's version number and exit
```