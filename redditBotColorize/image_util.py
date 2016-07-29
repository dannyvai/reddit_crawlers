from PIL import Image, ImageStat
import numpy as np

def is_color_image(file, thumb_size=50, MSE_cutoff=140, adjust_color_bias=True):
    try:
        pil_img = Image.open(file)
    except:
        print 'Couldn\'t open file %s'%file
        return False

    np_img = np.array(pil_img)
    if len(np_img.shape) > 2 and np_img.shape[2] > 1:
        if np.sum(np_img[:,:,1] - np_img[:,:,2]) == 0:
            print 'Grayscale'
            return False
    else:
        return False

    bands = pil_img.getbands()
    if bands == ('R','G','B') or bands== ('R','G','B','A'):
        thumb = pil_img.resize((thumb_size,thumb_size))
        SSE, bias = 0, [0,0,0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias)/3 for b in bias ]
        for pixel in thumb.getdata():
            mu = sum(pixel)/3
            SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
        MSE = float(SSE)/(thumb_size*thumb_size)
        if MSE <= MSE_cutoff:
            print "grayscale\t",
            print "( MSE=",MSE,")"
            return False
        else:
            print "Color\t\t\t",
            print "( MSE=",MSE,")"

            return True
    elif len(bands)==1:
        print "Black and white", bands
        return False
    else:
        print "Don't know...", bands
        return False
