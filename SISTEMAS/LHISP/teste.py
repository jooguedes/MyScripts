import gi 
gi.require_version("Gtk", "3.0") 
from gi.repository import Gtk 
  
  
class MyWindow(Gtk.Window): 
    def __init__(self): 
      Gtk.Window.__init__(self, title ="GfG") 
      self.box = Gtk.Box(spacing = 6) 
      self.add(self.box) 
      self.button1 = Gtk.Button(label ="Click Here") 
      self.button1.connect("clicked", self.on_button1_clicked) 
      self.box.pack_start(self.button1, True, True, 0) 
  
    def on_button1_clicked(self, widget): 
        print("Welcome to Geeks for Geeks.") 
  
win = MyWindow() 
win.connect("destroy", Gtk.main_quit) 
win.show_all() 
Gtk.main()
