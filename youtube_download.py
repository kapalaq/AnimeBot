from pytube import YouTube


class Download:

    def __init__(self, path, link):
        self.path = path
        try:
            self.youtube = YouTube(link)

        except Exception as error:
            print("Error:", error)

    async def download_video(self):
        video = await self.streams()
        video.download(self.path)
        return self.path + self.youtube.title + '.mp4'

    async def streams(self):
        mass = []
        par = ['240p', '360p', '480p', '720p', '1080p'][::-1]
        i = 0
        func = lambda x: 'mime_type="video/mp4"' in str(x) and par[i] in str(x)
        while not mass:
            mass = list(filter(func, self.youtube.streams))
            i += 1
            if i == 5:
                break
        return mass[0]
