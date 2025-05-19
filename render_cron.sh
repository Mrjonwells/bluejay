#!/bin/bash
cd /opt/render/project/src || exit
python3 backend/generators/blog_generator_runner.py
