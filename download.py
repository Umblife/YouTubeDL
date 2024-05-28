import os
import shutil
import youtube_dl


class Downloader:
    def __init__(self, fileformat='mp3', output_dir='./saved'):
        self._fileformat = fileformat
        self._outdir = output_dir

    def __call__(self, url, fileformat=None, output_dir=None):
        if fileformat is None:
            _format = self._fileformat
        if output_dir is None:
            _outdir = self._outdir

        self._downloadfile(url, _format, _outdir)

    def _downloadfile(self, url, fileformat, output_dir):
        if fileformat == 'mp3':
            _outdir = os.path.join(output_dir, 'mp3/')
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }], }

        else:
            _outdir = os.path.join(output_dir, 'mp4/')
            options = {
                'nocheckcertificate:': True,
                'outtmpl': os.path.join(_outdir, '%(title)s.mp4'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best'}

        os.makedirs(_outdir, exist_ok=True)
        with youtube_dl.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

            # when use 'outtmpl' option, the file is not correct format as mp3
            #   -> options = {'outtmpl': 'dirname/filename.mp3')}
            # for this reason, after download to current directory,
            # and move the file to the specified directory.
            if fileformat == 'mp3':
                info_with_audio_extension = dict(info)
                info_with_audio_extension['ext'] = 'mp3'
                filename = ydl.prepare_filename(info_with_audio_extension)
                shutil.move(f'./{filename}', _outdir)


if __name__ == "__main__":
    # sample
    download_youtube = Downloader(fileformat='mp3', output_dir='./saved')
    download_youtube('https://www.youtube.com/watch?v=0C3vCXMOtmE')
