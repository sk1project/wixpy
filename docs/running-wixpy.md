# Running WiX.Py

## MS Windows
Windows version contains `wix.py.exe` binary accessible in system PATH. So just
type `wix.py <your-file-name>.json` to run application.

## Linux
Linux/Unix version uses `wix.py` script as an executable file. But command will 
be the same as for Windows version: `wix.py <your-file-name>.json`

## Inside Docker environment
WiX.Py is designed to be Docker compatible tool, i.e. it doesn't depend on 
windowing system or networking features. So just use WiX.Py inside Docker
container as a regular commandline application. You can install WiX.Py into
Docker image as a deb-package (Ubuntu, Debian images) or using `pip`.

Thus you can skip dedicated MSW cloud instance building MSI packages in 
CI service. This one decreases project infrastructure cost and speed-ups 
continuous integration builds.

---

[Return to help TOC](https://wix.sk1project.net/docs.php)