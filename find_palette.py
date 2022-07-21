import tweepy
import yaml
import requests
import cv2 as cv
import numpy as np
import PIL
import matplotlib.pyplot as plt
from skimage import io
from sklearn.cluster import KMeans

def make_histogram(cluster):
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist

def get_rgb(color):
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return (red, green, blue)

def palette(height, width, clusters):
    palette = []
    steps = width/clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_):
        palette.append(centers)
    return palette

def find_palette(img):
    height, width, _ = np.shape(img)
    image = img.reshape((height * width, 3))

    num_clusters = 4
    clusters = KMeans(n_clusters=num_clusters)
    clusters.fit(image)
    p = palette(height, width, clusters)
    #print(p)

    colors = []
    for color in p:

        rgb = get_rgb(color)
        #print(f'  RGB values: {rgb}')
        colors.append(rgb)

    #k.fit(image.reshape(-1,3))
    # TODO: create class that takes in image data and calculates and returns color palette
    return colors

# def check_for_changes(since_id) # since_id represents the last tweet that was recieved.

def url_from_image_link(link):
    img = io.imread(link)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    palette = find_palette(img)
    color_code = hex_to_code(palette)
    palette_url = get_palette_url(color_code)
    print(palette_url)
    return palette_url

def url_from_image(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    palette = find_palette(img)
    color_code = hex_to_code(palette)
    palette_url = get_palette_url(color_code)
    print(palette_url)
    return palette_url

def combine_images():
    # TODO: take in multiple images and return a concat of them togethor
    return

def save_last_response(last_id):
    cfg["stats"]["last_response"] = last_id
    with open("settings.conf", "w") as ymlfile:
        yaml.dump(cfg, ymlfile, default_flow_style=False)

def get_palette_url(color_code):

    url = "https://colorhunt.co/php/create.php"

    payload='code=' + color_code
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    link = "https://colorhunt.co/palette/" + color_code
    return(link)

def hex_to_code(colors):
    color_code = ""
    for color in colors:
        color_code += str(rgb_to_hex(color))
    return color_code
    #print("Colors: " + str(code[0]))

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

#url_from_image_link("https://pbs.twimg.com/media/FX9uB4DWYAACaQb.jpg")

# PSEUDOCODE:
# get list of mentions since last check

# for each new mention, see how many images are tweeted

# if more than one, concat the images togethor to make full frame image

# for the final image, calculate the most common colors used

# with the new list of colors, generate new palette on a website

# tweet response to original request with new link
