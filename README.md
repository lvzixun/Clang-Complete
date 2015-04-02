clang-complete
=============

A clang plugin for sublime text3(MAC OSX), providing auto complete, syntax diagnostic and goto definition, using libclang(llvm 3.5.0). 


## install plugin

#### install plugin from git respositiory

```
$ git clone https://github.com/lvzixun/clang-complete.git
$ make
$ make install
```

#### install plugin from package control
1. install [package control](https://packagecontrol.io/installation)
2. `command+shift + p` -> `install package`
3. search `Clang-Complete` -> install

## setting config
set global options in `<sublime text3>/Packages/cc.sublime-ettings` file. you can add custom headfile at `include_options` section. 
this can also be specified as project specific options.
add somthing like the following to the `settings` section in your `<name>.sublime-project` file:


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
if `"cc_include_options"` exists in your project settings, it'll override rather than add
to the `"include_options"` defined in `cc.sublime-settings`.


## preview
<img src="http://ww4.sinaimg.cn/large/7608d17fgw1eo4dgrggc0g20da0bi44p.gif" width="50%" />