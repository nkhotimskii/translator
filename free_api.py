import speech_recognition as sr
from queue import Queue
from threading import Thread
import pyaudio
from googletrans import Translator

from simultaneous_translation import SimultaneousTranslation

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

class FreeApi(SimultaneousTranslation):
    def __init__(self):

        super().__init__()

        self.messages = Queue()
        self.recordings = Queue()
        self.original_texts = Queue()
        self.translations = Queue()

        self.original_text = ''
        self.translation = ''

        self.channels = 1
        self.frame_rate = 16000
        self.record_seconds = 5
        self.audio_format = pyaudio.paInt16
        self.sample_size = 2

        self.audio_bytes = []

        self.language_codes_path = 'language_codes.json'

        self.language_codes = self.set_language_codes(self.language_codes_path)

    def record_microphone(self, device_index, chunk=1024):
        self.p = pyaudio.PyAudio()
        logger.debug('opening stream')
        stream = self.p.open(format=self.audio_format,
                        channels=self.channels,
                        rate=self.frame_rate,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=chunk)

        frames = []
        while not self.messages.empty():
            data = stream.read(chunk)
            frames.append(data)
            if len(frames) >= (self.frame_rate * self.record_seconds) / chunk:
                self.recordings.put(frames.copy())
                frames = []

        logger.debug('stopping stream')
        stream.stop_stream()
        logger.debug('closing stream')
        stream.close()
        logger.debug('terminating audio interface')
        self.p.terminate()

    def start(self, source_language, target_language):
        source_language_code, translation_language_code, voicing_language_code = self.get_language_codes(source_language, target_language)
        self.messages.put(True)
        record = Thread(target=self.record_microphone, args=(self.device_index,))
        record.start()
        transcribe = Thread(target=self.speech_recognition, args=(source_language_code,))
        transcribe.start()
        translate = Thread(target=self.get_translation, args=(translation_language_code,))
        translate.start()
        voice = Thread(target=self.voicing, args=(voicing_language_code,))
        voice.start()
        logger.info('translation process is started (free api)')

    def stop(self):
        self.messages.get()
        logger.info('translation process is stopped (free api)')

    def speech_recognition(self, language_to_recognize):
        r = sr.Recognizer()
        while not self.messages.empty():
            if not self.recordings.empty():
                frames = self.recordings.get()
                self.audio_bytes.append(frames)
                audio = sr.AudioData(b''.join(frames), 16000, 2)
                try:
                    text = r.recognize_google(audio, language = language_to_recognize)
                    self.original_texts.put(text)
                    if self.original_text != '':
                        self.original_text += f' {text}'
                    else:
                        self.original_text = text
                except (RuntimeError, sr.UnknownValueError):
                    logging.warning('runtimererror/unknownvalueerror exception occured')
                    pass
    
    def get_original_audio(self, path):
        audio_bytes = self.audio_bytes
        return self.save_original_audio(audio_bytes, path)

    def get_translation_audio(self, path):
        return self.save_translation_audio(path)

    def get_translation(self, language_to_translate_to):
        translator = Translator()
        while not self.messages.empty():
            if not self.original_texts.empty():
                text = self.original_texts.get()
                translation = translator.translate(text, dest=language_to_translate_to).text
                self.translations.put(translation)
                if self.translation != '':
                    self.translation += f' {translation}'
                else:
                    self.translation += translation

    def voicing(self, language_to_voice):
        while not self.messages.empty():
            if not self.translations.empty():
                translation = self.translations.get()
                self.voice_translation(translation, language_to_voice)