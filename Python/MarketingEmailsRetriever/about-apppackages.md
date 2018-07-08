To output just the packages of the apps, change this code:

```python
def writeFile():
    writeFile = open("OutputEmails.txt", "w")
    for email in emailList:
        writeFile.write("%s\n" % email)
    writeFile.close()
```

to this one:

```python
def writeFile():
    writeFile = open("apppackages.txt", "w")
    for package in finalLinkList:
        writeFile.write("%s\n" % package)
    writeFile.close()
```
