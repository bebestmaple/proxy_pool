#!/bin/bash

python3 /app/proxy_pool/proxyPool.py schedule > /dev/null 2>&1 &
python3 /app/proxy_pool/proxyPool.py server