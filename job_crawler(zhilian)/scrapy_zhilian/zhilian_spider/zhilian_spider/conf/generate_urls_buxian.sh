#http://sou.zhaopin.com/jobs/searchresult.ashx?
echo "" | awk '{
 if(ARGIND==1)
 {
     hangye_dict[$1]=$2; 
 }
 else if(ARGIND==2)
 { 
     city_dict[$1]=$2; 
 }
 else if(ARGIND==3)
 {
     salary_dict[$1]=$2; 
 }
 else if(ARGIND==4)
 {
     company_dict[$1]=$2; 
 }
 else if(ARGIND==5)
 {
     years_dict[$1]=$2; 
 }
 else if(ARGIND==6)
 {
     xueli_dict[$1]=$2; 
 }
 else if(ARGIND==7)
 {
     fabushijian_dict[$1]=$2; 
 }

}END{
  for(hangye in hangye_dict)
  {
      for(city in city_dict)
      {
         for(salary in salary_dict)
         {
            for(company in company_dict)
            {
                for(year in years_dict)
                {
                    for(xueli in xueli_dict)
                    {
                       for(fabushijian in fabushijian_dict)
                       {
                            print "http://sou.zhaopin.com/jobs/searchresult.ashx?"hangye"&amp;"city"&amp;"salary"&amp;"company"&amp;"year"&amp;"xueli"&amp;"fabushijian"\t"hangye_dict[hangye]"\t"city_dict[city]"\t"salary_dict[salary]"\t"company_dict[company]"\t"years_dict[year]"\t"xueli_dict[xueli]"\t"fabushijian_dict[fabushijian]
                       }
                    }
                }
            }
         }
      }
  }
}' ./hangye.dict ./city.dict ./salary.dict ./company_type.dict ./years.dict.1 ./xueli.dict  ./fabushijian.dict

