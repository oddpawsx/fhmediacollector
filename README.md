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

## Example Usage
```
─ ~/Desktop
╰─❯ fhcollector --avoid avoid_list.txt --no-safe --search "male solo dildo_in_ass order:score score:>=290"
Current Configuration:
--------------------------------------------------
Allowed ratings: ['q', 'e']
CONF FILE:     /home/opx/.fhcollector.env
Username:     *********
API Key:     ********************************
--------------------------------------------------
Tags to avoid: ['human', 'cub']
--------------------------------------------------
Run ID: d4606b3d-c334-473e-b16a-a500b81d97e7
--------------------------------------------------
Performing search "male solo dildo_in_ass order:score score:>=290":
Downloaded '[872][eto_ya][2185811][D][A] ff1b6bb0f46f27d48b7d3ed3a441a478.gif'.
... (truncated for length) ...
Downloaded '[291][doxy+rajii][263968][C][S] c96521e2b9d67922b2fd99ae632e138d.jpg'.


--------------------------------------------------
DONE. Downloaded 13 pieces of media. Check the fhcollected folder.
```

## Naming Conventions of saved media
```
Filename: 
[872][eto_ya][2185811][D][A] ff1b6bb0f46f27d48b7d3ed3a441a478.gif
---
[872] = Post score
[eto_ya] - artist(s)
[2185811] = Post ID
[D] = whether or not there is cum (C=there is, D=dry/there isn't)
[A] = whether or not it is animated (S=static, A=animated)
ff1b6bb0f46f27d48b7d3ed3a441a478.png - the orignal filename from e621 (which I believe is the file's MD5 hash?)
```

