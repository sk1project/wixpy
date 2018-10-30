import wixpy

MSI_DATA = {
    "Name": "WiX.Py",
    "UpgradeCode": "3AC4B4FF-10C4-4B8F-81AD-BAC3238BF690",
    "Version": "0.2",
    "Manufacturer": "sK1 Project",
    "Description": "WiX.Py 0.1 Installer",
    "Comments": "Licensed under GPLv3",
    "Keywords": "msi, wix, build",
    "Win64": True,
    "Codepage": "1251",
    "SummaryCodepage": "1251",
    "Language": "1049",
    "Languages": "1049",
    "_OsCondition": "601",
    "_CheckX64": True,
    "_Conditions": [],
    "_AppIcon": "../resources/wixpy.ico",
    "_Icons": [],
    "_ProgramMenuFolder": "sK1 Project",
    "_SourceDir": "../src",
    "_InstallDir": "wixpy-0.2",
    "_OutputName": "wixpy-0.2-win64.msi",
    "_OutputDir": "../",
    "_SkipHidden": True
}

# wixpy.build(MSI_DATA, xml_only=True, stdout=True)
wixpy.build(MSI_DATA)