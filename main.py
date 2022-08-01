import pygame as py
import io
import numpy as p
import timeit
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

py.font.init()

cid = 'l'
secret = 'l'
client_credentials_manager = SpotifyClientCredentials(client_id ='e18f6a4d32594600b9f61fb6bff6c78d', client_secret = 'beb73937270a460188f7f2245a4aaafe')
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)


#controlls size of the window
WIDTH, HEIGHT = 1280, 720
flags = py.SCALED
win = py.display.set_mode((WIDTH, HEIGHT), flags)

#name of the display
py.display.set_caption("spotyRanker")
WHITE = (255, 255, 255)

#Frames per second control variable
FPS = 60

#color palette
DARK_GREENISH_BLUE = (5, 102, 141)
GREENISH_BLUE = (2, 128, 144)
GREEN = (0, 168, 150)
LIGHT_GREEN = (2, 195, 154)
CREAM = (240, 243, 189)

#Fonts
BIG_FONT = py.font.SysFont('impact', 20)
BIGGER_FONT = py.font.SysFont('impact', 25)
BIGGER_FONT_B = py.font.SysFont('impact', 25)
BIGGER_FONT_B.set_bold(True)


class button:
    def __init__(self, x, y, font, title, color):
        self.x = x
        self.y = y
        self.title = title
        self.font = font
        self.sprite = font.render(title, 1, CREAM)
        self.color = color
        self.width = len(title) * 10
        self.height = 30
        self.rect = py.Rect(self.x - 5, self.y, self. width, self.height)
        self.clicked = False

    def draw(self, win):
        self.isPressed()
        py.draw.rect(win, self.color, self.rect)
        win.blit(self.sprite,(self.x, self.y))

    def isHovered(self):
        pos = py.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.sprite = self.font.render(self.title, 1, DARK_GREENISH_BLUE)
        else:
            self.sprite = self.font.render(self.title, 1, CREAM)

    def isPressed(self):
        pos = py.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if py.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

            if py.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

    def changeTitle(self, title):
        self.title = title
        self.sprite = self.sprite = self.font.render(title, 1, CREAM)

#stats box
statBox = [BIGGER_FONT.render('Sort :', True, DARK_GREENISH_BLUE) ,
           BIGGER_FONT.render('Time :', True, DARK_GREENISH_BLUE),
           BIGGER_FONT.render('comparisons: ', True, DARK_GREENISH_BLUE)]


mergeButton = button(30, 100, BIG_FONT, 'Merge Sort', GREEN)
boxButton = button(170, 100, BIG_FONT, 'Box Sort', GREEN)

metricButton = button(50, 140, BIG_FONT, 'Sort BY...', GREEN)
DropDownBox = button(130, 140, BIGGER_FONT_B, ' > ', GREEN)

buttons = [mergeButton, boxButton, metricButton, DropDownBox]

metrics = ['ID', 'danceability', 'valence', 'url', 'loudness',
                 'speechiness', 'energy', 'instrumentalness', 'liveness', 'tempo', 'popularity']

dropList = []
for i in range(len(metrics)):
    dropList.append(button(160, 140 + 30 * i, BIG_FONT, metrics[i], GREEN))
    dropList[i].width = 160
    dropList[i].rect = py.Rect(dropList[i].x - 5, dropList[i].y, 160, dropList[i].height)


class Song:



    def __init__(self, x , y, ID, danceability, valence, url, loudness,
                 speechiness, energy, instrumentalness, liveness, tempo, popularity):
        self.x = x
        self.y = y
        self.ID = ID
        self.dancebility = danceability
        self.valence = valence
        self.url = url
        self.loudness = loudness
        self.speechiness = speechiness
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.tempo = tempo
        self.popularity = popularity


class Track:
    def __init__(self, x, y, width, height, URL, metric):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.metric = metric
        self.color = DARK_GREENISH_BLUE
        image_url = URL
        image_str = urlopen(image_url).read()
        image_file = io.BytesIO(image_str)
        self.image = py.image.load(image_file)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        py.draw.rect(win, self.color, (self.x + 64, self.y + 44, self.width, self.height))
    def setPosition(self, num):
        self.y = num

    def check(self):
            self.color = CREAM

    def finished(self):
            self.color = LIGHT_GREEN

    def match(self):
            self.color = GREEN

    def back(self):
        self.color = CREAM

