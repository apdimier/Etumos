from __future__ import absolute_import
from __future__ import print_function
import gtk.gdk

w = gtk.gdk.get_default_root_window()
w = gtk.gdk.get_display()
sz = w.get_size()
print("The size of the window is %d x %d" % sz)
pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
if (pb != None):
    pb.save("screenshot.png","png")
    print("Screenshot saved to screenshot.png.")
    pass
else:
    print("Unable to get the screenshot.")
    pass
    
    
def get_active_window_title(self):
    root_check = ''
    root = Popen(['xprop', '-root'],  stdout=PIPE)

    if root.stdout != root_check:
        root_check = root.stdout

        for i in root.stdout:
            if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                id_ = i.split()[4]
                id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
                pass
            pass
        id_w.wait()
        buff = []
        for j in id_w.stdout:
            buff.append(j)
            pass
        for line in buff:
            match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
            if match != None:
                type = match.group("type")
                if type == "STRING" or type == "COMPOUND_TEXT":
                    return match.group("name")
                pass
            pass
        pass
        return "Active window not found"


