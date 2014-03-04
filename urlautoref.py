#coding: utf-8
"""URL Auto-Reference Gedit Plugin

author: Marcelo Criscuolo <criscuolo.marcelo@gmail.com>
date: 2014-03-03
"""

import re
from gi.repository import GObject, Gedit, Gtk

# Useful Resources
# ----------------
# Gedit Plugin HowTo 
#   https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo
# GI API Reference
#   http://lazka.github.io/pgi-docs/api/Gtk_3.0/classes/TextBuffer.html
# Gedit Reference Manual
#   https://developer.gnome.org/gedit/stable/gedit-gedit-document.html
# tab-added signal
#   http://stackoverflow.com/a/14358423/215459


class ReferenceBase(object):
    def __init__(self):
        self.count = 0
        self.references = {}

    def get_reference(self, url):
        if url not in self.references:
            self.count += 1
            self.references[url] = self.count
        return self.references[url]

    def update(self, entries):
        """Loads base with entries.

        entries - sequence of (url, ref) tuples
        """
        self.count = len(entries)
        self.references.update(entries)

    def __contains__(self, url):
        return url in self.references


class URLAutoRefPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = 'URLAutoRefPlugin'
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        handler = self.window.connect('tab-added', self._on_tab_added)
        self.window.urlautoref_handler = handler

    def do_deactivate(self):
        self.window.disconnect(self.window.urlautoref_handler)

    def do_update_state(self):
        pass

    @staticmethod
    def extract_references(doc):
        end = doc.get_end_iter()
        # locating first reference entry, if any
        found = end.backward_search('[1]', 
                Gtk.TextSearchFlags.TEXT_ONLY, None)
        if not found:
            return []
        start = found[0]
        text = doc.get_text(start, end, False)
        entries = re.findall(r'\[(\d+)\]\s+(\S+)', text)
        entries = [(url, int(ref)) for ref, url in entries]
        return entries

    @staticmethod
    def is_url(text):
        protocols =  ['http:', 'https:', 'file:']
        return any(map(text.startswith, protocols))

    def _on_tab_added(self, window, tab, data=None):
        doc = tab.get_document()
        mime = doc.get_mime_type()
        if mime == 'text/plain':
            doc.refbase = ReferenceBase()
            doc.connect('paste_done', self._on_paste_done)
            doc.connect('loaded', self._on_loaded)

    def _on_loaded(self, doc, data):
        entries = URLAutoRefPlugin.extract_references(doc)
        doc.refbase.update(entries)

    def _on_paste_done(self, doc, clipboard):
        pasted_text = clipboard.wait_for_text()
        if not URLAutoRefPlugin.is_url(pasted_text):
            return
        # getting document region (including one char before)
        start = doc.get_iter_at_mark(doc.get_insert())
        start.backward_chars(len(pasted_text)+1)
        end = doc.get_iter_at_mark(doc.get_insert())
        doc_text = doc.get_text(start, end, False)
        # if user typed a '[' before pasting the URL
        if doc_text[0] == '[':
            url = pasted_text
            in_refbase = url in doc.refbase
            ref = doc.refbase.get_reference(url)
            doc.delete(start, end)
            citation = '[%d]' % ref
            doc.insert_at_cursor(citation, len(citation))
            if not in_refbase:
                ref_entry = '[%d] %s\n' % (ref, url)
                doc.insert(doc.get_end_iter(), ref_entry, len(ref_entry))

