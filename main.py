import random
import concurrent.futures
import pygame as py
import io
import numpy as p
import spotipy
import time

clock = time
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
WIDTH, HEIGHT = 1920, 1080
flags = py.RESIZABLE
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
BIGGEST_FONT = py.font.SysFont('impact', 35)
SMALL_FONT = py.font.SysFont('impact', 15)
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

class checkList:
    def __init__(self, x, y, Genres):
        self.x = x
        self.y = y
        self.boxes = []
        self.box_mask = []
        self.spacerx = 0
        self.spacery = 35
        self.mark = BIGGER_FONT.render('X', True, CREAM)
        scaler = 0
        for i in range(6):
            self.boxes.append(py.Rect(x + self.spacerx, y + self.spacery * scaler, 20, 25))
            self.box_mask.append(False)
            print(len(self.boxes))
            scaler += 1
        self.titles = []
        for i in Genres:
            self.titles.append(SMALL_FONT.render(i, True, CREAM))
    def draw(self, win):
        for i in range(len(self.boxes)):
            py.draw.rect(win, GREEN, self.boxes[i])
            win.blit(self.titles[i], (self.boxes[i].x + 30, self.boxes[i].y + 5))
            if self.box_mask[i]:
                win.blit(self.mark, (self.boxes[i].x + 3, self.boxes[i].y - 4))


    def isHovered(self, win):
        pos = py.mouse.get_pos()
        for i in range(len(self.boxes)):
            if self.boxes[i].collidepoint(pos):
                win.blit(self.mark, (self.boxes[i].x + 3, self.boxes[i].y - 4))

    def isWholePressed(self):
        pos = py.mouse.get_pos()
        for i in range(len(self.boxes)):
            if self.boxes[i].collidepoint(pos):
                if py.mouse.get_pressed()[0] == 1:
                    return True
        return False


    def isPressed(self):
        pos = py.mouse.get_pos()
        for i in range(len(self.boxes)):
            if self.boxes[i].collidepoint(pos):
                if py.mouse.get_pressed()[0] == 1 and not self.box_mask[i]:
                    self.box_mask[i] = True
                    return self.box_mask
                if py.mouse.get_pressed()[0] == 1 and self.box_mask[i]:
                    self.box_mask[i] = False
                    return self.box_mask







Genres = ['hiphop', 'pop','country', 'jazz', 'top10','rock']

checkBox = checkList(50, 180, Genres)
#stats box
stat_titles = ['Sort: ', 'Time: ', 'comparisons: ']
statBox = [BIGGER_FONT.render('Sort :', True, DARK_GREENISH_BLUE) ,
           BIGGER_FONT.render('Time :', True, DARK_GREENISH_BLUE),
           BIGGER_FONT.render('comparisons: ', True, DARK_GREENISH_BLUE)]
sort = ''
Time = '0.0'
comparisons = '0'

stats = [BIGGER_FONT.render(sort, True, GREEN),
         BIGGER_FONT.render(Time, True, GREEN),
         BIGGER_FONT.render(comparisons, True, GREEN)]

metricButton = button(50, 140, BIG_FONT, 'Sort BY...', GREEN)
metricButton.rect = py.Rect(metricButton.x - 5, metricButton.y, 200, 30)
DropDownBox = button(230, 140, BIGGER_FONT_B, ' > ', GREEN)

#function buttons
mergeButton = button(30, 100, BIG_FONT, 'Merge Sort', GREEN)
boxButton = button(170, 100, BIG_FONT, 'Bucket Sort', GREEN)

#page scroll button
left_scroll = button(1840, 1000, BIG_FONT, ' < ', GREENISH_BLUE)
right_scroll = button(1870, 1000, BIG_FONT, ' > ', GREENISH_BLUE)

shuffle_Button = button(10, 30, BIGGEST_FONT, 'SHUFFLE', GREEN)
shuffle_Button.rect = py.Rect(shuffle_Button.x - 5, shuffle_Button.y, 120, 50)

load_Button = button(135, 30, BIGGEST_FONT, 'Load Songs', GREEN)
load_Button.rect = py.Rect(load_Button.x - 5, load_Button.y, 170, 50)


buttons = [mergeButton, boxButton, metricButton, DropDownBox, shuffle_Button, load_Button,left_scroll, right_scroll]

metrics = ['num_samples', 'num_artist','danceability', 'duration_ms','valence', 'url', 'loudness', 'available_markets', 'key_confidence',
                 'speechiness', 'energy', 'instrumentalness', 'liveness', 'tempo', 'popularity',
           'mode_confidence', 'acousticness', 'tempo_confidence', 'track_number']

