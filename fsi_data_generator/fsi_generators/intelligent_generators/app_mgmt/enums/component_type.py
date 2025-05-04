from ....helpers import BaseEnum
from enum import auto


class ComponentType(BaseEnum):
    """
    Enum representing the types of software components that can be used in applications.
    """
    JAVA_LIBRARY = auto()  # A reusable Java code library or JAR file
    NPM_PACKAGE = auto()  # A JavaScript package managed through NPM
    NUGET_PACKAGE = auto()  # A software package for .NET managed through NuGet
    PYTHON_MODULE = auto()  # A Python library or module, typically installed via pip
    RUBY_GEM = auto()  # A package of Ruby code distributed through RubyGems
    FRAMEWORK = auto()  # A comprehensive set of libraries and tools for application development
    API = auto()  # An Application Programming Interface
    DOTNET_ASSEMBLY = auto()  # A compiled code library for the .NET framework
    DOCKER_IMAGE = auto()  # A lightweight, standalone software package
    GRADLE_PLUGIN = auto()  # A plugin for the Gradle build automation system
    MAVEN_PLUGIN = auto()  # A plugin for the Maven build automation tool
    OPERATING_SYSTEM = auto()
    HARDWARE_DEVICE = auto()

    _DEFAULT_WEIGHTS = [
        18.0,  # JAVA_LIBRARY
        14.0,  # NPM_PACKAGE
        10.0,  # NUGET_PACKAGE
        12.0,  # PYTHON_MODULE
        5.0,  # RUBY_GEM
        10.0,  # FRAMEWORK
        12.0,  # API
        8.0,  # DOTNET_ASSEMBLY
        11.0,  # DOCKER_IMAGE
        5.0,  # GRADLE_PLUGIN
        6.0,  # MAVEN_PLUGIN
        15.0,  # OPERATING_SYSTEM
        10.0  # HARDWARE_DEVICE
    ]
