#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import images2gif
import Image
from random import random as rand
from math import pi, sin, cos
from skimage import io, color


def fuckwith(image, p, colors=None, pil=False):
    
    if isinstance(image, Image.Image):
        image = np.array(image.convert('RGB'))

    a, b, t = p
    h, w, c = image.shape
    
    lab = color.rgb2lab(image)
    
    for y in range(h):
        lmax = np.max(lab[y,:,0])
        lavg = np.mean(lab[y,:,0])
        saw = ( (y + 25*t) % 25 )*0.15
        shift = int( (lavg*0.1 + lmax*0.15)*a + rand()*5 + saw )
    
        lab[y,:,:1] = np.roll(lab[y,:,:1], shift, 0)
        lab[y,:,2] = np.roll(lab[y,:,2], -shift//2, 0)
        
        lab[y,:,0] -= lmax * ( (1.5 ** a) - 1 )
        lab[y,:,0] *= ((a * 0.8) + 1.0)
        lab[y,:,0] += (a*5) - 1
        
        lab[y,:,1] += lmax * 0.2 * a
        lab[y,:,2] += lmax * 0.5 * a
    
    for x in range(w):
        lmax = np.max(lab[:,x,0])
        #shift = int(lmax*0.5*b + random.random()*2)
        #lab[:,x] = np.roll(lab[:,x], shift, 0)
        lab[:,x,0] += lmax * ( (1.4 ** b) - 1 )
        lab[:,x,1] -= lmax * 0.2 * b
        lab[:,x,2] -= lmax * 0.3 * b
    
    
    rgb = color.lab2rgb(lab)
    rgb = np.clip(rgb, 0, 1)
       
    if colors:
        rgb_scaled = (rgb*255).astype('uint8')  
        mod = Image.fromarray(rgb_scaled)
        mod = mod.convert('P', palette=Image.ADAPTIVE, colors=colors)
        if pil == True:
            return mod
        else:
            mod = mod.convert('RGB')
            pix = np.array(mod)
            return pix
    elif pil == True:
        rgb_scaled = (rgb*255).astype('uint8')  
        mod = Image.fromarray(rgb_scaled)
        return mod
    else:
        return rgb



def get_frames(im):
    '''converts a PIL gif Image into a list of frame Images'''
    frames = []
    lut = [1] * 256
    lut[im.info["transparency"]] = 0
    try:
        i= 0
        im.seek(i)
        first = im.copy()
        while 1:
            im.seek(i)
            mask = im.point(lut, "1")
            if i == 0: 
                palette = im.getpalette()
            else:
                im.putpalette(palette)
            first.paste(im, None, mask)
            frames.append( first )
            i += 1
    except EOFError:
        return frames
    
if __name__ == '__main__':
    ingif = Image.open('input/boxes.gif')
    print('frame duration: %f'% ingif.info['duration'])

    #frames = [ np.array(frame) for frame in get_frames(ingif)]
    n = len(frames)
    print('frames in original: ' + str(n))

    out = []

    for i, frame in enumerate(frames):
        t = float(i)/n
        
        a = (-cos( t*2*pi ) + 1) * 0.1
        a += rand() * 0.22
        
        b = (-cos( t*2*pi + 2 ) + 1) * 0.05
        b += (rand() * 0.4) - 0.2
        
        f = fuckwith(frame, (a,b,t), colors=80)
        out.append(f)
        print(i, end=' ')

    savenum = raw_input('file name? ')
    path = 'output/%i.gif' % savenum
    images2gif.writeGif(path, out, duration=0.03)
    print('saved to ' + path)
    savenum += 1

    fuckwith(frames[5], (0.5, 0.5, 1), pil=True, colors=80)
