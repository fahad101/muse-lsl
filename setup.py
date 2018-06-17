from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from shutil import copyfile
import os
import platform
import subprocess
import tempfile
import zipfile
import wget
import logging 

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        if(check_install_bluemuse(True)): install_bluemuse()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        if(check_install_bluemuse()): install_bluemuse()

def install_bluemuse():
    zipfile_name = 'BlueMuse_1.0.7.0.zip'
    url = 'https://github.com/kowalej/BlueMuse/raw/master/Dist/' + zipfile_name
    dist_folder = 'temp_bluemuse_dist'

    tmp_dir = tempfile.mkdtemp(dist_folder) or dist_folder

    print('Downloading BlueMuse to: ' + tmp_dir)
    zipfile_path = os.path.join(tmp_dir, zipfile_name)
    wget.download(url, zipfile_path)

    print('Extracting: ' + zipfile_path)
    zip_ref = zipfile.ZipFile(zipfile_path, 'r')
    zip_ref.extractall(tmp_dir)
    zip_ref.close()

    extract_dir = zipfile_path.replace('.zip','')
    powershell_path = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
    install_script = os.path.join(extract_dir, 'InstallBlueMuse.ps1')
    subprocess.call([powershell_path, '-ExecutionPolicy', 'Unrestricted', install_script])

def check_install_bluemuse(ask_user = False):
    platform_name = platform.system().lower()
    if platform_name == 'windows' and int(platform.version().replace('.', '')) >= 10015063:
        if ask_user: return True
        print('-------------------- ATTENTION ----------------------------\nWe have detected you are on a compatible Windows 10 system.')
        while(True):
            try:
                # Normally we should be able to ask user for confirmation.
                # However this can fail, therefore we will just isntall since the platform is OK.
                install = input('Would you like to auto install BlueMuse now (y/n)?')
                if(install.lower() == 'y'):
                    return True
                elif(install.lower() == 'n'):
                    return False
            except:
                return True
    return False

def copy_docs():
    docs_dir = 'muselsl/docs'
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    copyfile('README.md', docs_dir + '/README.md')
    copyfile('blinks.png', docs_dir + '/blinks.png')

copy_docs()

setup(name='muselsl',
      version='1.0.0',
      description='Stream and visualize EEG data from the Muse 2016 headset.',
      keywords='muse lsl eeg ble neuroscience',
      url='https://github.com/alexandrebarachant/muse-lsl/',
      author='Alexandre Barachant',
      author_email='alexandre.barachant@gmail.com',
      license='BSD (3-clause)',
      entry_points={
          'console_scripts': ['muselsl=muselsl.cli:main',],
      },
      cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
      },
      packages=find_packages(),
      package_data={'muselsl': ['docs/*']},
      include_package_data=True,
      zip_safe=False,
      install_requires=['bitstring', 'pylsl', 'pygatt==3.1.1',
                        'pandas', 'scikit-learn', 'numpy', 'seaborn', 'pexpect'],
      extras_require={'Viewer V2': ['mne', 'vispy']},
      classifiers=[
          # How mature is this project?  Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for.
          'Intended Audience :: Science/Research',
          'Topic :: Software Development',

          # Pick your license as you wish (should match "license" above).
          'License :: OSI Approved :: BSD License',

          # Specify the Python versions you support here.  In particular,
          # ensure that you indicate whether you support Python 2, Python 3 or both.
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',

          'Programming Language :: Python'])
