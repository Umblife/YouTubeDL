import ffmpeg
import glob
import os
import youtube_dl


class Downloader:
    def __init__(self, fileformat='mp3', output_dir='./downloaded'):
        self._fileformat = fileformat
        self._outdir = output_dir

    def __call__(self, url, fileformat=None, output_dir=None):
        if fileformat is None:
            _format = self._fileformat
        if output_dir is None:
            _outdir = self._outdir
            os.makedirs(_outdir, exist_ok=True)

        self._downloadfile(url, _format, _outdir)

    def _downloadfile(self, url, fileformat, output_dir):
        options = {
            'nocheckcertificate:': True,
            'outtmpl': os.path.join(output_dir, '%(title)s' + f'.{fileformat}'),
        }

        if fileformat == 'mp3':
            options['format'] = 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio'
            youtube_dl.YoutubeDL(options).download([url])

            filenames = glob.glob(os.path.join(output_dir, '*.m4a'))
            for filename in filenames:
                self._converttomp3(filename)
        else:
            options['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best'
            youtube_dl.YoutubeDL(options).download([url])

    @staticmethod
    def _converttomp3(filename):
        root, ext = os.path.splitext(filename)
        if ext not in ['.m4a']:
            return
        newname = '%s.mp3' % root
        stream = ffmpeg.input(filename)
        stream = ffmpeg.output(stream, newname, format='mp3', audio_bitrate='320k')
        ffmpeg.run(stream)
        os.remove(filename)


if __name__ == "__main__":
    # sample
    download_youtube = Downloader(fileformat='mp3', output_dir='./downloaded')
    download_youtube('https://www.youtube.com/watch?v=0C3vCXMOtmE')
