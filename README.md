URL Auto-Reference Gedit Plugin
===============================


Transforms pasted URLs into numbered references compatible with [Markdown syntax][3].


## Installing

Copy plugin files to your local Gedit plugin directory:

    mkdir -p ~/.local/share/gedit/plugins
    cp urlautoref.{plugin,py} ~/.local/share/gedit/plugins/


Open Gedit, go to `Edit -> Preferences -> Plugins` and activate
`URL Auto-Reference`.

This code was tested in Gedit 3.8.3.


## How to Use

In Gedit, type a `[` and paste the URL with 
<kbd>ctrl</kbd> + <kbd>v</kbd>. URLAuto-Ref will automatically turn it into a numbered reference like `[1]` and append the full address to a list at end of the file like:

    [1]: http://github.com/
    [2]: http://stackoverflow.com/

When starting a new file, inserting some blanks after your first line may be a good idea. Otherwise you'll get the reference list appended to it.

[3]: http://daringfireball.net/projects/markdown/syntax#link

