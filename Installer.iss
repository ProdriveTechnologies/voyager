// ###########################
#define Release "1.15.0"
// ###########################

#define AppName "voyager"
#define Publisher "Prodrive Technologies"

[Setup]
AppPublisher={#Publisher}
AppName=voyager
AppId=voyager_{#Release}
AppVersion={#Release}
WizardStyle=modern
DefaultDirName={localappdata}\ProdriveTechnologies\voyager\
DefaultGroupName={#Publisher}\voyager
UninstallDisplayIcon=.\icon_black.ico
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
Source: "dist/voyager/*"; DestDir: {app}; Flags: ignoreversion recursesubdirs


[Code]
const
	ModPathName = 'modifypath';
	ModPathType = 'user';

function ModPathDir(): TArrayOfString;
begin
	setArrayLength(Result, 1)
	Result[0] := ExpandConstant('{app}');
end;
#include "modpath.iss"
