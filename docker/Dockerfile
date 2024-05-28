FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    wget \
    zip unzip \
    python3.12 python3.12-venv python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

# set python venv
RUN python -m venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"

# install python libs
WORKDIR /workspace
RUN pip install ffmpeg ffmpeg-python && \
    hash=$(git ls-remote https://github.com/ytdl-org/youtube-dl.git | head -n 1 | cut -c 1-40) && \
    wget https://github.com/ytdl-org/youtube-dl/archive/$hash.zip && \
    unzip -n $hash.zip && cd youtube-dl-$hash && \
    python -m pip install . && \
    cd .. && rm -r youtube-dl-$hash $hash.zip
