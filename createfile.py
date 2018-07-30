import os
for i in range(1, 100):
    file = open("E:/files/file"+str(i)+".html",'w')
    file.write("<html><h1>File"+str(i)+"</h1><body>Used for Testing.</body></html>")
    file.close()
