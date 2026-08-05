[app]
title = 潛執の囚禁
package.name = imprisonment
package.domain = game.imprison
source.dir = .
source.include_exts = py,png,jpg,mp3,webp,flac
version = 0.5.4
requirements = python3,pygame_sdl2,sdl2
orientation = landscape
osx.kivy_version = 2.2.0
fullscreen = 1
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
env.SDL_GL_ACCELERATED_VISUALS = 1
android.fps = 180
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.wakelock = True
entrypoint = __main__.py
