from zeroset import cv0
import cv2
from zeroset import py0
from zeroset import viz0
import sys


def test_func():
    print(sys._getframe().f_code.co_name)
    print(py0.get_function_name())
    return
    files = cv0.glob("../data/", ["*.jpg", "*.png"])
    images = cv0.imreads(files)

    cv0.imshow(images, mode=cv0.IMSHOW.TK).waitESC()
    # print(*dir(list()), sep="\n")

    print("Hello")


import os
from glob import glob
import shutil
import pdf2image
import logging
import time

logging.disable(logging.DEBUG)


def pdf2img(file, save_as_zip=False):
    def generator():
        count = 0
        name = os.path.splitext(os.path.basename(file))[0]
        while True:
            output = f'{name}_{count:04d}'
            count += 1
            yield output

    basedir = os.path.dirname(file)
    basename, _ = os.path.splitext(os.path.basename(file))

    dirname = f'{basedir}/{basename}'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    else:
        raise Exception(f'{dirname} already exists')
    pdf2image.convert_from_path(file, fmt='png', output_folder=dirname, first_page=0, output_file=generator())
    if save_as_zip:
        zipname = shutil.make_archive(basename, "zip", root_dir=dirname)
        shutil.move(zipname, basedir)
        shutil.rmtree(dirname)
    return True


def img2pdf(dirname):
    files = glob(f'{dirname}/*.jpg') + glob(f'{dirname}/*.png')
    files.sort()

    imgs = [cv0.imread(file) for file in files]
    imgs = [cv0.resize(img, width=1600) for img in imgs]
    imgs = [cv0.to_pil(img) for img in imgs]

    dst = os.path.join(os.path.dirname(dirname), os.path.basename(dirname) + ".pdf")
    imgs[0].save(dst, save_all=True, append_images=imgs[1:])


def test():
    #pdf2img("C:/Users/spring/Documents/Paper/SmoothQuant(Accurate and Efficient Post-Training Quantization for Large Language Models).pdf", False)
    pass

if __name__ == '__main__':
    test()
