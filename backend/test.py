from io import BytesIO
from PIL import Image
from scipy import linalg
from skimage import io, img_as_float, img_as_uint
import numpy as np
from sklearn.cluster import KMeans

file = open("wikipedia.png", "rb").read()
file = BytesIO(file)

original_image = np.array(Image.open(file).convert("L"))
shape = original_image.shape
image = original_image.reshape(-1, 1)

"""
kmeans = KMeans(n_clusters=8).fit(image)
centers = sorted(map(int, list(kmeans.cluster_centers_.flatten())))
print(centers)
"""

#means = [8, 66, 211, 252]
#_means = list(range(256))
#_means = [0, 23, 55, 104, 166, 215, 236, 254]
#_means = [0, 10, 23, 46, 56, 64, 73, 81, 89, 102, 109, 119, 129, 140, 152, 160, 168, 174, 179, 188, 198, 204, 211, 217, 221, 226, 230, 233, 236, 244, 250, 254]
_means = [0, 255]
means = np.array(_means).reshape(-1, 1)

X = np.array(list(range(8))).reshape(-1, 1)
kmeans = KMeans().fit(X)
kmeans.cluster_centers_ = means

image = kmeans.predict(image).reshape(shape)

U, S, V = linalg.svd(image)
k = 100

parts = [U[:,:k], S[:k], V[:k,:]]

image = np.matrix(parts[0]) * np.diag(parts[1]) * np.matrix(parts[2])
image = ((image - np.min(image)) / (np.max(image) - np.min(image))) * (len(_means) - 1)

print("here")

for r in range(shape[0]):
	print(r)
	for c in range(shape[1]):
		v = int(image[r, c])
		try:
			image[r, c] = _means[v]
		except:
			raise ValueError(v)

image = ((image - np.min(image)) / (np.max(image) - np.min(image)))

io.imsave("test.png", image)

