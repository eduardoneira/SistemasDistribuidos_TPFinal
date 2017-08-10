#!/usr/bin/env bash

FILES = /BigPic/*.jpg
id = 0;
pids = (0 0 0 0)
for f in $files
do
  currentCamera = './camara' + str(id)
  cp f  currentCamera+'/img/'
  python3 currentCamera+'/main.py'
  pids[id] = $!
  id += 1;
done
for i in 0..4
do
  kill -INT pids[i]
done