dropList = []
for i in range(len(metrics)):
    dropList.append(button(260, 140 + 30 * i, BIG_FONT, metrics[i], GREEN))
    dropList[i].width = 260
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
        self.height = height
        self.metric = metric
        self.width = width
        self.color = DARK_GREENISH_BLUE

        #turning url into and image object
        image_url = URL
        image_str = urlopen(image_url).read()
        image_file = io.BytesIO(image_str)
        self.image = py.image.load(image_file).convert()
        self.image = py.transform.scale(self.image,(64, 64))


    def draw(self, win):
        py.draw.rect(win, self.color, (self.x, self.y, 68, 68))
        win.blit(self.image, (self.x + 2, self.y + 2))
        py.draw.rect(win, self.color, (self.x + 70, self.y + 50, self.width, self.height))
    def setPosition(self, num):
        self.y = num

    def check(self):
        self.color = CREAM

    def finished(self):
        self.color = LIGHT_GREEN

    def match(self):
        self.color = GREEN

    def back(self):
        self.color = DARK_GREENISH_BLUE

def loadPlaylist(metric, track, playlist):
    output_start = 0.0
    output_end = 100.0
    input_start = 0.0
    input_end = 1.0

    match (metric):
        case 'tempo':
            input_start = 60.0
            input_end = 200.0
        case 'loudness':
            input_start = -20.0
            input_end = 0.0
        case 'speechiness':
            input_start = 0.0
            input_end = 0.5
        case 'instrumentalness':
            input_start = 0.0
            input_end = 0.1
        case 'liveness':
            input_start = 0.0
            input_end = 0.8

    slope = (output_end - output_start)/(input_end - input_start)

    for i in range(len(track)):

        if metric == 'tempo_confidence' or metric == 'num_samples' or metric == 'key_confidence' or metric == 'mode_confidence':
            input = sp.audio_analysis(track[i])['track'][metric]
            n_width = int(output_start + slope * (input - input_start))
            playlist.append(Track(0, 0, n_width, 15, str(sp.track(track[i])['album']['images'][2]['url']),
                                  input))

        if metric == 'duration_ms' or metric == 'track_number' or metric == 'popularity':
            print('first')
            input = sp.track(track[i])[metric]
            n_width = int(output_start + slope * (input - input_start))
            playlist.append(Track(0, 0, n_width, 15, str(sp.track(track[i])['album']['images'][2]['url']),
                                  input))
        elif metric == 'num_artists':
            input = len(sp.track(track[i])['artists'][0]['id'])
            n_width = int(output_start + slope * (input - input_start))
            playlist.append(Track(0, 0, n_width, 15, str(sp.track(track[i])['album']['images'][2]['url']),
                                  input))
        elif metric == 'available_markets':
            input = len(sp.track(track[i])[metric])
            n_width = int(output_start + slope * (input - input_start))
            playlist.append(Track(0, 0, n_width, 15, str(sp.track(track[i])['album']['images'][2]['url']),
                                  input))
        else:
            input = sp.audio_features(track[i])[0][metric]
            n_width = int(output_start + slope * (input - input_start))
            playlist.append(Track(0, 0, n_width, 15, str(sp.track(track[i])['album']['images'][2]['url']),
                                  input))

        print(playlist[i].metric)

    #return playlist

def quickLoad(metric, track, songs):
    with concurrent.futures.ThreadPoolExecutor() as executer:
        temp = [executer.submit(loadPlaylist, metric, track[i], songs) for i in range(len(track))]

    print(songs)

    return songs

playlist2021 = sp.playlist_tracks('spotify:playlist:37i9dQZF1DX18jTM2l2fJY')

id_list = []
song_list = []

# makes the id list

for track in playlist2021['items'][:10]:
    id_list.append(track['track']['id'])

playlistIDS = ['37i9dQZF1DWVRSukIED0e9', '37i9dQZF1DX7Jl5KP2eZaS',
               '37i9dQZF1DX18jTM2l2fJY']

track_list = []
top10List = ['37i9dQZF1DX0yEZaMOXna3','37i9dQZF1DX3Sp0P28SIer','37i9dQZF1DX0h0QnLkMBl4','37i9dQZF1DX9ukdrXQLJGZ','37i9dQZF1DX8XZ6AUo9R4R',
             '37i9dQZF1DWTE7dVUebpUW','37i9dQZF1DXe2bobNYDtW8','37i9dQZF1DWVRSukIED0e9','37i9dQZF1DX7Jl5KP2eZaS', '37i9dQZF1DX18jTM2l2fJY']
