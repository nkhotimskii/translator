from __future__ import division

from google.cloud import speech, translate_v2 as translate
from google.api_core.exceptions import OutOfRange

import pyaudio
from six.moves import queue

from threading import Thread

import logging

import os

import time

from simultaneous_translation import SimultaneousTranslation

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

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk, device_index):
        self._rate = rate
        self._chunk = chunk
        self.device_index = device_index

        self._buff = queue.Queue()
        self.closed = True

        self.audio_bytes = []

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            input_device_index=self.device_index,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
                chunk = self._buff.get()
                if chunk is None:
                    return
                data = [chunk]

                while True:
                    try:
                        chunk = self._buff.get(block=False)
                        if chunk is None:
                            return
                        data.append(chunk)
                    except queue.Empty:
                        break
                    
                self.audio_bytes.append(data)
                yield b"".join(data)

class GoogleApi(SimultaneousTranslation):
    def __init__(self, credentials):

        super().__init__()

        # Recording settings
        self.rate = 16000
        self.chunk = int(self.rate / 10)

        self.credentials = credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials

        self.client = translate.Client()

        self.started = False

        self.translation_queue = queue.Queue()

        self.original_text = ''

        self.translation = ''

        self.audio_bytes = []

        self.language_codes_path = 'language_codes.json'

        self.language_codes = self.set_language_codes(self.language_codes_path)

        self.stream = None

    def listen_print_loop(self, stream, responses, translation_language_code):
        for response in responses:
            self.audio_bytes = stream.audio_bytes
            if self.started:
                if not response.results:
                    continue
                
                result = response.results[0]
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                if result.is_final:
                    if self.original_text != '':
                        self.original_text += ' ' + transcript
                        translation = self.translate(translation_language_code, transcript)
                        self.translation += ' ' + translation
                        self.translation_queue.put(translation)
                    else:
                        self.original_text = transcript
                        translation = self.translate(translation_language_code, transcript)
                        self.translation = translation
                        self.translation_queue.put(translation)
                    print(translation)

    def translate(self, target, text):
        result = self.client.translate(text, target_language=target)
        return result['translatedText']

    def voicing(self, language_to_voice):
        while self.started:
            if not self.translation_queue.empty():
                translation = self.translation_queue.get()
                self.voice_translation(translation, language_to_voice)
                time.sleep(self.translation_pause)

    def terminate_translation(self):
        logger.debug('stopping stream')
        self.stream._audio_stream.stop_stream()
        logger.debug('closing stream')
        self.stream._audio_stream.close()
        self.stream.closed = True
        self.stream._buff.put(None)
        self.stream._buff.queue.clear()
        if self.stream._buff.empty():
            logger.debug('buff is emptied')
        # logger.debug('terminating audio interface')
        # self.stream._audio_interface.terminate()
        self.translation_queue.queue.clear()

    def main(self, source_language_code, translation_language_code, voicing_language_code):
        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code=source_language_code,
            enable_automatic_punctuation=True,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True, single_utterance=False
        )

        self.started = True
        voice = Thread(target=self.voicing, args=(voicing_language_code,))
        voice.start()
        while self.started:
            with MicrophoneStream(self.rate, self.chunk, self.device_index) as self.stream:
                logger.debug('stream opened')
                audio_generator = self.stream.generator()
                requests = (
                    speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator
                )
                try:
                    responses = client.streaming_recognize(streaming_config, requests)
                except Exception as e:
                    logger.error(e)
                    print('streaming recognize')
                try:
                    self.listen_print_loop(self.stream, responses, translation_language_code)
                except OutOfRange as e:
                    logger.error(e)
                    print('listen print loop')
                
            logger.debug('stopping stream')
            self.stream._audio_stream.stop_stream()
            logger.debug('closing stream')
            self.stream._audio_stream.close()
    
    def start(self, source_language, target_language):
        source_language_code, translation_language_code, voicing_language_code = self.get_language_codes(source_language, target_language)
        process = Thread(target=self.main, args=(source_language_code, translation_language_code, voicing_language_code,))
        process.start()
        logger.info('translation process is started (google api)')

    def stop(self):
        self.started = False
        logger.info('translation process is stopped (google api)')
        self.terminate_translation()

    def get_original_text(self):
        return self.original_text

    def get_translation(self):
        return self.translation

    def get_original_audio(self, path):
        audio_bytes = self.audio_bytes
        return self.save_original_audio(audio_bytes, path)

    def get_translation_audio(self, path):
        return self.save_translation_audio(path)