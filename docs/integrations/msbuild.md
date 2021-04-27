# MSBuild
MSBuild integration is done through a Visual Studio project properties file (voyager.props).
This file contains all the include paths, lib paths, flags, etc. for the project.
Each voyager project creates it's own .props file that has to be included in Visual Studio.

## Add props file to build
In case the project is not yet configured for voyager the user must add the props file to the project.

Go to your Visual Studio project, and open the **Property Manager** (usually in **View -> Other Windows -> Property Manager**).
Highlight the project to which the props file has to be added. Click the + icon and select the generated `voyager.props` file.

### Project not loading
When a user forgets to run `voyager install`, Visual Studio won't load the project because the .props file is missing.
This can be fixed by adding a condition to the Import in the .vcxproj file: `<Import Project="voyager.props" Condition="exists('voyager.props')" />`