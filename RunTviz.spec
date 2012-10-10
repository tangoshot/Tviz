# -*- mode: python -*-
a = Analysis(['RunTviz.py'],
             pathex=['C:\\CodeBench\\tviz'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'RunTviz.exe'),
          debug=False,
          strip=None,
          upx=False,
          console=True )
