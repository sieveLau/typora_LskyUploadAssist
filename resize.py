from PIL import Image
from pathlib import Path
import os

MAX_UPLOAD_SIZE_IN_BYTE = 1.8*1000*1000
TARGET_IMAGE_WIDTH_IN_PIXELS = 1024
QUALITY_STEP = 5

def append_id(filename,id):
    path = Path(filename)
    return path.with_stem(f"{path.stem}_{id}")

#print(append_id(testfile,"resized"))

def compress_under_size(size, file_path):
    '''file_path is a string to the file to be custom compressed
    and the size is the maximum size in bytes it can be which this 
    function searches until it achieves an approximate supremum'''

    # if RGBA, convert into RGB (jpeg doesn't support A)
    with Image.open(file_path) as picture:
        if picture.mode in ("RGBA", "P"): 
            picture = picture.convert("RGB")
            picture.save(file_path)
            picture.close()
        

    quality = 90 #not the best value as this usually increases size

    current_size = os.stat(file_path).st_size

    while current_size > size or quality == 0:
        if quality == 0:
            os.remove(file_path)
            raise Exception("Error: File cannot be compressed below this size")  
        current_size = compress_pic(file_path, quality)
        quality -= QUALITY_STEP


def compress_pic(file_path, qual):
    '''File path is a string to the file to be compressed and
    quality is the quality to be compressed down to'''
    picture = Image.open(file_path)
    #dim = picture.size
    
    picture.save(file_path,"JPEG", optimize=True, quality=qual) 
    picture.close()
    processed_size = os.stat(file_path).st_size

    return processed_size

def resize(filePath):
    basewidth = TARGET_IMAGE_WIDTH_IN_PIXELS

    # open放在外面，因为open如果抛出Exception就不会占用，也就不需要close
    img = Image.open(filePath)
    savePath = append_id(filePath,"resized")
    try:
        wpercent = (basewidth/float(img.size[0]))
        
        # 如果是放大的话就不用做分辨率缩小了
        if wpercent <= 1.0 :
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
        # 但是也有可能小图大size，还是要做一个压缩文件大小的操作
        if os.stat(filePath).st_size < MAX_UPLOAD_SIZE_IN_BYTE: return filePath
        else:
            img.save(savePath)
            # compress_under_size会重新打开图片，所以先close
            img.close()
            compress_under_size(MAX_UPLOAD_SIZE_IN_BYTE, savePath)
            return savePath
    finally: img.close()