To add new feature -> create branch with name: username/feature_name.

prepare env for linux (for MacOS change apt with brew for windows dunno xD):
```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3.7
sudo pip3 install virtualenv
```

in repo dir: 
```
virtualenv venv -p $(which python3.7)

source venv/bin/activate    # or add in pycharm like
pip install -r requiments.txt
```
