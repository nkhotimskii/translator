import json
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


class Translator():
    def __init__(self, simutlaneous_translation, credentials_path=None):
        self.simultaneous_translation = simutlaneous_translation

        self.credentials_path = credentials_path

    def start(self, source_language, target_language, application):
        self.simultaneous_translation.change_routing(application)
        self.simultaneous_translation.start(source_language, target_language)

    def stop(self):
        self.simultaneous_translation.restore_volume()
        self.simultaneous_translation.stop()

    def get_original_text(self):
        return self.simultaneous_translation.original_text

    def get_translation(self):
        return self.simultaneous_translation.translation

    def get_original_audio(self, path):
        logger.info('getting original audio')
        return self.simultaneous_translation.get_original_audio(path)

    def get_translation_audio(self, path):
        logger.info('getting translation audio')
        return self.simultaneous_translation.get_translation_audio(path)

    def clear(self):
        self.simultaneous_translation.original_text = ''
        self.simultaneous_translation.translation = ''

    def control_volume(self, volume):
        self.simultaneous_translation.control_volume(volume)

    def get_languages(self):
        return self.simultaneous_translation.language_codes

    def get_applications(self):
        return self.simultaneous_translation.get_applications()

    def disable_devices(self):
        self.simultaneous_translation.disable_devices()

    def session_store(self, source_language, target_language, google_checkbox: bool):
        logger.info('saving session')
        volume = self.simultaneous_translation.volume
        credentials_path = self.simultaneous_translation.credentials
        dictionary = {
            'source_language': source_language,
            'target_language': target_language,
            'volume': volume,
            'credentials_path': credentials_path,
            'google_checkbox': google_checkbox
        }
        json_object = json.dumps(dictionary)
        with open('session_store.json', 'w') as file:
            file.write(json_object)

    def restore_session(self):
        logger.info('restoring session')
        with open('session_store.json', 'r') as file:
            json_object = json.load(file)
            source_language = json_object['source_language']
            target_language = json_object['target_language']
            volume = int(json_object['volume'])
            credentials_path = json_object['credentials_path']
            google_checkbox = json_object['google_checkbox']
        return source_language, target_language, volume, credentials_path, google_checkbox