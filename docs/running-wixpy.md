# Running WiX.Py

## MS Windows
Windows version contains `wix.py.exe` binary accessible in system PATH. So just
type `wix.py <your-file-name>.json` to run application.

## Linux
Linux/Unix version uses `wix.py` script as an executable file. But command will 
be the same as for Windows version:
```
wix.py <your-file-name>.json
```

## Generation GUID
For you app you need unique GUIDs. You could generate them using WiX.Py:
```
wix.py --generate_guid
```

## Inside Docker environment
WiX.Py is designed to be Docker compatible tool, i.e. it doesn't depend on 
windowing system or networking features. So just use WiX.Py inside Docker
container as a regular commandline application. You can install WiX.Py into
Docker image as a deb-package (Ubuntu, Debian images) or using `pip`.

Thus you can skip dedicated MSW cloud instance building MSI packages in 
CI service. This one decreases project infrastructure cost and speed-ups 
continuous integration builds.

# Preparing source folder
To prepare application source folder just copy all the files and directories
into some folder. The folder name does not matter. For example, you can use
`build` name. Source folder content should be the same as you need installing
on target machine in `ProgramFiles`. Installation folder name will be specified
in json file.

Resource files like icon for MSI package can be placed outside source folder
because they will not be in installation folder on target machine.

---

[Return to help TOC](https://wix.sk1project.net/docs.php)
