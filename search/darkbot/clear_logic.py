import socket

print('name of current module is : '+__name__)
''' Basically Smetimes when you are importing from a module, you would like to know whether a modules function is being used as an import, or if you are using the original .py file of that module.


a=[0,1,2,3,4,5,6,7,8,9]
b="dark"
e=[]
for x in a:
    e.append([x,b])
for x in e:
    print(x)

a=set()
a.add('a')
print(a)
for each in a:
    print(each)


a="my name is"
b="daud"

if b in a:
    print(b)
else:
    print("b is not in a")'''

a="daudaaaaaaaaaa"
temp = socket.socket
print(temp)
b=a.rindex('d')
a=a[:b+1]
print(b)
print(a)