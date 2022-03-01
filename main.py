#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import subprocess
import json
import datetime

SetLogLevel(-1)

if not os.path.exists("model"):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

sample_rate = 16000
model = Model("model")
rec = KaldiRecognizer(model, sample_rate)
rec.SetWords(True)

process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                            sys.argv[1],
                            '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'],
                           stdout=subprocess.PIPE)


WORDS_PER_LINE = 1000


def transcribe():
    i = 0
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            show_time = i > 0 and i % 30 == 0
            print_something(rec.Result(), show_time)
            i += 1
    print_something(rec.FinalResult(), False)


def print_something(res, show_time):
    jres = json.loads(res)
    if not 'result' in jres:
        return
    words = jres['result']
    start = datetime.timedelta(seconds=words[0]['start'])
    end = datetime.timedelta(seconds=words[-1]['end'])
    content = " ".join([l['word'] for l in words])
    if show_time:
        print(f"\n{start} - {end}")
    print(f"{content}", end=" ")
    # print (res['text'])


transcribe()
