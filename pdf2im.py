import os
from wand.image import Image, Color


def pdf_to_jpg(pdf_path,  output_path = None, resolution = 200):

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    if not output_path:
        output_path = os.path.dirname(pdf_path)
    if (not os.path.exists(output_path)) and (output_path!='') and (not os.path.isdir(output_path)):
        os.mkdir(output_path)
        with Image(filename=pdf_path, resolution=resolution) as  pdf:
            for n, page in enumerate(pdf.sequence):
                with Image(page) as image:
                    image.format = 'jpg'
                    image.background_color = Color('white')
                    image.alpha_channel = 'remove'
                    image_name = os.path.join(output_path, 'pag{}.jpg'.format(n))
                    image.save(filename = image_name)
    else:
        print "el directorio destino ya existe o el nombre de dicho dir en ''"
        print "ruta :"+output_path+"."