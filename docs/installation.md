# WiX.Py installation
We have provided several ways to install WiX.Py depending on system: system 
specific packages, source code and PyPI.

## MS Windows

### MSI installer
If you are not familiar with Python, try using WiX.Py MSI package. Installer
contains Python binaries and adds WiX.Py into system PATH. So after installation
WiX.Py will be available as an executable command in command prompt.

### Installing from PyPI
Another way is installing Python 2.7 (we recommend to use py2 due to unicode
issues) and run `pip` to install WiX.Py from PyPI:
```
pip install WiX.Py
```
Please note that you need checking availability of your Python installation in 
system PATH. If not, add manually `[Python folder]` and `[Python folder]\Scripts`

### Installing from source code
The last option is installing from source code:

* Download WiX.Py source code tarball
* Unpack source code folder somewhere
* Run command `python setup.py install` in source code folder

As for PyPI install, you need installing Python 2.7 and place it in system PATH.

## Linux distributions

### Deb package
For Debian, Ubuntu, LinuxMint and other deb-based distors we are providing ready
deb-packages. To install package use the command:

```
sudo apt-get install ./<package-name>.deb
```

WiX.Py has not own native extensions. Therefore the content of all the packages 
is identical. Major difference for them is a dependency list. For access to libmsi
and libgcab libraries WiX.Py uses gobject introspection. To run WiX.Py 
you need installing libmsi, libgcab, their introspection stubs and python
gobject introspection package. In different distros the packages have different 
naming. If you installing WiX.Py deb-package on non-specified system, you need be
sure that required packages in system repositories have the same naming. You
may find some useful tips in [dependency.py](https://github.com/sk1project/wixpy/blob/master/dependencies.py)
file.

We don't create RPM packages because CentOS has no all required packages in
repositories. Other RPM distros are not used as a build instance usually. But 
you can install WiX.Py on Fedora and OpenSuse 15 from PyPI or from source code. 
Installation steps the same as for MS Windows platform.

### Installing from PyPI
To install from PyPI use command:

```
sudo pip install wix.py
```

Installer tries resolving dependencies described above. If not successful, 
installer print warning that you need resolving dependencies manually.

### Installing from source code
The last option is installing from source code:

* Download WiX.Py source code tarball
* Unpack source code folder somewhere
* Run command `sudo python setup.py install` in source code folder

## Other UNIX platforms
WiX.Py code is a pure Python code. So you could install it anywhere if you 
have Python installed. But you need installing libmsi, libgcab, their 
introspection stubs and python gobject introspection package. For example,
on macOS you could try using `brew install msitools` to install libmsi and 
libgcab. The issue is rather theoretical because there is no practical sense
for that.

---

[Return to help TOC](https://wix.sk1project.net/docs.php)