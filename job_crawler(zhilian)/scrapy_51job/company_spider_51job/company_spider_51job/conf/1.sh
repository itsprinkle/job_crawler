#!/bin/sh
echo "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"  > pattern.conf
echo "<site>" >> pattern.conf

awk '{
  if(ARGIND==1)
  {
    dict[NR]=$0;
  } 
  else
  {
    print "<sub url=\""$1"\" >";
    for(i=1;i<=27;i++)
    {
       print dict[i];     
    }
  }
}' ./temp.txt ./sub.list.head >>  pattern.conf

echo "</site>" >> pattern.conf
