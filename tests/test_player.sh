#!/bin/bash
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
CLASSPATH1=~/ai/gthd/gthd.jar
CLASSPATH2=~/ai/grossthello/grossthello.jar
FILE=results.log

if test -f "$FILE"; then
  rm "$FILE"
fi
for i in {1..50};
do 
  $JAVA_HOME/bin/java -cp $CLASSPATH1 Gthd 0 >> results.log &
  sleep 0.5
  python3 ~/ai/gothello/gthplayer.py black localhost 0 3 >> /dev/null &
  $JAVA_HOME/bin/java -cp $CLASSPATH2 Grossthello white localhost 0 3 >> /dev/null &
  sleep 10
done
python3 ~/ai/gothello/tests/count_wins.py
