#!/bin/bash

python3 /app/proxyPool.py schedule > /dev/null 2>&1 &
python3 /app/proxyPool.py server