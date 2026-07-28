import setuptools
import versioneer

import os
import re
import sys
import platform
import subprocess
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

# Intended to make building in manylinux images easier.
# CentOS (or the EPEL package?) calls CMake cmake3...
cmake3_path = Path("/usr/bin/cmake3")
cmake_name = "cmake3" if cmake3_path.exists() else "cmake"

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[str(p) for p in Path(sourcedir).glob('**/*')])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        debug = os.getenv("DEBUG", "").lower() in {"1", "true", "yes", "on"}

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPython_EXECUTABLE=' + sys.executable,
                      '-DPYBIND11_FINDPYTHON=ON']

        cfg = 'Debug' if debug else 'Release'
        build_args = [f'-j{os.cpu_count()}']

        generator = os.getenv('CMAKE_GENERATOR', '')
        if not generator and platform.system() == "Windows":
            import shutil
            # Ninja needs MSVC to be available in the current environment.
            if shutil.which("ninja") is not None and shutil.which("cl") is not None:
                os.environ["CMAKE_GENERATOR"] = "Ninja"
                generator = "Ninja"

        generator_name = generator.lower()
        uses_ninja = generator_name.startswith("ninja")
        single_config_generators = {"ninja", "nmake makefiles", "mingw makefiles"}
        is_multi_config = (
            platform.system() == "Windows"
            and generator_name not in single_config_generators
        )

        if platform.system() == "Windows":
            if is_multi_config:
                cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
                if (
                    not generator_name or generator_name.startswith("visual studio")
                ) and sys.maxsize > 2**32:
                    cmake_args += ['-A', 'x64']
                build_args += ['--config', cfg]
                if not uses_ninja:
                    build_args += ['--', '/m']
            else:
                cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call([cmake_name, ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call([cmake_name, '--build', '.'] + build_args, cwd=self.build_temp)


with open("README.md", "r") as fh:
    long_description = fh.read()

cmdclass = versioneer.get_cmdclass()
cmdclass["build_ext"] = CMakeBuild

setuptools.setup(
    name="oead",
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    author="leoetlino",
    author_email="leo@leolam.fr",
    description="Library for recent Nintendo EAD formats in first-party games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeldamods/oead",
    packages=setuptools.find_packages(),
    license="GPL-2.0-or-later",
    classifiers=[
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.9",
    ext_modules=[CMakeExtension(name="oead", sourcedir="py")],
    data_files=[('data', [str(p) for p in Path('data').glob('**/*')])],
    zip_safe=False,
)
