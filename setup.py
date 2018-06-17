from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from shutil import copyfile
import os
import platform
import subprocess

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        if(check_install_bluemuse(True)): install_bluemuse()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        if(check_install_bluemuse()): install_bluemuse()
        install.run(self)

def install_bluemuse():
    powerShellPath = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
    remove = "./bluemuse_dist/Remove-AppOldPackage.ps1"
    install = './bluemuse_dist/Add-AppDevPackage.ps1'
    subprocess.call([powerShellPath, '-ExecutionPolicy', 'Unrestricted', remove])
    subprocess.call([powerShellPath, '-ExecutionPolicy', 'Unrestricted', install])

def check_install_bluemuse(ask_user = False):
    platformName = platform.system().lower()
    if platformName == 'windows' and int(platform.version().replace('.', '')) >= 10015063:
        if d: return True
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
      package_data={'': ['bluemuse_dist/*'], 'muselsl': ['docs/*']},
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
