from PIL import Image, ImageStat

def is_color_image(file, thumb_size=40, MSE_cutoff=100, adjust_color_bias=True):
    pil_img = Image.open(file)
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

if __name__ == "__main__":
    import image_downloader
    img_url = 'http://imgur.com/n8d3Cjt'
    file_path = image_downloader.download_image(img_url)
    detect_color_image(file_path,40,100)

