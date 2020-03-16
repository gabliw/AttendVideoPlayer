# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import kivy_deps
import ffpyplayer

# added_files = [ ('info.json', '.')]
added_files = []

a = Analysis(['main.py'],
             pathex=['your project path and add (\\AttendVideoPlayer)'],
             binaries=[('find your envs path and add (\\Lib\\site-packages\\cv2\\opencv_videoio_ffmpeg420_64.dll)', '.')],
             datas=added_files,
             hiddenimports=['pkg_resources.py2_warn', 'ffpyplayer','ffpyplayer.pic', 'win32timezone',
    'ffpyplayer.threading', 'ffpyplayer.tools', 'ffpyplayer.writer',
    'ffpyplayer.player', 'ffpyplayer.player.clock', 'ffpyplayer.player.core',
    'ffpyplayer.player.decoder', 'ffpyplayer.player.frame_queue',
    'ffpyplayer.player.player', 'ffpyplayer.player.queue',
    'numpy.random.common', 'numpy.random.bounded_integers',
    'numpy.random.entropy', 'plyer.platforms.win.filechooser'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AttendVideoPlayer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)