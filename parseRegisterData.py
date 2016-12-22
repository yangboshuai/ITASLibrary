f=open(r'C:\Python27\Lib\site-packages\ITASLibrary\tmp2.txt','r')

data = {}

for x in f:
    tmp=x.split()
    if len(tmp)>1:
        print "'"+tmp[0]+"':'"+tmp[1]+"',"
    else:
        print "'"+tmp[0]+"':'',"
f.close()
