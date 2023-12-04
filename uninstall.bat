@echo off
setlocal enabledelayedexpansion

set app=%1
set vb="\VB"
set vb_pf="\VB\VB_pf\VB"
set vb_pf_x86="\VB\VB_pf_(x86)\VB"
set vb_path=%app%%vb%
set vb_pf_path=%app%%vb_pf%
set vb_pf_x86_path=%app%%vb_pf_x86%
set "vb_path_without_quotes="!vb_path:"=!""
set "vb_pf_path_without_quotes="!vb_pf_path:"=!""
set "vb_pf_x86_path_without_quotes="!vb_pf_x86_path:"=!""
move %vb_pf_x86_path_without_quotes% "C:\Program Files (x86)"
move %vb_pf_path_without_quotes% "C:\Program Files"
REG ADD "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:Voicemeeter {17359A74-1236-5467}" /v SystemComponent /t REG_DWORD /d 0 /f

REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:VBCABLE {87459874-1236-4469}" /f
REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\VB:Voicemeeter {17359A74-1236-5467}" /f

rmdir /s /q "C:\Program Files (x86)\VB"
rmdir /s /q "C:\Program Files\VB"
