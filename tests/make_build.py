import os
import shutil

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    projdir = os.path.dirname(current_path)
    wixpy_path = os.path.join(projdir, 'src', 'wixpy')
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
