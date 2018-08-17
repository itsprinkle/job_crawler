# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')


from  xml.dom import  minidom
def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename='360buy.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')



def get_xml_data(filename='360buy.xml'):
    start_urls=[]

    sub_pattern_dict={}
    next_pattern_dict={}
    next_field_pattern_dict={}

    item_pattern_dict={}
    node_pattern_dict={}

    sub_relabs_dict={}
    next_relabs_dict={}
    next_field_relabs_dict={}
    item_relabs_dict={}

    page_lang_dict={}

    doc = minidom.parse(filename)
    root = doc.documentElement

    sub_nodes = get_xmlnode(root,'sub')
    for node in sub_nodes:
        url = get_attrvalue(node,'url')
        lang = get_attrvalue(node,'lang')
        start_urls.append(url)

    	node_pattern_dict[url]={}
	
        if lang:
           page_lang_dict[url]=lang
	else:
           page_lang_dict[url]="chn"

	
	####在sub下面解析next节点的信息
        node_next = get_xmlnode(node,'next')
        if len(node_next)==0:
           next_pattern_dict[url]="NULL"
           sub_pattern_dict[url]="NULL"
           next_relabs_dict[url]="NULL"
        else:
           for next in node_next:
             next_xpath = get_attrvalue(next,'xpath')
             if next_xpath == "":
                next_pattern_dict[url]=("NULL")
                sub_pattern_dict[url]=("NULL")
             else:
                sub_pattern_dict[url]=next_xpath
                next_pattern_dict[url]=(next_xpath)

             next_relabs = get_attrvalue(next,'relabs')
             if next_relabs == "" or next_relabs is None:
                sub_relabs_dict[url]="absolute"
                next_relabs_dict[url]="absolute"
             else:
                sub_relabs_dict[url]=next_relabs
                next_relabs_dict[url]=next_relabs

	####在sub下面解析field节点的信息
        node_next_field = get_xmlnode(node,'next_field')
        if len(node_next_field)==0:
           next_field_pattern_dict={}
           #next_field_relabs_dict[url]="NULL"
        else:
           next_field_pattern_list={}
           for next_field in node_next_field:
             next_field_xpath = get_attrvalue(next_field,'xpath')
             next_field_name = get_attrvalue(next_field,'name')
             if next_field_xpath == "":
                next_field_pattern_dict[url]=("NULL")
             else:
           	next_field_pattern_list[next_field_name]=next_field_xpath 
             next_field_pattern_dict[url]=next_field_pattern_list

             #next_field_relabs = get_attrvalue(next_field,'relabs')
             #if next_field_relabs == "" or next_field_relabs is None:
             #   next_field_relabs_dict[url]="absolute"
             #else:
             #   next_field_relabs_dict[url]=next_field_relabs


	###在sub下面解析item
        node_item = get_xmlnode(node,'item')
        if len(node_item)==0:
           item_pattern_dict[url]=[]
        else:
	   item_pattern_list={}
           for item in node_item:
             item_xpath = get_attrvalue(item,'xpath')
             item_name = get_attrvalue(item,'name')
             if item_xpath == "":
		item_pattern_list[item_name]="NULL"
             else:
		item_pattern_list[item_name]=item_xpath
             item_pattern_dict[url]=item_pattern_list

             item_relabs = get_attrvalue(item,'relabs')
             if item_relabs == "" or item_relabs is None:
                item_relabs_dict[url]="absolute"
             else:
                item_relabs_dict[url]=item_relabs

	     ##在item下面解析node 
	     node_field = get_xmlnode(item,'field')	
	     node_pattern_list={}
	     for field in node_field:
	         node_xpath = get_attrvalue(field,'xpath')
	         node_name = get_attrvalue(field,'name')
                 if node_xpath == "":
		    node_pattern_list[node_name]="NULL"	
	         else:
                    node_pattern_list[node_name]=node_xpath
		 node_pattern_dict[url][item_name]=node_pattern_list
	       
    return start_urls,sub_pattern_dict,next_pattern_dict,next_field_pattern_dict,item_pattern_dict,node_pattern_dict,sub_relabs_dict,next_relabs_dict,item_relabs_dict,page_lang_dict

def test_xmltostring():
    print xml_to_string()


def test_load_xml():
    start_urls,sub_pattern,next_pattern,next_field_pattern,item_pattern,node_pattern,sub_relabs,next_relabs,item_relabs,page_lang=get_xml_data()
    print (start_urls)
    print (next_pattern)
    print (item_pattern)
    print (node_pattern)

    print (sub_relabs)
    print (next_relabs)
    print (item_relabs)

if __name__ == "__main__":
    test_xmltostring()
    test_load_xml()
