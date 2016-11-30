# Copyright 2014 Richar Nunez - rnezferreira9@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import logging

from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton

from ConfigParser import SafeConfigParser


ORANGE = "#FCB947"


class HablandoGuarani(activity.Activity):

    def __init__(self, handle):

        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1
        self.parser = SafeConfigParser()
        self.parser.read('config.ini')

        self.__make_toolbar()

        # label with the text, make the string translatable
        eb = Gtk.EventBox()
        eb.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('White')[1])
        self.set_canvas(eb)

        win = Gtk.VBox()
        eb.add(win)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file('images/logo.jpg')
        win.add(Gtk.Image.new_from_pixbuf(pixbuf.scale_simple(400, 100, GdkPixbuf.InterpType.BILINEAR)))

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        win.add(self.textview)
        
        self.buttonbox_letters = Gtk.HButtonBox()  
        self.buttonbox_letters.set_layout(Gtk.ButtonBoxStyle.CENTER)
        win.add(self.buttonbox_letters)

        bo1 = self.make_button('A', ORANGE)
        bo2 = self.make_button('E')
        bo3 = self.make_button('I', ORANGE)
        bo4 = self.make_button('O')
        bo5 = self.make_button('U', ORANGE)
        bo6 = self.make_button('Y')
        bo7 = self.make_button('G', ORANGE)

        hbox2 = Gtk.HBox()
        win.add(hbox2)

        achehety = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('images/achegety.jpg')
        achehety.set_from_pixbuf(pixbuf.scale_simple(600, 200, GdkPixbuf.InterpType.BILINEAR))
        win.add(achehety)

        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.translate_cb)
        self.entry.connect("backspace", self.backspace_cb)
        win.add(self.entry)

        dic = Gtk.TextView()
        dic.set_wrap_mode(Gtk.WrapMode.WORD)
        dic.set_editable(False)

        scroll = Gtk.ScrolledWindow()
        scroll.set_border_width(10)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)
        scroll.add(dic)
        win.add(scroll)

        self.show_all()
        self.load_file(dic.get_buffer())

    def __make_toolbar(self):
        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()
        toolbar_box.toolbar.show_all()

    def make_button(self, letter, color=None):
        button = Gtk.Button(self.parser.get('dic',letter))
        button.connect('clicked', self.add_letter, letter)
        self.buttonbox_letters.add(button)

        if color != None:
            button.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse(color)[1])

    def add_letter(self, widget, letter):
        parser = SafeConfigParser()
        parser.read('config.ini')
        self.entry.set_text(self.entry.get_text() + parser.get('dic', letter))

    def load_file(self, textbuffer):
        path = "lang/guarani/dic.txt"
        infile = open(path, "r")

        with open(path) as file:
            string = file.read()
            textbuffer.set_text(string)
            file.close()


    def translate_cb(self, widget):
        entry = self.entry.get_text()+' = '
        cargar = self.textview.get_buffer()
        infile = "lang/guarani/dic.txt"

        with open(infile, 'r') as f:
            for line in f:
                if line.lstrip().startswith(entry.capitalize()):
                    line = line.rstrip()
                    cargar.set_text(line) 
                    break

            if entry != line:
                cargar.set_text('No se ha encontrado coincidencia')

    def backspace_cb(self, widget):
        cargar = self.textview.get_buffer()
        cargar.set_text('')
