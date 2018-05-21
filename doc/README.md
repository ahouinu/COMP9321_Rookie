#This is the API document reference

###@LY



###@MS

The api below is based on the NSW Map Service. We use the defalut layer 0(More details check[layer](http://maps.six.nsw.gov.au/arcgis/sdk/rest/index.html#/Layer_Table/02ss00000089000000/)), the logic of the api is simply use the intersection query with 'Rid'.

###get_poi(city, suburb_name, description)

###Request Parameter

Parameter   | Deatails
---------   | --------
city	    | String input which is the city name
surburb     | String input which is the city name
description | This parameter is to narrow the information to fit up with the requirements of users.It could be a List or a String.<br>Examples: description = [restaurant, chinese food]<br>description = 'opera hosue'

