#!/usr/bin/env python

from __future__ import print_function
import pyglet
from pyglet.gl import *
from PIL import Image
from math import sin, cos, pi
from random import random as rand
from sys import argv
from shader import Shader
from mystery import fuckwith


def pyglet_to_pil(pyglet_image):
    i = pyglet_image.get_image_data()
    pil_image = Image.frombuffer(i.format, (i.width, i.height), i.data, 'raw', i.format, 0, 0)
    return pil_image

def pil_to_pyglet(pil_image):
    w, h = pil_image.size
    mode = pil_image.mode
    img_data = pil_image.tostring()
    pyglet_image = pyglet.image.ImageData(w, h, mode, img_data)
    return pyglet_image


class W(pyglet.window.Window):
    def __init__(self, sprite):
        super(W, self).__init__()
        self.mouse = [0,0]
        self.sprite = sprite
        self.shader = Shader(open('pass.vert').read(), open('RGB2Lab.glsl').read())

    def on_draw(self):
        x, y = self.mouse
        # glEnable(GL_LINE_SMOOTH)
        # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # glOrtho(-1., 1., 1., -1., 0., 1.)

        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        self.shader.bind()
        self.sprite.draw()

        #self.shader.uniformf('C', *self.C)

        self.shader.unbind()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse = [x, y]

    def on_mouse_press(self, x, y, buttons, modifiers):
        # capture window contents to buffer
        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        image = pyglet_to_pil(buf)
        image.show()
    

def main():
    default = 'input/keyboard.gif'
    input_path = argv[1] if len(argv) > 1 else default
    animation = pyglet.resource.animation(input_path)
    animation.frames = animation.frames[:3]

    print('fucking with %i frames: ' % len(animation.frames))

   # for i in range(len(animation.frames)):
   #     t = float(i)/len(animation.frames)

   #     a = (-cos( t*2*pi ) + 1) * 0.1
   #     a += rand() * 0.22
   #     
   #     b = (-cos( t*2*pi + 2 ) + 1) * 0.05
   #     b += (rand() * 0.4) - 0.2

   #     pilframe = pyglet_to_pil(animation.frames[i].image)
   #     fuckedframe = fuckwith(pilframe, (a,b,t), colors=80)
   #     image = pil_to_pyglet(fuckedframe.convert('RGBA'))

   #     animation.frames[i] = pyglet.image.AnimationFrame(image, 0.03)
   #     print(str(i))

    sprite = pyglet.sprite.Sprite(animation)
    print('target: %s' % sprite.image.frames[0].image.get_texture().target)
    print('id: %s' % sprite.image.frames[0].image.get_texture().id)


    window = W(sprite)
    pyglet.app.run()

if __name__ == '__main__':
    main()
