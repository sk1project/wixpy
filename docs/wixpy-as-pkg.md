# Using WiX.Py as a Python package
WiX.Py builds WXS document model using JSON input data. And this model generates
MSI installer. During this process application coverts JSON file data into Python
dict structure. So you could simplify this process and use `wixpy` package
directly:

```
import wixpy

MSI_DATA = {
    'Name': 'MyApp',
    'UpgradeCode': '3AC4B4FF-19C5-4B8F-83AD-BAC3238BF690',
    'Version': '1.0',
    'Manufacturer': 'MyCompany',
    '_SourceDir': './build',
    '_InstallDir': 'myapp-1.0',
    '_OutputName': 'myapp-1.0-win32.msi',
    '_OutputDir': './'
    }
    
wixpy.build(MSI_DATA)

``` 

That is all you need to include MSI build in your CI infrastructure. Of course
you could extend MSI_DATA dict by additional fields described before. Here is just 
simplified example.

---

[Return to help TOC](https://wix.sk1project.net/docs.php)