hiphopList = ['37i9dQZF1DX0XUsuxWHRQd','37i9dQZF1DWTggY0yqBxES', '37i9dQZF1DX1lHW2vbQwNN', '37i9dQZF1DXaxIqwkEGFEh', '37i9dQZF1DXd43GfSFAeHA',
              '37i9dQZF1DWWIfrT204w7E', '37i9dQZF1DX9cjKvsL1KlZ', '37i9dQZF1DX2Q2blQJBfBS', '37i9dQZF1DX9sQDbOMReFI', '37i9dQZF1DWWAqc46ZJdZf']
popList = ['37i9dQZF1DXcBWIGoYBM5M', '37i9dQZF1DWWvvyNmW9V9a', '37i9dQZF1DWUa8ZRTfalHk', '37i9dQZF1DX5Vy6DFOcx00', '37i9dQZF1DX2L0iB23Enbq',
           '37i9dQZF1DWSqBruwoIXkA', '37i9dQZF1DX0b1hHYQtJjp',  '37i9dQZF1DXbcP8BbYEQaO', '37i9dQZF1DX2lVtkHKv2NU', '37i9dQZF1DX7iB3RCnBnN4']
countryList =['37i9dQZF1DX1lVhptIYRda', '37i9dQZF1DWUgBy0IJPlHq', '37i9dQZF1DXcSzYlwgjiSi', '37i9dQZF1DWVn8zvR5ROMB', '37i9dQZF1DWVpjAJGB70vU',
              '37i9dQZF1DXdxUH6sNtcDe', '37i9dQZF1DWYnwbYQ5HnZU', '37i9dQZF1DXbIbVYph0Zr5', '37i9dQZF1DX6RCydf9ytsj' , '37i9dQZF1DXa90jZU6E5GN']
rockList =['37i9dQZF1DWXRqgorJj26U', '37i9dQZF1DX3oM43CtKnRV', '37i9dQZF1DX1rVvRgjX59F', '37i9dQZF1DX1spT6G94GFC', '37i9dQZF1DWWwzidNQX6jx',
           '37i9dQZF1DWWzBc3TOlaAV', '37i9dQZF1DX9wa6XirBPv8', '37i9dQZF1DXb3m918yXHxA', '37i9dQZF1DX82Zzp6AKx64', '37i9dQZF1DWWGFQLoP9qlv']
jazzList = ['37i9dQZF1DX7YCknf2jT6s', '37i9dQZF1DXcWL5K0oNHcG', '37i9dQZF1DX8PhKVl4Zniv', '37i9dQZF1DWW2c0C8Vb2IR', '37i9dQZF1DWTR4ZOXTfd9K',
            '37i9dQZF1DWV7EzJMK2FUI', '37i9dQZF1DX0SM0LYsmbMT', '37i9dQZF1DXbITWG1ZJKYt', '37i9dQZF1DXdwTUxmGKrdN', '37i9dQZF1DX3bH0P2uDnWA']


def getSongs(options):
    temp = []
    tracks = []
    if options == 'top10':
        for i in range(0,10):
            pL = sp.playlist_tracks('spotify:playlist:' + top10List[i])
            for track in pL['items'][:100]:
                singleID = track['track']['id']
                temp.append(singleID)
            track_list.append(temp.copy())
            temp.clear()
            print(track_list)

    if options == 'hiphop':
        for i in range(0,10):
            pL = sp.playlist_tracks('spotify:playlist:' + hiphopList[i])
            for track in pL['items'][:100]:
                singleID = track['track']['id']
                temp.append(singleID)
            track_list.append(temp.copy())
            temp.clear()
    if options == 'pop':
        for i in range(0,10):
            pL = sp.playlist_tracks('spotify:playlist:' + popList[i])
            for track in pL['items'][:100]:
                singleID = track['track']['id']
                temp.append(singleID)
            track_list.append(temp.copy())
            temp.clear()
    if options == 'country':
        for i in range(0,10):
            pL = sp.playlist_tracks('spotify:playlist:' + countryList[i])
            for track in pL['items'][:100]:
                singleID = track['track']['id']
                temp.append(singleID)
            track_list.append(temp.copy())
            temp.clear()
    if options == 'rock':
        for i in range(0,10):
            pL = sp.playlist_tracks('spotify:playlist:' + rockList[i])
            for track in pL['items'][:100]:
                singleID = track['track']['id']
                temp.append(singleID)
            track_list.append(temp.copy())
            temp.clear()
    if options == 'jazz':
        for i in range(0,10):
            pL = sp.playlist_tracks('spotify:playlist:' + jazzList[i])
            for track in pL['items'][:100]:
                singleID = track['track']['id']
                temp.append(singleID)
            track_list.append(temp.copy())
            temp.clear()
    print(track_list)
    return track_list



