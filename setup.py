import os
import subprocess
import sys
import os
import subprocess
import sys
from setuptools import setup, find_packages, Command
from setuptools.command.develop import develop
from setuptools.command.install import install

def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def install_ffmpeg():
    subprocess.check_call(['ffmpeg_download.bat'], shell=True)

def verify_installation():
    # Check if FFmpeg executables exist
    ffmpeg_files = ['ffmpeg.exe', 'ffprobe.exe', 'ffplay.exe']
    for file in ffmpeg_files:
        if not os.path.exists(os.path.join('dist', file)):
            raise RuntimeError(f"FFmpeg installation incomplete: {file} not found")

class InstallCommand(install):
    def run(self):
        install_ffmpeg()
        install.run(self)

class DevelopCommand(develop):
    def run(self):
        install_ffmpeg()
        develop.run(self)
        verify_installation()

class ReleaseCommand(Command):
    description = 'Build and upload the package to PyPI'
    user_options = [
        ('repository=', 'r', 'repository to upload to'),
        ('username=', 'u', 'username for repository'),
        ('password=', 'p', 'password for repository'),
    ]

    def initialize_options(self):
        self.repository = None
        self.username = None
        self.password = None

    def finalize_options(self):
        pass

    def run(self):
        # Clean previous builds
        for dir_to_clean in ['build', 'dist', '*.egg-info']:
            subprocess.run(['rm', '-rf', dir_to_clean], shell=True)

        # Install FFmpeg
        install_ffmpeg()

        # Build distributions
        subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])

        # Upload to PyPI using twine
        twine_cmd = ['twine', 'upload']
        if self.repository:
            twine_cmd.extend(['--repository-url', self.repository])
        if self.username:
            twine_cmd.extend(['--username', self.username])
        if self.password:
            twine_cmd.extend(['--password', self.password])
        twine_cmd.append('dist/*')
        
        subprocess.check_call(twine_cmd)

def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read requirements
install_requires = read_requirements('src/requirements.txt')
dev_requires = read_requirements('requirements-dev.txt')

setup(
    name='media-encoder',
    version='0.1.0',
    description='A media encoding tool for streaming',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='r4d4m4n71s',
    url='https://github.com/yourusername/media-encoder',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        "": ["dist/*.exe"],  # Include FFmpeg executables
        "config": ["*.json"],  # Include config files
    },
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'media-encoder=media_encoder.gui.encoder_cli:main',
        ],
    },
    cmdclass={
        'install': InstallCommand,
        'develop': DevelopCommand,
        'release': ReleaseCommand,
    },
)