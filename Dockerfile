FROM python

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --upgrade pip
RUN pip install vosk srt

WORKDIR /run

# RUN git clone https://github.com/alphacep/vosk-api.git

WORKDIR /run/vosk-api/python/example

# RUN curl -O https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
# RUN unzip vosk-model-en-us-0.22.zip
# RUN mv vosk-model-en-us-0.22 model

COPY *.py ./
COPY *.wav ./
# COPY . .

# ENV PYTHONUNBUFFERED=0

CMD python srt.py short.wav
# CMD python main.py audio_16k.wav
# CMD python test_srt.py short.wav
# CMD python srt.py short.wav
