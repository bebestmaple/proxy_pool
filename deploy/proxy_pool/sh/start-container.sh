#!/bin/bash

chmod 777 /app/deploy/proxy_pool/sh/start-container.sh
python3 /app/proxyPool.py schedule > /dev/null 2>&1 &
python3 /app/proxyPool.py server