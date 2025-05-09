#!/bin/bash
pip install watchdog
watchmedo shell-command --patterns="train_from_logs.py" --recursive --command='python train_from_logs.py' .
