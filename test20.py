def AddToExceptIParr(n,value):
    l= list( ftpExceptIParr)

    num = n -l.count(value)
    for i in range(1,num):
        ftpExceptIParr.append(value)
    return
c=[]
ftpExceptIParr=[]
a= ["4/5","5.3.3","6.3.36"]
AddToExceptIParr(10,a[1] )
print (c)
ftpExceptIParr.remove(a[1])
ftpExceptIParr.remove(a[1])
ftpExceptIParr.remove(a[1])
ftpExceptIParr.remove(a[1])
