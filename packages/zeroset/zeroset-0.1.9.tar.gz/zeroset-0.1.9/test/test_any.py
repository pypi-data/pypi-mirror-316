# from zeroset import py0
# import numpy as np
# import sys
#
# a = np.zeros((300, 300, 3), dtype=np.uint8)
#
# print(py0.get_value_size(a))
#
# print(py0._format_file_size(sys.getsizeof(a)))

from zeroset import log0
import zlib
import base64

# data = "pypi-AgEIcHlwaS5vcmcCJGNlNzMyM2Q1LTJiYmEtNGIxYi04NTkzLTk5YzBiZWFjYTk0YQACKlszLCI2MTkyZDBhMi04M2RmLTQxNzctOTkxOC02NDNjYTA2Mzc5Y2IiXQAABiDPreUmR1FX26oZDUvdOWzybob_Bvom5rmXejVVliI5Mw"
# compress_data = zlib.compress(data.encode(encoding='utf-8'), level=9)
# key_data = base64.b64encode(compress_data).decode()
#
# compress_data = base64.b64decode(key_data.encode())
#
# org_data = zlib.decompress(compress_data).decode('utf-8')
# print(org_data)
# print(len(org_data))  # 350000 출력
#
import cv2

img = cv2.imread("C:/Users/spring/Documents/git/zeroset/data/computer04.jpg")
mask = cv2.imread("C:/Users/spring/Documents/git/zeroset/data/computer04_mask.png", cv2.IMREAD_GRAYSCALE)
mask[mask != 0] = 255
mask_3channel = cv2.merge([mask, mask, mask])
img_masked = cv2.bitwise_and(img, mask_3channel)

b, g, r = cv2.split(img_masked)
img_png = cv2.merge([b, g, r, mask])
cv2.imwrite("computer_4ch.png", img_png)
