@echo off
setlocal enabledelayedexpansion

set app=%1
set svcl="\svcl-x64\svcl.exe"
set svcl_path=%app%%svcl%
set "svcl_path_without_quotes="!svcl_path:"=!""

%svcl_path_without_quotes% /Disable "CABLE Input"
%svcl_path_without_quotes% /Disable "CABLE Output"
%svcl_path_without_quotes% /Disable "VoiceMeeter Input"
%svcl_path_without_quotes% /Disable "VoiceMeeter Output"

REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:Voicemeeter {17359A74-1236-5467}" /f
REG ADD "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:Voicemeeter {17359A74-1236-5467}" /v "QuietDisplayName" /t REG_SZ /d "Voicemeeter, The Virtual Mixing Console" /f
REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:VBCABLE {87459874-1236-4469}" /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VB:VBCABLE {87459874-1236-4469}" /v "QuietDisplayName" /t REG_SZ /d "VBCABLE, The Virtual Audio Cable" /f
REG ADD "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:Voicemeeter {17359A74-1236-5467}" /v SystemComponent /t REG_DWORD /d 1 /

rmdir /s /q "%AppData%\Microsoft\Windows\Start Menu\Programs\VB Audio\Voicemeeter"
rmdir /s /q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\VB Audio"

set vb="\VB"
set vb_pf="\VB\VB_pf"
set vb_pf_x86="\VB\VB_pf_(x86)"
set vb_path=%app%%vb%
set vb_pf_path=%app%%vb_pf%
set vb_pf_x86_path=%app%%vb_pf_x86%
set "vb_path_without_quotes="!vb_path:"=!""
set "vb_pf_path_without_quotes="!vb_pf_path:"=!""
set "vb_pf_x86_path_without_quotes="!vb_pf_x86_path:"=!""

mkdir %vb_path_without_quotes%
mkdir %vb_pf_path_without_quotes%
mkdir %vb_pf_x86_path_without_quotes%

move "C:\Program Files (x86)\VB" %vb_pf_x86_path_without_quotes%
move "C:\Program Files\VB" %vb_pf_path_without_quotes%
