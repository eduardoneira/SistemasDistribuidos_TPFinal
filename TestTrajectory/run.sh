#!/bin/bash
id=0;
for f in $(ls ./BigPic)
do
  cp "./BigPic/"${f}  "./Camara"${id}"/img/"
  id=$(( $id + 1 ))
done
for i in {0..4}
do
  cd "./Camara"${i}
  python3 "main.py"
  cd ".."
done
