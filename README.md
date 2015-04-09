Clang-Complete
=============

A clang plugin for Sublime Text 3 (MAC OSX / Linux), providing:
- Auto complete
- Syntax diagnostic
- Goto definition

Using libclang (llvm 3.5.0). 

## Install the Plugin

#### From git repository

Note: To determine the path to Sublime Text 3 Packages directory, start Sublime Text 3, Choose menu `Preferences` -> `Browse Packages` 

```
$ cd <sublime-text-3 Packages directory>  # see note above
$ git clone https://github.com/lvzixun/clang-complete.git
$ cd clang-complete
$ make [linux]
$ make install
```
On Ubuntu, `$ make linux`, On Mac OSX, run the default `$ make`.

 
#### From package control
1. Install [package control](https://packagecontrol.io/installation)
2. `command+shift + p` -> `install package`
3. Search `Clang-Complete` -> install

Installation using Package Control is only support on Mac.


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

if `"cc_include_options"` exists in your project settings, it will override rather than add
to the `"include_options"` defined in `cc.sublime-settings`.


## Preview
<img src="http://ww4.sinaimg.cn/large/7608d17fgw1eo4dgrggc0g20da0bi44p.gif" width="50%" />

## Support
[Donate](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9SSZZ9NYW9F6E)



## TODO LIST
| feature | status |
|:--------:|:-------:|
| support mac osx | done |
| support linux  | done |
| support window | X |
| support sublimetext 2 | X |
