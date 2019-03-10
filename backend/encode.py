from io import BytesIO
from PIL import Image
from scipy import linalg
from skimage import io, img_as_float, img_as_uint
import numpy as np
from sklearn.cluster import KMeans
import base64
import skimage.measure

def compress_image(src_image):
    file = BytesIO(src_image)

    image_file = Image.open(file).convert("L")
    original_image = np.array(image_file)
    original_image = skimage.measure.block_reduce(original_image, (3,3), np.average)
    shape = original_image.shape
    image = original_image.reshape(-1, 1)

    #means = [8, 66, 211, 252]
    #_means = list(range(256))
    _means = [0, 23, 55, 104, 166, 215, 236, 254]
    #_means = [0, 10, 23, 46, 56, 64, 73, 81, 89, 102, 109, 119, 129, 140, 152, 160, 168, 174, 179, 188, 198, 204, 211, 217, 221, 226, 230, 233, 236, 244, 250, 254]
    means = np.array(_means).reshape(-1, 1)

    X = np.array(list(range(8))).reshape(-1, 1)
    kmeans = KMeans().fit(X)
    kmeans.cluster_centers_ = means

    image = kmeans.predict(image).reshape(shape)

    for r in range(shape[0]):
        for c in range(shape[1]):
             v = int(image[r, c])
             image[r, c] = _means[v]

    image = ((image - np.min(image)) / (np.max(image) - np.min(image))) 

    result = BytesIO()
    io.imsave(result, image)
    result = base64.b64encode(result.getvalue());
    return result

def compress(jsontable, encoded_image):
    encoded = base64.b64decode(encoded_image.encode("ascii"))
    compressed =  compress_image(encoded).decode("ascii")
    jsontable["i"] = compressed
