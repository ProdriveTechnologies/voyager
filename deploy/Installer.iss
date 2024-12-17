// ###########################
#define Release "1.17.3"
// ###########################

#define AppName "voyager"
#define Publisher "Prodrive Technologies"

[Setup]
AppPublisher={#Publisher}
AppName=voyager
AppId=voyager
AppVersion={#Release}
WizardStyle=modern
DefaultDirName={commonpf64}\Prodrive\voyager\
DefaultGroupName={#Publisher}\voyager
UninstallDisplayIcon={app}\voyager.exe
UninstallDisplayName=voyager {#Release}
Compression=lzma2
SolidCompression=yes
OutputDir=.\setup
OutputBaseFilename=voyagerSetup
SetupIconFile=.\icon_black.ico
ChangesEnvironment=true

[Tasks]
Name: modifypath; Description: &Add application directory to your system path

[Files]
Source: "../dist/voyager/*"; DestDir: {app}; Flags: ignoreversion recursesubdirs


[Code]
const
	ModPathName = 'modifypath';
	ModPathType = 'system';

function ModPathDir(): TArrayOfString;
begin
	setArrayLength(Result, 1)
	Result[0] := ExpandConstant('{app}');
end;
#include "modpath.iss"
