import os

path = 'f:\\wxPic\\'
lis = []


def picHandle():
    for pics in os.listdir(path):
        filename = os.path.join(path, pics)
        fileSize = os.path.getsize(filename)
        if fileSize == 0:
            os.remove(filename)
            print('%s is null and has been deleted!' % pics)
            continue
        if fileSize in lis:
            os.remove(filename)
            print('%s repeated and has been deleted!' % pics)
        else:
            lis.append(fileSize)
    print('Deleting duplicate and null pics successfully!')

# picHandle()
