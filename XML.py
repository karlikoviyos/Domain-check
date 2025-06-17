import urllib.request
import xml.dom.minidom as minidom

def get_dns(xml_file):
    dom = minidom.parseString(xml_file)
    dom.normalize()
    elements=dom.getElementsByTagName("DomainGetListResult")
    dns_dict={}
    domains_dict={}
    info_list=[]
    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == "Domain":
                    key= child.getAttribute('Name')
                    value1=child.getAttribute('User')
                    value2 = child.getAttribute('Created')
                    value3 = child.getAttribute('Expires')
                    value4=child.getAttribute("IsOurDNS")
                    value=[value1, value2,value3,value4]
                    
                    dns_dict[key] = value
    return dns_dict
                
def get_dns_servers(login,token,userIP,requests):
    spisok_listov=[]
    
    for request in requests:
        req=request.split('.')
        
        url='https://api.namecheap.com/xml.response?ApiUser='+login+'&ApiKey='+token+'&UserName='+login+'&Command=namecheap.domains.dns.getList&ClientIp='+userIP+'&SLD='+req[0]+'&TLD='+req[1]
        data=xml_read(url)
        dom = minidom.parseString(data)
        dom.normalize()
        elements=dom.getElementsByTagName("DomainDNSGetListResult")
        child_list=[]
        for node in elements:
            for child in node.childNodes:
                if child.nodeType == 1:
                    if child.tagName == "Nameserver":
                        value=str(child.firstChild.data)
                        child_list.append(value)
        spisok_listov.append(child_list)
    return spisok_listov
                        # value=[value1, value2,value3,value4]
def xml_read(url):
    file=urllib.request.urlopen(url)
    return file.read()
def print_dict(dict):
    data_list={}
    for key in dict.keys():
        data_list[key]=dict[key]
    return data_list
def get_list(login,token,userIP):
    url="https://api.namecheap.com/xml.response?ApiUser="+ login+"&ApiKey="+token+"&UserName="+login+"&Command=namecheap.domains.getList&ClientIp="+userIP
    data=xml_read(url)
    dns = get_dns(data)
    dns_list=print_dict(dns)
    return dns_list