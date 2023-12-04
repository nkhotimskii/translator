import subprocess
from subprocess import Popen, PIPE
import pandas as pd
import io

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

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

class Configs():
    def __init__(self):

        self.headphones = 'Headphones'
        self.speakers = 'Speakers'
        self.microphone = 'Internal Microphone'
        self.virtual_cable_input = 'CABLE Input'
        self.virtual_cable_output = 'CABLE Output'
        self.voice_meeter_input = 'VoiceMeeter Input'
        self.voice_meeter_output = 'VoiceMeeter Output'
        
        self.apps = None

        self.process = ''

        self.enable_devices()

        self.configs_df = self.get_configs()

        self.setup()

    def get_configs(self):
        open_configs = Popen(['svcl-x64\\svcl.exe', '/scomma'], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        configs = open_configs.communicate()[0]
        return pd.read_csv(io.BytesIO(configs))

    def enable_devices(self):
        for device in [self.voice_meeter_input, self.voice_meeter_output, self.virtual_cable_input, self.virtual_cable_output]:
            Popen(['svcl-x64\\svcl.exe',
                    '/Enable',
                    device,
                    ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

    def disable_devices(self):
        for device in [self.voice_meeter_input, self.voice_meeter_output, self.virtual_cable_input, self.virtual_cable_output]:
            Popen(['svcl-x64\\svcl.exe',
                    '/Disable',
                    device,
                    ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

    def setup(self):
        logger.debug(f'setting up sound settings')
        # Set headphones or speakers as default playback device
        if self.headphones in self.configs_df['Name'].values:
            Popen(['svcl-x64\\svcl.exe',
                    '/SetDefault', 
                    f'{self.configs_df[(self.configs_df.Name == self.headphones) & (self.configs_df.Type == "Device")]["Command-Line Friendly ID"].values[0]}',
                    '0',
                    ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        else:
            Popen(['svcl-x64\\svcl.exe',
                    '/SetDefault',
                    f'{self.configs_df[(~self.configs_df.Name.isin(["CABLE Input", "VoiceMeeter Input"])) & (self.configs_df.Type == "Device") & (self.configs_df.Direction == "Render") & (self.configs_df["Device State"] == "Active")]["Command-Line Friendly ID"].values[0]}',
                    '0',
                    ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        # Set voice meeter input as default communication device
        Popen(['svcl-x64\\svcl.exe',
                '/SetDefault', 
                self.voice_meeter_input,
                '2',
                ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        # Set microphone as default communication device
        Popen(['svcl-x64\\svcl.exe',
                '/SetDefault',
                f'{self.configs_df[(~self.configs_df.Name.isin(["CABLE Output", "VoiceMeeter Output"])) & (self.configs_df.Direction == "Capture") & (self.configs_df["Device State"] == "Active")]["Name"].values[0]}',
                '2',
                ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        # Set virtual cable output to listen to indicated device
        Popen(['svcl-x64\\svcl.exe',
                '/SetListenToThisDevice',
                self.virtual_cable_output,
                '1',
                ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        # Set voice meeter output to listen to indicated device
        Popen(['svcl-x64\\svcl.exe',
                '/SetListenToThisDevice',
                self.voice_meeter_output,
                '1',
                ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo) 
        # Indicate device for voice meeter output to listen to (virtual cable input)
        Popen(['svcl-x64\\svcl.exe',
            '/SetPlaybackThroughDevice',
            self.voice_meeter_output,
            self.virtual_cable_input,
            ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        # Set VB-Audio Virtual Cable as default device
        Popen(['svcl-x64\\svcl.exe',
                '/SetDefault',
                "CABLE Output",
                '1',
                ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

    def change_routing(self, app):
        self.process = self.configs_df[self.configs_df.Name == app]['Process Path'].values[0]
        logger.debug(f'routing a process {self.process} to voice meeter input')
        device = self.configs_df[self.configs_df.Name == self.voice_meeter_input]['Command-Line Friendly ID'].values[0]
        Popen(['svcl-x64\\svcl.exe', '/SetAppDefault', f'{"" + device + ""}', 'all', f'{"" + self.process + ""}'], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

    def show_applications(self):
        self.configs_df = self.get_configs()
        self.apps = self.configs_df[(self.configs_df.Type == 'Application') & (self.configs_df.Direction == 'Render') & (~self.configs_df.Name.isin(['Python', 'System Sounds', 'Microsoft® Windows® Operating System','Программа синхронного перевода','app','app.exe']))].Name.tolist()
        self.apps = [str(i) for i in self.apps]
        return list(set(self.apps))

    def control_volume(self, volume):
        try:
            Popen(['svcl-x64\\svcl.exe',
                        '/SetVolume',
                        self.configs_df[self.configs_df['Process Path'] == self.process].Name.values[0],
                        str(volume),
                        ], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
        except IndexError:
            pass