poi.py 主要完成了对api的调用，

与glue.py的对接要求：

###input： String类型，所有parameter在一个String里面用空格分开 eg: sydney kensington university

###output: 

没有搜索结果时：

返回String，提示用户no such results

如果有结果：

如果只有一个parameter则直接返回point_list
point_list数据类型：元素为dic类型的list

如果有多个parameter，则poi.py通过inter_check_list函数寻找符合条件的rid_list, 再返回inter_chekc_list
inter_list数据类型： 元素为dic类型的list

## The source code explanation

>the format of the url has been attached on the top of the py file

##functoin design

###check_link(url)
detect the connectoin with url

###get_content(list, src)
The main function to implement the web crawler. Beatifulsoup is a power python package to parse the tag of html. The function get the resource of the html and store into a list. The format of the item in the list is dic.

###inter_check(data)
This function is to intergrate the input of the users and find the most available results to response. The parameter 'data' is the whole source of the initial result divided by description. This function returns the rid of the property results.

###run(user_input)

This is the main function and where the interaction between poi.py and glue.py happends. The input has been split into serveral parameters to do the query. Developer should figure out the data format before extend to modify the program.