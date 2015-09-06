Clang-Complete
=============

A clang plugin for Sublime Text 3 (MAC OSX / Linux / Windows), providing:
- Auto complete
- Syntax diagnostic
- Goto definition

Using libclang (llvm 3.5.0). 

## Install the Plugin

#### From git repository

Note: To determine the path to Sublime Text 3 Packages directory, start Sublime Text 3, Choose menu `Preferences` -> `Browse Packages` 

```
$ cd <sublime-text-3 Packages directory>  # see note above
$ git clone https://github.com/lvzixun/Clang-Complete.git
$ cd Clang-Complete
$ make [linux / windows]
```
On Ubuntu, `$ make linux`, On Mac OSX, run the default `$ make`.

##### Windows prerequisites(only if you want to compile yourself)

1. install MINGW-W64 32 e.g. from [here](http://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.4/threads-posix/dwarf/i686-4.8.4-release-posix-dwarf-rt_v3-rev0.7z/download)
2. install [LLVM 3.6.1](http://llvm.org/releases/3.6.1/LLVM-3.6.1-win32.exe)(binary is included in `lib` directory)

 
#### From package control
1. Install [package control](https://packagecontrol.io/installation)
2. `command+shift + p` -> `install package`
3. Search `Clang-Complete` -> install

Installation using Package Control is only supported on Mac.


## Configuration

Global options can be set in `<sublime-text-3 Packages directory>/clang-complete/cc.sublime-settings` file. Header files can be included in the `include_options` section.

Alternatively, header files can also be included from the Sublime Text 3 `<name>.sublime-project` files by adding the `cc_include_options` subsection to the `settings` section in your `<name>.sublime-project` file:

~~~~.js
"settings":
{
    "cc_include_options":
    [
        "-I/headfile_path1",
        "-I/headfile_path2",
        "-I/headfile_path3"
        // ...
    ]
     // ...
}
~~~~


Example settings for Windows:

~~~~.js
    "settings":
    {
        "cc_include_options":
        [
            "-isystem", "C:\\MinGW\\i686-w64-mingw32\\include",
            "-isystem", "C:\\MinGW\\i686-w64-mingw32\\include\\c++",
            "-isystem", "C:\\MinGW\\i686-w64-mingw32\\include\\c++\\tr1",
            "-isystem", "C:\\MinGW\\i686-w64-mingw32\\include\\c++\\i686-w64-mingw32",
            "-isystem", "C:\\LLVM\\lib\\clang\\3.6.1\\include",
            "-DBOOST_USE_WINDOWS_H"
        ]
    }
~~~~


if `"cc_include_options"` exists in your project settings, it will merge to
the `"include_options"` defined in `cc.sublime-settings`.


## Preview
<img src="http://ww4.sinaimg.cn/large/7608d17fgw1eo4dgrggc0g20da0bi44p.gif" width="50%" />

## Donate
[Paypal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9SSZZ9NYW9F6E)

alipay支付宝账号: lvzixun@gmail.com 



## TODO LIST
| feature | status |
|:--------:|:-------:|
| support mac osx | done |
| support linux  | done |
| support window | done |
| support sublimetext 2 | X |
