

import sys
import os
import shutil

python_install_dir = os.path.dirname(sys.executable)
gsf_package_dir = os.path.join(python_install_dir, 'Lib', 'site-packages', 'gsf')
shutil.rmtree(gsf_package_dir)
ese_package_dir = os.path.join(python_install_dir, 'Lib', 'site-packages', 'ese')
shutil.rmtree(ese_package_dir)