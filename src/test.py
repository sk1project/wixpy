import os
import shutil
import wixpy

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    wixpy_path = os.path.join(current_path, 'wixpy')
    projdir = os.path.dirname(current_path)
    app_icon = os.path.join(projdir, 'resources', 'wixpy.ico')

    # Prepare build dir
    builddir = os.path.join(projdir, 'build')
    if os.path.exists(builddir):
        shutil.rmtree(builddir, True)
    os.makedirs(builddir)
    dest = os.path.join(builddir, 'wixpy')
    shutil.copytree(wixpy_path, dest)
    exe_src = os.path.join(projdir, 'scripts', 'wix.py.exe')
    shutil.copy(exe_src, builddir)

    # MSI build data
    win64 = True
    MSI_DATA = {
        # Required
        'Name': wixpy.PROJECT,
        'UpgradeCode': '3AC4B4FF-10C4-4B8F-81AD-BAC3238BF690',
        'Version': wixpy.VERSION,
        'Manufacturer': 'sK1 Project',
        # Optional
        'Description': '%s %s Installer' % (wixpy.PROJECT, wixpy.VERSION),
        'Comments': 'Licensed under GPLv3',
        'Keywords': 'msi, wix, build',
        'Win64': win64,
        'Codepage': '1251',
        'SummaryCodepage': '1251',
        'Language': '1049',  # 1033
        'Languages': '1049',

        # Installation infrastructure
        '_OsCondition': 601,
        '_CheckX64': win64,
        '_Conditions': [],  # [[msg,condition,level], ...]
        '_AppIcon': app_icon,
        '_Icons': [],
        '_ProgramMenuFolder': 'sK1 Project',
        '_Shortcuts': [
            {'Name': wixpy.PROJECT,
             'Description': 'Crossplatform MSI builder',
             'Target': 'wix.py.exe',
             'Open': [],
             'OpenWith': [],
             'EditWith': [],
             },
        ],
        '_AddToPath': ['', ],
        '_AddBeforePath': [],
        '_SourceDir': builddir,
        '_InstallDir': 'wixpy-%s' % wixpy.VERSION,
        '_OutputName': '%s-%s-%s.msi' % (wixpy.PROJECT.lower(), wixpy.VERSION,
                                         'win64' if win64 else 'win32'),
        '_OutputDir': projdir,
        '_SkipHidden': True,
    }

    # MSI build
    try:
        # wixpy.build(MSI_DATA, xml_only=True, engine=Engine.WIXL, stdout=True)
        # wixpy.build(MSI_DATA, xml_only=True, stdout=True)
        wixpy.build(MSI_DATA)
    except Exception as e:
        raise e
    finally:
        pass
        shutil.rmtree(builddir, True)
