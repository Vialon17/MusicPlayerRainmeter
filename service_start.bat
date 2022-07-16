if "%1"=="hide" goto CmdBegin
start mshta vbscript:createobject("wscript.shell").run("""%~0"" hide",0)(window.close)&&exit
:CmdBegin

cd C:\Users\Vialon17\Documents\Python\NetCloudMusicPlayer\NeteaseCloudMusicApi
node app.js
