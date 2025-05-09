#!/bin/bash
# Install watchdog to ensure watchmedo is available
pip install watchdog

# Run the training loop using watchmedo
watchmedo shell-command \
  --patterns="train_from_logs.py" \
  --recursive \
  --command='python train_from_logs.py' \
  .
