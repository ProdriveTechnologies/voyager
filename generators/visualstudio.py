
from generators.generator import Generator

class VisualStudioGenerator(Generator):
    template = '''<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ImportGroup Label="PropertySheets" />
  <PropertyGroup Label="UserMacros" />
  <PropertyGroup Label="Voyager-RootDirs">{item_properties}
  </PropertyGroup>
  {properties}
  <ItemGroup />
</Project>'''

    properties_template = '''<PropertyGroup Label="VoyagerVariables"{condition}>
    <VoyagerCompilerFlags>{compiler_flags}</VoyagerCompilerFlags>
    <VoyagerLinkerFlags>{linker_flags}</VoyagerLinkerFlags>
    <VoyagerPreprocessorDefinitions>{definitions}</VoyagerPreprocessorDefinitions>
    <VoyagerIncludeDirectories>{include_dirs}</VoyagerIncludeDirectories>
    <VoyagerResourceDirectories>{res_dirs}</VoyagerResourceDirectories>
    <VoyagerLibraryDirectories>{lib_dirs}</VoyagerLibraryDirectories>
    <VoyagerBinaryDirectories>{bin_dirs}</VoyagerBinaryDirectories>
    <VoyagerLibraries>{libs}</VoyagerLibraries>
  </PropertyGroup>
  <PropertyGroup{condition}>
    <LocalDebuggerEnvironment>PATH=%PATH%;{bin_dirs}</LocalDebuggerEnvironment>
    <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
  </PropertyGroup>
  <ItemDefinitionGroup{condition}>
    <ClCompile>
      <AdditionalIncludeDirectories>$(VoyagerIncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <PreprocessorDefinitions>$(VoyagerPreprocessorDefinitions)%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <AdditionalOptions>$(VoyagerCompilerFlags) %(AdditionalOptions)</AdditionalOptions>
    </ClCompile>
    <Link>
      <AdditionalLibraryDirectories>$(VoyagerLibraryDirectories)%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
      <AdditionalDependencies>$(VoyagerLibraries)%(AdditionalDependencies)</AdditionalDependencies>
      <AdditionalOptions>$(VoyagerLinkerFlags) %(AdditionalOptions)</AdditionalOptions>
    </Link>
    <Midl>
      <AdditionalIncludeDirectories>$(VoyagerIncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
    </Midl>
    <ResourceCompile>
      <AdditionalIncludeDirectories>$(VoyagerIncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <PreprocessorDefinitions>$(VoyagerPreprocessorDefinitions)%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <AdditionalOptions>$(VoyagerCompilerFlags) %(AdditionalOptions)</AdditionalOptions>
    </ResourceCompile>
  </ItemDefinitionGroup>'''

    item_template = '''
    <Voyager-{name}-Root>{root_dir}</Voyager-{name}-Root>'''

    def _format_items(self):
        sections = []
        for name, dep in self.dependencies.dependencies:
            fields = {
                'root_dir': dep.rootpath,
                'name': name
            }
            section = self.item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _format_properties(self, build_info, condition):
        fields = {
            'condition': condition,
            'bin_dirs': "TODO"
        }
        formatted_template = self.properties_template.format(**fields)
        return formatted_template

    @property
    def content(self):
        per_item_props = self._format_items()
        pass