test = Track(600, 400, 64,20, 'https://i.scdn.co/image/ab67616d0000485141720ef0ae31e10d39e43ca2', 'id')

def draw_songs(arr):
    for s in arr:
        s.draw()


def draw_window(win, visible, songList, start, end):
    win.fill(GREEN)
    py.draw.rect(win, GREENISH_BLUE, (0, 0,350, 720))

    py.draw.rect(win, LIGHT_GREEN, (0, 400, 350, 320))
    py.draw.rect(win, CREAM, (40, 440, 270, 240))

    for i in range(len(statBox)):
        win.blit(statBox[i], (60, 440 + 25 * i))
        size = py.font.Font.size(BIGGER_FONT, stat_titles[i])
        win.blit(stats[i], (size[0] + 65, 443 + 25 * i))

    checkBox.draw(win)
    checkBox.isHovered(win)


    if visible:
        for i in range(len(metrics)):
            if dropList[i].isPressed():
                songList.clear()
                buttons[2].changeTitle(dropList[i].title)
                songList = quickLoad(metrics[i], track_list, songList)
                #songList = songList[0].copy()
                print(len(songList))



        for i in dropList:
            i.draw(win)
            i.isHovered()

    for i in buttons:
        i.draw(win)
        i.isHovered()

    #test.draw(win)

    z = 0
    space = 0

    if end > len(songList):
        end = len(songList) - 1

    if len(songList) > 0:
        for t in range(start, end):
            songList[t].x = 360 + space
            songList[t].y = 5 + 70 * z
            z += 1
            if z == 14:
                space += 150
                z = 0

            songList[t].draw(win)

    py.display.update()
    return songList

def main():
    #fps control
    songList = []
    track_list = []
    start_index = 0
    end_index = 140
    clock = py.time.Clock()
    visible = False
    game = True
    while game:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                game = False
            if event.type == py.MOUSEBUTTONDOWN:
                if load_Button.isPressed():
                    if len(track_list) > 0:
                        track_list.clear()
                    for i in range(len(checkBox.boxes)):
                        if checkBox.box_mask[i]:
                            track_list = getSongs(Genres[i])
                    print(track_list)

                if left_scroll.isPressed() and not start_index == 0:
                    start_index -= 25
                    end_index -= 25
                if right_scroll.isPressed():
                    start_index += 25
                    end_index += 25

                if checkBox.isWholePressed():
                    checkBox.box_mask = checkBox.isPressed()
                if DropDownBox.isPressed():
                   if not visible:
                       visible = True
                   else:
                       visible = False
                if mergeButton.isPressed():
                    import time
                    sort = 'Merge Sort'
                    stats[0] = BIGGER_FONT.render(sort, True, GREEN)
                    start = time.time()
                    comparisons = str(mergeSort(songList, 0, len(songList) - 1, win, visible, start_index, end_index))
                    end = time.time()
                    stats[2] = BIGGER_FONT.render(comparisons, True, GREEN)
                    print(end - start)
                    time = str(round((end - start),2))
                    stats[1] = BIGGER_FONT.render(time, True, GREEN)
                if boxButton.isPressed():
                    import time
                    sort = 'Bucket Sort'
                    stats[0] = BIGGER_FONT.render(sort, True, GREEN)
                    start = time.time()
                    comparisons = str(bucketSort(songList, visible, win, start_index, end_index))
                    comparisons = str(bucketSort(songList, visible, win, start_index, end_index))
                    end = time.time()
                    time = str(round((end - start), 2))
                    stats[2] = BIGGER_FONT.render(comparisons, True, GREEN)
                    stats[1] = BIGGER_FONT.render(time, True, GREEN)
                if shuffle_Button.isPressed():
                    random.shuffle(songList)

        songList = draw_window(win, visible, songList, start_index, end_index)
    py.quit()


