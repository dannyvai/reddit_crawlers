
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import caffe
import skimage.color as color
import scipy.ndimage.interpolation as sni
import cv2
import scipy.io as sio
from PIL import Image
import os  


l_mean = sio.loadmat('ilsvrc_2012_mean.mat')
lm = np.array(l_mean['mean_data'])
lm = lm/np.max(lm)
lm_lab = color.rgb2lab(lm)
lm_lab_l = lm_lab[:,:,0]
lm_lab_l = lm_lab_l - np.mean(np.mean(lm_lab_l)) + 50
lm_lab_l =  Image.fromarray(lm_lab_l)


plt.rcParams['figure.figsize'] = (12, 6)
gpu_id = 0
caffe.set_mode_gpu()
caffe.set_device(gpu_id)
print 'loading network...'
net = caffe.Net('colorization_deploy_v0.prototxt', 'colorization_release_v0.caffemodel', caffe.TEST)
print '\n done loading network! \n'

(H_in,W_in) = net.blobs['data_l'].data.shape[2:] # get input shape
(H_out,W_out) = net.blobs['class8_ab'].data.shape[2:] # get output shape
net.blobs['Trecip'].data[...] = 6/np.log(10) # 1/T, set annealing temperature
# load the original image

mainDir = './demo/'
for fn in os.listdir(mainDir):
     if os.path.isfile((mainDir + fn)):
        print (fn)
        
        img_rgb = caffe.io.load_image((mainDir + fn))
        
        img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
        img_l = img_lab[:,:,0] # pull out L channel
        img_l_eq = img_l.copy()
        
        powerFactor = 0.5
        img_l_eq = img_l
        img_l_eq = img_l_eq - np.min(img_l_eq)
        img_l_eq = img_l_eq / np.max(img_l_eq) * 2
        img_l_eq = np.power(img_l_eq,powerFactor) * 100/np.power(2,powerFactor)
        
        (H_orig,W_orig) = img_rgb.shape[:2] # original image size
        
        # create grayscale version of image (just for displaying)
        img_lab_bw = img_lab.copy()
        img_lab_bw[:,:,1:] = 0
        img_rgb_bw = color.lab2rgb(img_lab_bw)
        
        # resize image to network input size
        img_rs = caffe.io.resize_image(img_rgb,(H_in,W_in)) # resize image to network input size
        img_lab_rs = color.rgb2lab(img_rs)
        img_l_rs = img_lab_rs[:,:,0]
        img_l_rs_eq = img_l_rs.copy()
        lm_lab_l_rs = lm_lab_l.resize((W_in,H_in), Image.ANTIALIAS)
        
        img_l_rs_eq = img_l_rs
        img_l_rs_eq = img_l_rs_eq - np.min(img_l_rs_eq)
        img_l_rs_eq = img_l_rs_eq / np.max(img_l_rs_eq) * 2
        img_l_rs_eq = np.power(img_l_rs_eq,powerFactor) * 100/np.power(2,powerFactor)
        # show original image, along with grayscale input
        img_pad = np.ones((H_orig,W_orig/10,3))
        img_pad1 = np.ones((H_orig,W_orig/10))
        
        net.blobs['data_l'].data[0,0,:,:] = img_l_rs - lm_lab_l_rs # subtract 50 for mean-centering
        net.forward() # run network
        print '\n finish going through network! \n'
        
        ab_dec = net.blobs['class8_ab'].data[0,:,:,:].transpose((1,2,0)) # this is our result
        ab_dec_us = sni.zoom(ab_dec,(1.*H_orig/H_out,1.*W_orig/W_out,1)) # upsample to match size of original image L
        img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
        img_rgb_out = np.clip(color.lab2rgb(img_lab_out),0,1) # convert back to rgb
        
        newImage = np.hstack(( img_rgb, img_pad,img_rgb_bw,img_pad,img_rgb_out ))
        cv2.imwrite((mainDir + 'together/' + fn),(newImage[:,:,[2,1,0]]*255).astype('uint8'))
        

