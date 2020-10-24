#!/bin/bash

ps aux | grep SimpleHTTPServer | grep -v grep | awk '{print $2}' | while read pid; do kill -9 $pid; done
ps aux | grep "watch .. . make html" | grep -v grep | awk '{print $2}' | while read pid; do kill -9 $pid; done

cd build/html

/usr/bin/python2 -m SimpleHTTPServer > /dev/null 2>&1 &

cd ..

watch -n 2 "make html" > /dev/null 2>&1 &
