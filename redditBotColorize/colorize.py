import numpy as np
import caffe
import skimage.color as color
import scipy.ndimage.interpolation as sni
import scipy.io as sio
from PIL import Image

net = None
W_in = None
H_in = None
H_out = None
W_out = None
lm_lab_l_rs = None

def loadDNN(useGpu = False):
    global net,W_in,H_in,H_out,W_out,lm_lab_l_rs
    if useGpu:    
        gpu_id = 0
        caffe.set_mode_gpu()
        caffe.set_device(gpu_id)
    net = caffe.Net('colorization_deploy_v0.prototxt', 'colorization_release_v0.caffemodel', caffe.TEST)
    print '\n done loading network! \n'

    (H_in,W_in) = net.blobs['data_l'].data.shape[2:] # get input shape
    (H_out,W_out) = net.blobs['class8_ab'].data.shape[2:] # get output shape
    net.blobs['Trecip'].data[...] = 6/np.log(10) # 1/T, set annealing temperature
    
    l_mean = sio.loadmat('ilsvrc_2012_mean.mat')
    lm = np.array(l_mean['mean_data'])
    lm = lm/np.max(lm)
    lm_lab = color.rgb2lab(lm)
    lm_lab_l = lm_lab[:,:,0]
    lm_lab_l = lm_lab_l - np.mean(np.mean(lm_lab_l)) + 50
    lm_lab_l =  Image.fromarray(lm_lab_l)    
    lm_lab_l_rs = lm_lab_l.resize((W_in,H_in), Image.ANTIALIAS)
    
def runDNN(imagePath):
    global net,W_in,H_in,H_out,W_out
    if net is None:
        print 'Fuck you!'
        return -1
    # load the original image
    img_rgb = caffe.io.load_image(imagePath)
    (H_orig,W_orig) = img_rgb.shape[:2] # original image size
    img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
    img_l = img_lab[:,:,0] # pull out L channel

    # Strech the histogram
    powerFactor = 1
    img_l = img_l - np.min(img_l)
    img_l = img_l / np.max(img_l) * 2
    img_l = np.power(img_l,powerFactor) * 100/np.power(2,powerFactor)
    
    # resize image to network input size
    img_rs = caffe.io.resize_image(img_rgb,(H_in,W_in)) # resize image to network input size
    img_lab_rs = color.rgb2lab(img_rs)
    img_l_rs = img_lab_rs[:,:,0]

    # Strech the histogram
    img_l_rs = img_l_rs - np.min(img_l_rs)
    img_l_rs = img_l_rs / np.max(img_l_rs) * 2
    img_l_rs = np.power(img_l_rs,powerFactor) * 100/np.power(2,powerFactor)    
    
    net.blobs['data_l'].data[0,0,:,:] = img_l_rs - lm_lab_l_rs # subtract 50 for mean-centering
    net.forward() # run network
    print '\n finish going through network! \n'
    
    ab_dec = net.blobs['class8_ab'].data[0,:,:,:].transpose((1,2,0)) # this is our result
    ab_dec_us = sni.zoom(ab_dec,(1.*H_orig/H_out,1.*W_orig/W_out,1)) # upsample to match size of original image L
    img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
    img_rgb_out = np.clip(color.lab2rgb(img_lab_out),0,1) # convert back to rgb
    return (img_rgb_out[:,:,[2,1,0]]*255.0).astype('uint8')
    