# begin merge sort
# begin code citation: sorting powerpoint slides 89 - 90
def mergeSort(arr, left, right, win, visible, start, end):
    comparisons = 0
    if left < right:
        # calculate the middle section of the array
        middle = left + (right - left) // 2

        # sort first half and second half
        mergeSort(arr, left, middle, win, visible, start, end)
        mergeSort(arr, middle + 1, right, win, visible, start, end)

        # merge all subarrays
        comparisons = merge(arr, left, middle, right, win, visible, comparisons, start, end)
        return comparisons




def merge(arr, left, middle, right, win, visible, comparisons, start, end):
    # create new subarrays
    n1 = middle - left + 1
    n2 = right - middle

    sub1 = [test] * n1
    sub2 = [test] * n2

    # Copy data into subarrays

    for iter_i in range(n1):
        sub1[iter_i] = arr[left + iter_i]

    for iter_j in range(n2):
        sub2[iter_j] = arr[middle + 1 + iter_j]

    iter_i = 0
    iter_j = 0
    final = left

    # sort and merge subarrays into one array
    while iter_i < n1 and iter_j < n2:
        arr[iter_i].check()
        arr[iter_j].check()
        draw_window(win, visible, arr,start, end)
        arr[iter_i].back()
        arr[iter_j].back()

        if sub1[iter_i].width <= sub2[iter_j].width:
            arr[final] = sub1[iter_i]
            iter_i = iter_i + 1
            comparisons += 1
        else:
            arr[final] = sub2[iter_j]
            iter_j = iter_j + 1
            comparisons += 1
        final = final + 1



    # copy any remaining elements into array
    while iter_i < n1:
        arr[iter_i].check()
        draw_window(win, visible, arr, start, end)
        arr[iter_i].back()
        #temp.append(arr[i])
        arr[final] = sub1[iter_i]
        iter_i = iter_i + 1
        final = final + 1

    while iter_j < n2:
        arr[iter_j].check()
        draw_window(win, visible, arr, start, end)
        arr[iter_j].back()
        #temp.append(arr[j])
        arr[final] = sub2[iter_j]
        iter_j = iter_j + 1
        final = final + 1
    return comparisons
#begin code citation: sorting powerpoint slide 38
def insertionSort(bArray, visible, win, comparisons,start, end):
    for i in range(len(bArray)):
        bArray[i].check()
        draw_window(win, visible, bArray, start, end)
        bArray[i].back()
        key = bArray[i].width
        j = i - 1

        while key < bArray[j].width and j >= 0:
            bArray[i].check()
            draw_window(win, visible, bArray, start, end)
            bArray[i].back()
            bArray[i], bArray[j] = bArray[j], bArray[i]
            j = j - 1

    return bArray
#end code citation: sorting powerpoint slide 38

def bucketSort(array, visible, win, start, end):
    buckets = []
    comparisons = 0
    for i in range(len(array) * 3):
        buckets.append([])

    for j in array:
        if array[0].width <= 1:
            comparisons += 1
            bucketIndex = int(10 * j.width)
            buckets[bucketIndex].append(j)
        elif array[0].width >= 100000:
            comparisons += 1
            bucketIndex = int(0.00001 * j.width)
            buckets[bucketIndex].append(j)
        elif array[0].width >= 100:
            comparisons += 1
            bucketIndex = int(0.01 * j.width)
            buckets[bucketIndex].append(j)
        elif array[0].width >= 10:
            comparisons += 1
            bucketIndex = int(0.1 * j.width)
            buckets[bucketIndex].append(j)
        elif array[0].width < 10:
            comparisons += 1
            bucketIndex = int(1 * j.width)
            buckets[bucketIndex].append(j)

    # for k in range(100):
    for k in range(len(array) * 3):
        buckets[k] = insertionSort(buckets[k], visible, win, comparisons, start, end)
    for k in range(len(buckets)):
        print(buckets[k])

    finalIndex = 0
    for i in range(len(array) * 3):
        for j in range(len(buckets[i])):
            array[finalIndex] = buckets[i][j]
            finalIndex = finalIndex + 1
    return comparisons

def finalBucket(arr, visible, win, start, end):
    negative = []
    positive = []
    for i in range(len(arr)):
        if arr[i].width < 0:
            negative.append(arr[i])
        else:
            positive.append(arr[i])

    print(bucketSort(negative, visible, win, start, end))
    print('\n')
    print(bucketSort(positive, visible, win, start, end))
    # bucketSort(negative)
    # bucketSort(positive)

    for i in range(len(negative)):
        negative[i] = -1 * negative[i]
    negative.reverse()
    arr = p.concatenate((negative, positive))

    return arr
# end code citation: sorting powerpoint slides 89 - 90


if __name__ == "__main__":
    main()