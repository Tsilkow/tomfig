# Tomfig

This repository holds my dotfiles as well as the script for updating, syncing and setting them up.

Names and paths of configs are held in `metaconfig.py`.

## Usage

To see the state of configs declared in metaconfig, run:
```bash
python manage.py check
```

To set up symlinks for all configs in a given set, run:
```bash
python manage.py setup $config_set
```
(by default, files at specified locations are backed up and symlinks are overwritten)


To add local config, that's written in metaconfig but absent in tomfig, run:
```bash
python manage.py move-to-tomfig $config_set
```