def loadPlaylist(metric, track):
    playlist = []

    for i in range(len(track)):
        playlist.append(Track(0, 0, 64, 20, str(sp.track(track[i])['album']['images'][2]['url']),
                              sp.audio_features(track[i])[0][metric]))

    return playlist


playlist2021 = sp.playlist_tracks('spotify:playlist:37i9dQZF1DX18jTM2l2fJY')

id_list = []
song_list = []

# makes the id list

for track in playlist2021['items'][:100]:
    id_list.append(track['track']['id'])
"""
for track in id_list[:100]:
    print(track)
    song_list.append(Song(0,
                          0,
                          track,
                          sp.audio_features(track)[0]['danceability'],
                          sp.audio_features(track)[0]['valence'],
                          str(sp.track(track)['album']['images'][2]['url']),
                          sp.audio_features(track)[0]['loudness'],
                          sp.audio_features(track)[0]['speechiness'],
                          sp.audio_features(track)[0]['energy'],
                          sp.audio_features(track)[0]['instrumentalness'],
                          sp.audio_features(track)[0]['liveness'],
                          sp.audio_features(track)[0]['tempo'],
                          sp.track(track)['popularity']))

"""


trackList = loadPlaylist('energy', id_list)


test = Track(600, 400, 64,20, 'https://i.scdn.co/image/ab67616d0000485141720ef0ae31e10d39e43ca2', 'id')

def draw_window(win, visible):

    win.fill(GREEN)
    py.draw.rect(win, GREENISH_BLUE, (0, 0,300, 720))

    py.draw.rect(win, LIGHT_GREEN, (0, 400, 300, 320))
    py.draw.rect(win, CREAM, (40, 440, 220, 240))

    for i in range(len(statBox)):
        win.blit(statBox[i], (50, 440 + 25 * i))

    if visible:
        for i in range(len(metrics)):
            if dropList[i].isPressed():
                buttons[2].changeTitle(dropList[i].title)

        for i in dropList:
            i.draw(win)
            i.isHovered()

    for i in buttons:
        i.draw(win)
        i.isHovered()

    test.draw(win)

    z = 0
    space = 0
    for t in trackList:
        t.x = 330 + space
        t.y = 5 + 64 * z
        z += 1
        if z == 11:
            space += 138
            z = 0

        t.draw(win)

    py.display.update()

def main():
    #fps control
    clock = py.time.Clock()
    visible = False
    game = True
    while game:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                game = False
            if event.type == py.MOUSEBUTTONDOWN:

                if DropDownBox.isPressed():
                   if not visible:
                       visible = True
                   else:
                       visible = False


        draw_window(win, visible)
    py.quit()


# begin merge sort
# begin code citation: sorting powerpoint slides 89 - 90
def mergeSort(arr, left, right):
    if left < right:
        # calculate the middle section of the array
        middle = left + (right - left) // 2

        # sort first half and second half
        mergeSort(arr, left, middle)
        mergeSort(arr, middle + 1, right)

        # merge all subarrays
        merge(arr, left, middle, right)

def merge(arr, left, middle, right):
    # create new subarrays
    n1 = middle - left + 1
    n2 = right - middle

    sub1 = [0] * n1
    sub2 = [0] * n2

    # Copy data into subarrays
    for i in range(n1):
        sub1[i] = arr[left + i]

    for j in range(n2):
        sub2[j] = arr[middle + 1 + j]

    i = 0
    j = 0
    final = left

    # sort and merge subarrays into one array
    while i < n1 and j < n2:
        if sub1[i] <= sub2[j]:
            arr[final] = sub1[i]
            i = i + 1
        else:
            arr[final] = sub2[j]
            j = j + 1
        final = final + 1

    # copy any remaining elements into array
    while i < n1:
        arr[final] = sub1[i]
        i = i + 1
        final = final + 1

    while j < n2:
        arr[final] = sub2[j]
        j = j + 1
        final = final + 1
# end code citation: sorting powerpoint slides 89 - 90


arr = [12.5, 11.0, 13.5, 5.5, 6.5, 7.5]
#arr = ["1YieJ8UoB4t4w8Ua0N3nGv", "1mw0RgNXIpYRyyCdBQbLgA", "17RA3JGafJm5zRtKJiKPIm", "1R2kfaDFhslZEMJqAFNpdd"]
size = len(arr)
print("Original Array")
for i in range(size):
    print(arr[i])

mergeSort(arr, 0, size - 1)
print("\n\nSorted Array")
for i in range(size):
    print(arr[i])
    #print(py.font.get_fonts())
# end merge sort

if __name__ == "__main__":
    main()