import cx_Freeze as cx
import sys
import os
import platform

cwd = os.getcwd()
icon_loc = os.path.join(os.path.join(cwd, 'images'), 'chilloi.ico')
include_files = [
    (os.path.join(cwd, 'images'), 'images')
]

if platform.system() == 'Windows':
    PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))
    os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tk8.6')

    include_files += [
        (os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
        (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), '')
    ]

base = None
target_name = 'desktop'
if platform.system() == "Windows":
    base = "Win32GUI"
    target_name = 'billingsoftware.exe'
    shortcut_data = [
        ('DesktopShortcut', 'DesktopFolder', 'Billing Software', 'TARGETDIR', '[TARGETDIR]' + target_name, None, 'Billing Software application', None, None, None, None,'TARGETDIR'),
        ('MenuShortcut', 'ProgramMenuFolder', 'Billing Software', 'TARGETDIR', '[TARGETDIR]' + target_name, None, 'Billing Software application', None, None, None, None,'TARGETDIR'),
    ]
cx.setup(
    name='Billing Software',
    version='1.0',
    author='Anas Nadeem',
    author_email='anas5678go@gmail.com',
    description='Billing Software.',
    # packages=['billing_software'],
    options={
        'build_exe':{
            'include_files':include_files,
            "packages": ["reportlab", "psycopg2","num2words"],
            # "excludes": ["tkinter"],
        },
        'bdist_msi':{
            'upgrade_code':'{12345678-90AB-CDEF-1234-567890ABCDEF}',
            'data':{'Shortcut':shortcut_data}
        }
    },
    executables = [cx.Executable("login_dash.py", base=base, target_name=target_name, icon=icon_loc)],
)
