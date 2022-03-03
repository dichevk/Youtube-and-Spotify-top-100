import json
import random
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#DEVELOPER_KEY = 'AIzaSyAHtQmvsjj06Rs1n5M2FswLKMo8DmSrndk'
#DEVELOPER_KEY = 'AIzaSyAYY74ahBroJPGXJkr9Pg3p-iIdLAQaLas'
DEVELOPER_KEY = 'AIzaSyD359cWKnx1t_LFk0fUHWR5xUxp-uXdxhM'
#DEVELOPER_KEY = 'AIzaSyCJnEaDCRHSCxw8Iy5OADHBd2jvWrkf_cE'
#DEVELOPER_KEY = 'AIzaSyD311orSklGKZPAatHP3qIvL3SX2KTvRj4'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def setup():
    with open('videos.txt') as json_file:
        videos = json.load(json_file)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    return youtube, videos


def youtube_video(youtube, videos):
    videoId = videos[list(videos.keys())[-1]]['id']     # Get the ID of the last song on the list.
    search_response = youtube.search().list(part='id,snippet',
                                            relatedToVideoId=videoId,
                                            maxResults=3,
                                            type='video').execute()     # Get a list of recommended videos for that song.

    response_dict = dict()
    result_nr = 0
    for search_result in search_response.get('items', []):  # Going through every result of the query.
        response_dict[result_nr] = search_result    # Adding each of them to a list
        result_nr += 1

    random.seed(time.time())
    upper_bound = len(response_dict) - 1    # Determining the upper bound of the random number generator
    rnd = random.randint(0, upper_bound)
    try:
        rnd_song = response_dict[rnd]   # Selecting random song
        rnd_song_title = rnd_song['snippet']['title']
        if rnd_song_title not in videos:
            videos_response = youtube.videos().list(part='id,snippet,statistics',
                                                    id=rnd_song['id']['videoId']).execute()     # Retrieving the selected video and its data
            for video_result in videos_response.get('items', []):
                if video_result['snippet']['categoryId'] == '10':   # Checking if the video is categorized as music
                    videos[rnd_song_title] = video_result
                    print("+1")

        youtube_video(youtube, videos)  # Rinse and repeat
    except KeyError:    # For some of the recommended videos the 'snippet' element is missing.
        youtube_video(youtube, videos)
        exit()
    except HttpError as e:
        print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
        with open('videos.txt', 'w') as json_file:
            json.dump(videos, json_file)
        exit()



if __name__ == '__main__':
    #videoId = 'uxpDa-c-4Mc'
    #categoryId = '10'
    yt, vid = setup()
    try:
        print(youtube_video(yt, vid))
    except HttpError as e:
        print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))