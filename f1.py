from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import crop
from skimage import exposure
from skimage.color import rgb2gray
from skimage.transform import radon, rotate, resize, swirl
from skimage.filters import unsharp_mask, meijering, sato, threshold_yen, window,threshold_otsu, sobel,roberts, prewitt_v, prewitt_h
from skimage.morphology import erosion, dilation, opening, closing, white_tophat, black_tophat, skeletonize, convex_hull_image, disk, remove_small_holes
import cv2
import io
import base64

#arayüzde resim gösterme methodu
def gui_images(file_or_bytes, resize=None):

    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


#uzaysal dönüşüm işlemleri
#radon işlemi
def radon_u(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    theta = np.linspace(0., 180., max(image.shape), endpoint=False)
    image = radon(image, theta=theta, circle=True)
    plt.imsave(path, image, cmap = 'gray')
    return path

#swirl işlemi
def swirl_u(path):
    image = np.asarray(Image.open(path))
    image = swirl(image, rotation=0, strength=250, radius=120)
    plt.imsave(path, image, cmap = 'gray')
    return path

#döndürme işlemi sırasında döndürülecek derece kullanıcıdan alınmaktadır
def rotate_u(path, derece):
    image = np.asarray(Image.open(path))
    image = rotate(image, int(derece))
    plt.imsave(path, image, cmap = 'gray')
    return path

#yeniden boyutlandırma işleminde büyüklükler kullanıcıdan alınmaktadır
def resize_u(path, a, b):
    image = np.asarray(Image.open(path))
    image = resize(image,(int(a), int(b)))
    plt.imsave(path, image, cmap = 'gray')
    return path

#kırpma işlemi
def crop_u(path):
    image = np.asarray(Image.open(path))
    image = crop(image, ((50, 50), (50, 50), (0, 0)), copy=False)
    plt.imsave(path, image, cmap = 'gray')
    return path

#yoğunluk dönüşümü işlemi
def rescale_y(path, min, max):
    image = np.asarray(Image.open(path))
    image = exposure.rescale_intensity(image, in_range=(min, max))
    plt.imsave(path, image)
    return path

#histogram işlemleri
def hist_equalize(path):
    image = np.asarray(Image.open(path))
    image = exposure.equalize_hist(image)

    c = plt.hist(image.ravel(), bins=256, histtype='step', color='black')
    plt.imsave(path, image)
    return path, c

def show_histo(path,histo):
    image = np.asarray(Image.open(path))
    image = exposure.equalize_hist(image)
    histo = plt.hist(image.ravel(), bins=256, histtype='step', color='black')
    plt.ylim([0, 20000])
    plt.show()

#filtreler
#sobel işlemi
def sobel_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = sobel(image)
    plt.imsave(path, image, cmap = 'gray')
    return path

#roberst işlemi
def roberts_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = roberts(image)
    plt.imsave(path, image, cmap = 'gray')
    return path

#window işlemi
def windowed_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = image * window('hann', image.shape)
    plt.imsave(path, image, cmap = 'gray')
    return path

#unsharp işlemi
def unsharp_f(path):
    image = np.asarray(Image.open(path))
    image = unsharp_mask(image, radius=5, amount=2)
    plt.imsave(path, image)
    return path

#prewitt_v işlemi
def prewitt_v_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = prewitt_v(image, mask=None)
    plt.imsave(path, image, cmap = 'gray')
    return path

#prewitt_h işlemi
def prewitt_h_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = prewitt_h(image, mask=None)
    plt.imsave(path, image, cmap = 'gray')
    return path

#sato işlemi
def sato_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = sato(image, sigmas=range(1, 10, 2), black_ridges=True, mode=None, cval=0)
    plt.imsave(path, image, cmap = 'gray')
    return path

#meijering işlemi
def meijering_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = meijering(image, sigmas=range(1, 10, 2), alpha=None, black_ridges=True, mode='reflect', cval=0)
    plt.imsave(path, image, cmap = 'gray')
    return path

#threshold_otsu işlemi
def threshold_otsu_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    thresh = threshold_otsu(image)
    binary = image > thresh
    plt.imsave(path, binary, cmap = 'gray')
    return path

#threshold_yen
def threshold_yen_f(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    thresh = threshold_yen(image)
    binary = image <= thresh
    plt.imsave(path, binary, cmap='gray')
    return path


#morfolojik işlemler
#morfolojik opening işlemi
def opening_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = opening(image,disk(4))
    plt.imsave(path, image, cmap='gray')
    return path

#morfolojik closing işlemi
def closing_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = closing(image, disk(4))
    plt.imsave(path, image, cmap='gray')
    return path

#erosion işlemi
def erosion_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = erosion(image, disk(4))
    plt.imsave(path, image, cmap='gray')
    return path

#dilation işlemi
def dilation_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = dilation(image, disk(4))
    plt.imsave(path, image, cmap='gray')
    return path

#white_tophat işlemi
def white_tophat_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = white_tophat(image, disk(4))
    plt.imsave(path, image, cmap='gray')
    return path

#black_tophat işlemi
def black_tophat_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = black_tophat(image, disk(4))
    plt.imsave(path, image, cmap='gray')
    return path

#skeletonize işlemi
def skeletonize_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = skeletonize(image == 0)
    plt.imsave(path, image, cmap='gray')
    return path

#convex_hull işlemi
def convex_hull_m(path):
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = convex_hull_image(image)
    plt.imsave(path, image, cmap='gray')
    return path

#gradient işlemi
def gradient_m(path):
    kernel = np.ones((5, 5), np.uint8)
    image = np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = cv2.morphologyEx(image,cv2.MORPH_GRADIENT, kernel)
    plt.imsave(path, image, cmap='gray')
    return path

#remove small holes işlemi
def remove_small_holes_m(path):
    image = np.asarray(Image.open(path))
    #image = rgb2gray(image)
    image = remove_small_holes(image,150)
    image = opening(image,disk(3))
    plt.imsave(path, image, cmap='gray')
    return path

#gizemli filtre
def gizem_f(path):
    image =np.asarray(Image.open(path))
    image = rgb2gray(image)
    image = swirl(image, rotation=0, strength=250, radius=120)
    image = image * window('hann', image.shape)
    plt.imsave(path,image, cmap='jet')
    return path

#video filtreleri

def canny_v(path, fourcc, fps, fw, fh, cap):
    out = cv2.VideoWriter(path, fourcc, fps, (fw, fh), False)
    while (cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:
            frame = cv2.Canny(frame, 25, 75)
            out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

            # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def flip_v(path, fourcc, fps, fw, fh, cap):
    out = cv2.VideoWriter(path, fourcc, fps, (fw, fh))
    while (cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 0)
            out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def blur_v(path, fourcc, fps, fw, fh, cap):
    out = cv2.VideoWriter(path, fourcc, fps, (fw, fh))
    while (cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:
            frame = cv2.GaussianBlur(frame, (7, 7), 1.41)
            out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

            # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def hue_v(path, fourcc, fps, fw, fh, cap):
    out = cv2.VideoWriter(path, fourcc, fps, (fw, fh))
    while (cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += 15
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            out.write(frame)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

            # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()