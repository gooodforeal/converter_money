def get_vals(date=get_normal_date()):
#     response = urllib.request.urlopen(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date[0]}/{date[1]}/{date[2]}")
#     dom = xml.dom.minidom.parse(response)
#     dom.normalize()
#     vals_list = []
#     node_list = dom.getElementsByTagName("Valute")
#     for node in node_list:
#         children = node.childNodes
#         for child in children:
#             if child.nodeName == "Name":
#                 vals_list.append(child.childNodes[0].nodeValue)
#                 if "Польский" in child.childNodes[0].nodeValue:
#                     vals_list.append("Российский рубль")
#     return vals_list