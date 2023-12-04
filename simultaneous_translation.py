from utils import CountLogger
import pygame
import math
import gtts
import json
import pyaudio
import wave
from pipe import chain
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os
import configs

# Moviepy fix
import sys
output = open("output.txt", "wt", encoding="utf-8")
sys.stdout = output
sys.stderr = output

from threading import Thread

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logs = logging.FileHandler(filename='logs.log')
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
logs.setFormatter(format)
logger.addHandler(handler)
logger.addHandler(logs)
logger.setLevel(logging.DEBUG)
logs.setLevel(logging.DEBUG)

class SimultaneousTranslation():
    def __init__(self, google_api=False):
        
        self.p = pyaudio.PyAudio()

        # Recording device
        self.device = 'VoiceMeeter Output (VB-Audio Vo'
        self.device_index = self.choose_device_index(self.device)

        # Controlling volume
        self.sound = None
        self.volume = 20
        
        # Voicing translation
        pygame.init()
        pygame.mixer.init()
        self.count = CountLogger()

        self.google_api = google_api

        self.channels = 2
        self.frame_rate = 44100
        self.sample_width = 2

        self.original_text = ''
        self.translation = ''

        self.started = False

        self.credentials = None

        self.configs = configs.Configs()

    def change_routing(self, application):
        self.configs.change_routing(application)

    def control_volume(self, volume: int):
        self.volume = volume
        self.configs.control_volume(volume*5)

    def restore_volume(self):
        self.configs.control_volume(100)

    def get_applications(self):
        return self.configs.show_applications()

    def disable_devices(self):
        self.configs.disable_devices()

    def voice_translation(self, translation, language_to_voice):
        obj = gtts.gTTS(text=translation, lang=language_to_voice, slow=False)
        self.count.log()
        try:
            obj.save(f'speech\\speech_{self.count._count}.mp3')
        except gtts.tts.gTTSError as e:
            logger.error(e)
        self.sound = pygame.mixer.Sound(f'speech\\speech_{self.count._count}.mp3')
        self.sound.set_volume(self.volume)
        #self.translation_pause = math.ceil(self.sound.get_length())
        self.translation_pause = self.sound.get_length()
        self.sound.play()
        logger.info('voicing translation')

    def set_language_codes(self, filename):
        with open(filename) as json_data_file:
            language_codes = json.load(json_data_file)
        return language_codes
    
    def get_language_codes(self, source_language, target_language):
        source_language_code = self.language_codes.get('languages_to_recognize').get(source_language)
        translation_language_code = self.language_codes.get('languages_to_translate_to').get(target_language)
        voicing_language_code = self.language_codes.get('languages_to_voice').get(target_language)
        return source_language_code, translation_language_code, voicing_language_code

    def choose_device_index(self, device_name):
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            if device['name'] == device_name:
                return i

    def save_translation_audio(self, path):
        audio_clip_paths = [f'speech\\speech_{i}.mp3' for i in range(1, self.count._count+1)]
        save_audio = Thread(target=self.concatenate_audio, args=(audio_clip_paths, path,))
        save_audio.start()

    def concatenate_audio(self, audio_clip_paths, output_path):
        logger.info('saving translation audio...')
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        logger.debug('clips are generated')
        final_clip = concatenate_audioclips(clips)
        logger.debug('clips are concatenated')
        final_clip.write_audiofile(output_path)
        if os.path.exists(output_path):
            logger.info(f'translation audio saved to {output_path}')
        else:
            logger.error('failed to save audio file')
        # for file_name in audio_clip_paths:
        #     os.remove(file_name)
        #     self.count._count = 0
        return

    def save_original_audio(self, audio_bytes, path):
        wf = wave.open(path, 'wb')
        wf.setnchannels(self.channels)
        wf.setframerate(self.frame_rate)
        wf.setsampwidth(self.sample_width)
        wf.writeframes(b''.join(list(audio_bytes | chain)))
        wf.close()
        