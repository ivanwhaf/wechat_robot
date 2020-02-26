import os

path = 'f:\\wxPic\\'


def rename():
    i = 1000
    for pics in os.listdir(path):
        fileName = os.path.splitext(pics)[0]
        fileType = os.path.splitext(pics)[1]
        os.rename(os.path.join(path, pics),
                  os.path.join(path, str(i)+fileType))
        i = i+1

    i = 1
    for pics in os.listdir(path):
        oldName = os.path.join(path, pics)
        if os.path.getsize(oldName)/1024 > 500:
            os.remove(oldName)
            print('%s has been deleted!' % pics)
            continue
        fileName = os.path.splitext(pics)[0]
        fileType = os.path.splitext(pics)[1]
        newName = os.path.join(path, str(i)+fileType)
        if oldName != newName:
            os.rename(oldName, newName)
            print('%s--->%s' % (pics, str(i)+fileType))
        i = i+1

    print('rename successfully!')

# rename()
