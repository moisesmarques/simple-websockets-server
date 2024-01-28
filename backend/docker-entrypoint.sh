#!/bin/bash
# exit on error
set -o errexit

# testing
#python ./websocket.py

# serve (use -n parameter to run in the foreground)
supervisord -c supervisord.conf