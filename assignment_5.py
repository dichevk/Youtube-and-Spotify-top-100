import json
import matplotlib.pyplot as plt

def main():
    views = []


    with open("videos.txt") as yt_dataset:
        videos = json.load(yt_dataset)

    # Get view count of each video
    for v in videos:
        views.append(int(videos[v]["statistics"]["viewCount"]))

    # Sort by view count in descending order
    views.sort(reverse=True)

    # Plot the graph
    x_axis = [x for x in range(1, len(views)+1)]
    y_axis = [y for y in views]
    print(y_axis[int(len(y_axis) / 2 - 1)])
    plt.plot(x_axis, y_axis)
    plt.xlabel("Number of videos")
    plt.ylabel("View count volume")
    plt.show()


if __name__ == '__main__':
    main()
