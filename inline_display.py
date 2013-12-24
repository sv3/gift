import Image
from IPython.core import display
from io import BytesIO

def display_pil_image(im):
    """displayhook function for PIL Images, rendered as PNG"""
    b = BytesIO()
    im.save(b, format='png')
    data = b.getvalue()

    ip_img = display.Image(data=data, format='png', embed=True)
    return ip_img._repr_png_()

# register display func with PNG formatter:
png_formatter = get_ipython().display_formatter.formatters['image/png']
png_formatter.for_type(Image.Image, display_pil_image)
