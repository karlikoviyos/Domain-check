import pandas as pd
import csv
from XML import *
import os
dir = os.getcwd()
pd.set_option('display.max_column',None)

df = pd.DataFrame({'AccauntName': [], 'DomainName': [], 'Created': [], 'Expires': [],'Ns-Namechip':[],'NS-1': [],'NS-2': [],'NS-3': [],'NS-4': []})
df.to_csv(dir+'\output.csv')


ichilnik=2
with open('input.csv') as f:
    csv_reader=csv.reader(f)
    next(csv_reader)
    Users = []
    Domains = []
    Createds = []
    Expireses = []
    IsOurNss=[]
    DNS_serverers = []
    NS1s=[]
    NS2s=[]
    NS3s=[]
    NS4s=[]
    for row in csv_reader:
        User, Token, IP =row
        warnUser=User
        request = get_list(User, Token, IP)
        DNS_servers=get_dns_servers(User,Token,IP,request)

        if len(request) >0:
            for domain in request:
                    Username=request[domain][0]
                    Created=request[domain][1]
                    Expires=request[domain][2]
                    IsOurNS=request[domain][3]
                    Users.append(User)
                    Domains.append(domain)
                    Createds.append(Created)
                    Expireses.append(Expires)
                    
                    IsOurNss.append(IsOurNS)
            for dom in range(len(request)):
                DNS_server=list(DNS_servers[dom])
                
                for i in range(4):
                    if len(DNS_server)<4:
                        count_of_NaN=4-len(DNS_server)
                        for i in range(count_of_NaN):
                            DNS_server.append('NaN')
                    else:
                        pass
                DNS_serverers.append(DNS_server)
        else:
            print("Вы неправильно ввели Логин,токен или IP в строке "+str(ichilnik))
            Users.append(User)
            Domains.append('NaN')
            Createds.append('NaN')
            Expireses.append('NaN')
            IsOurNss.append('NaN')
            DNS_serverers.append(['NaN','NaN','NaN','NaN'])
        ichilnik+=1
    for i in DNS_serverers:
        NS1s.append(i[0])
        NS2s.append(i[1])
        NS3s.append(i[2])
        NS4s.append(i[3])
    a={'AccauntName': Users, 'DomainName': Domains, 'Created': Createds, 'Expires': Expireses,'NS NameChip': IsOurNss,'NS-1': NS1s,'NS-2': NS2s,'NS-3': NS3s,'NS-4': NS4s}
    df = pd.DataFrame.from_dict(a)
    df.transpose()
    df.to_csv(dir + '\output.csv', mode='a', header=False)
    inp=input('press Enter to Continue')
        