
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
        for name, dep in self.build_info.packages:
            fields = {
                'root_dir': dep.rootpath,
                'name': dep.safe_name
            }
            section = self.item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _format_properties(self):
        fields = {
            'condition': '',
            'bin_dirs': "".join("%s;" % p for p in self.build_info.bin_paths),
            'res_dirs': "",
            'include_dirs': "".join("%s;" % p for p in self.build_info.include_paths),
            'lib_dirs': "".join("%s;" % p for p in self.build_info.lib_paths),
            'libs': "".join('%s;' % lib for lib in self.build_info.libs),
            'definitions': "".join("%s;" % d for d in self.build_info.defines),
            'compiler_flags': "",
            'linker_flags': "",
            'exe_flags': ""
        }
        formatted_template = self.properties_template.format(**fields)
        return formatted_template

    @property
    def content(self):
        per_item_props = self._format_items()
        properties = [self._format_properties()]

        fields = {
            'item_properties': per_item_props,
            'properties': '\n'.join(properties)
        }
        formatted_template = self.template.format(**fields)
        return formatted_template