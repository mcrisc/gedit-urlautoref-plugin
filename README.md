Gedit URLAutoRef Plugin
===============================


Transforms pasted URLs into numbered references automatically


## Installing

Copy both files to your local Gedit plugin directory:

    mkdir -p ~/.local/share/gedit/plugins
    cp urlautoref.{plugin,py} ~/.local/share/gedit/plugins/


Open Gedit, go to `Edit -> Preferences -> Plugins` and activate
`URL Auto-Reference`.

This code was tested in Gedit 3.8.3.


## How to Use

In Gedit, type a `[` and paste the URL with 
<kbd>ctrl</kbd> + <kbd>v</kbd>. URLAutoRef will automatically turn it into a numbered reference like `[1]` and append the full address to a list at end of the file like:

    [1] http://github.com/
    [2] http://stackoverflow.com/

Inserting some blanks after your current line may be a good idea. Otherwise you'll get your reference list appended to the end of your current line.

