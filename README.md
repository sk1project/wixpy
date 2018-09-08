# WiX.Py
Cross-platform JSON-driven MSI package builder. Unlike a bunch of WiX/wixl 
wrappers (python-wix, go-msi, msi-packager etc.) WiX.Py is a standalone 
application. It uses libmsi on UNIX platforms and msi.dll on MS Windows.

Application has been designed for build toolchains under Docker environment,
i.e. it doesn't depend on windowing system or networking features. Thus it 
allows building MSI packages in CI services without dedicated MSW 
cloud instance. This one decreases project infrastructure cost and 
speed-ups builds.

Unlike WiX/wixl we don't propose users to use complex WXS file format and 
understanding MSI internal features. To build MSI package for your app 
you need creating just a small JSON file of 20-40 lines with description of 
MSI package features (application name, manufacturer, keywords etc.). 
No any magic or special knowledge.

We have designed WiX.Py first of all to build installers for small and medium 
size desktop applications. If you need complex enterprise features for your
installer you may use WiX.

Brief visual guide how to use WiX.Py is on the main page of project website: 
https://wix.sk1project.net

## WiX.Py features

* Crossplatform MSI package generation
* WXS file generation
* JSON-driven MSI build
* Recursive source folder scanning
* Localizable installer
* OS version check
* x64 architecture check
* Custom conditions
* 32/64bit installations
* MSI package icon
* ProgramMenu folder and shortcuts
* Desktop shortcuts
* Add to system PATH
* File type associations ('Open', 'Open with')
* MIME-type and icon for associated files
* 'Edit with' menu item for associated files

If you need some additional feature, submit feature request feature.
Installation and usage details see on project documentation page.

---

[Return to help TOC](https://wix.sk1project.net/docs.php)