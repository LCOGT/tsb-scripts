# tsb-scripts
Scripts used in conjunction with the Telescope Software Build, e.g. to analyse tracking performance

## Virtual environment

Before executing these scripts, set up a python virtual environment:

```
$ cd tsb-scripts
$ virtualenv venv
$ source venv/bin/activate
```
## Install required libraries

From within your virtual environment:
```
$ pip install -r requirements.txt
```

## Run the script

For example to analyse a mic log:
```
python AmcLog.py /path/to/data/files/mic.1m0a.doma.bpl.lco.gtnPT202110062055.dat
```

