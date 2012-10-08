# -*- mode: python -*-
a = Analysis(['run.py'],
             pathex=['C:\\CodeBench\\tvizpy'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'run.exe'),
          debug=False,
          strip=None,
          upx=False,
          console=True )
