#!/bin/sh
awk '{
  if(ARGIND==1)
  {
    city_dict[$1]=$2;
  }
  else if(ARGIND==2)
  {
    workyear_dict[$1]=$2;
  }
  else if(ARGIND==3)
  {
    degreefrom_dict[$1]=$2;
  }
  
  else
  {
    for(city in city_dict)
    {
      for(workyear in workyear_dict)
      {
        for(degreefrom in degreefrom_dict)
        {
          print "http://search.51job.com/jobsearch/search_result.php?fromJs=1&amp;jobarea="city"&amp;workyear="workyear"&amp;degreefrom="degreefrom"&amp;funtype="$1"\t"$2"\t"city_dict[city]"\t"workyear_dict[workyear]"\t"degreefrom_dict[degreefrom]
        }
      }
    } 
  }
}' ./city.codes   ./workyear.codes  ./degreefrom.codes  ./title.codes > ./sub.list
