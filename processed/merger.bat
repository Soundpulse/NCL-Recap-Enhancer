for %%A IN (*.mp4) do ( "E:\MKVToolNix\mkvmerge.exe" -o "remux-%%~nxA" "%%~A" --forced-track "1" --default-track "1" --track-name "0:not valid subtitles" --language "0:eng" "%%~nA.srt")

@echo off
echo ----------------------------------------------------------------------
echo Finished operation!
echo Press any key to exit
pause