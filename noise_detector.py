import cv2
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('images/noisy_image.jpg', cv2.IMREAD_GRAYSCALE)

# Calculate and plot histogram
plt.hist(image.ravel(), bins=256, range=(0, 255), histtype='step')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.title('Histogram of Pixel Intensities')
plt.show()

