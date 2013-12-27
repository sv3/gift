#!/usr/bin/env python

from __future__ import print_function
import pyglet
from pyglet.gl import *
import Image
from mystery import fuckwith


def pyglet_to_pil(pyglet_image):
    i = pyglet_image.get_image_data()
    pil_image = Image.frombuffer(i.format, (i.width, i.height), i.data,
                'raw', i.format, 0, 0)
    return pil_image

def pil_to_pyglet(pil_image):
    w, h = pil_image.size
    mode = pil_image.mode
    img_data = pil_image.tostring()
    pyglet_image = pyglet.image.ImageData(w, h, mode, img_data)
    return pyglet_image


animation = pyglet.resource.animation('input/boxes.gif')
animation.frames = animation.frames[:4]

print('fucking with %i frames: ' % len(animation.frames))

for i in range(len(animation.frames)):
    pilframe = pyglet_to_pil(animation.frames[i].image)
    fuckedframe = fuckwith(pilframe, (0.5, 0.5, 1), pil=True, colors=80)
    image = pil_to_pyglet(fuckedframe.convert('RGBA'))

    animation.frames[i] = pyglet.image.AnimationFrame(image, 0.03)
    print(str(i))

sprite = pyglet.sprite.Sprite(animation)


class W(pyglet.window.Window):
    def __init__(self):
        super(W, self).__init__()
        self.mouse = [0,0]

    def on_draw(self):
        x, y = self.mouse
        sprite.draw()
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        pyglet.gl.glColor4f(1.0,0,0,1.0)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', (10, 15, x, y))
        )

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse = [x, y]

    def on_mouse_press(self, x, y, buttons, modifiers):
        # capture window contents to buffer
        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        image = pyglet_to_pil(buf)
        image.show()
    

window = W()
pyglet.app.run()
