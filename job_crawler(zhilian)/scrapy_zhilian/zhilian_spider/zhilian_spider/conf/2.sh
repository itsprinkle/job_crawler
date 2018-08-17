#!/bin/sh
#awk -F ' ' '{ 
#for(i=2;i<=NF;i++)
#{
# print "jl="$i" "$i;
#}
#}' city.list  > ./city.list.1

awk '{
 if(ARGIND==1)
{
   dict[$0]; 
}
else
{
  if($0 in dict)
  {
     
  }
  else
  {
      print $0;
  } 
}
}' ./main_city.dict  ./city.list.1 > ./mini_city.dict
