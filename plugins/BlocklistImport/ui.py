
import gtk

class GTKConfig(gtk.Dialog):
    def __init__(self, plugin):
        gtk.Dialog.__init__(self, title="Blocklist Config",
                            flags=gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        # Setup
        self.set_border_width(12)
        self.vbox.set_spacing(6)

        # List source
        label = gtk.Label()
        label.set_markup('<b>Blocklist URL</b>')
        self.url = gtk.Entry()
        self.listtype = gtk.combo_box_new_text()
        self.listtype.append_text("PeerGuardian (GZip)")
        self.listtype.set_active(0)

        hbox = gtk.HBox(False, 6)
        hbox.pack_start(label)
        hbox.pack_start(self.url)
        hbox.pack_start(self.listtype)

        self.vbox.pack_start(hbox)

        # Load on start
        self.load_on_start = gtk.CheckButton("Load on start")
        self.vbox.pack_start(self.load_on_start)

        self.connect('response', self.ok)
        self.connect('close', self.cancel)

        self.hide_all()

        self.plugin = plugin


    def ok(self, dialog, response):
        self.hide_all()

        if response != gtk.RESPONSE_ACCEPT:
            self.cancel(dialog)
            return
        
        self.plugin.setconfig(self.url.get_text(),
                              self.load_on_start.get_active())
        
    def cancel(self, dialog, response):
        self.hide_all()

    def start(self):
        self.show_all()


class GTKProgress(gtk.Dialog):
    def __init__(self, plugin):
        gtk.Dialog.__init__(self, title="Loading Blocklist",
                            flags=gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        # Setup
        self.set_border_width(12)
        self.vbox.set_spacing(6)

        label = gtk.Label()
        label.set_markup('<b>Loading and installing blocklist</b>')
        self.vbox.pack_start(label)

        self.progress = gtk.ProgressBar()
        self.vbox.pack_start(self.progress)

        self.connect('close', self.cancel)

        self.hide_all()

    def start_download(self):
        self.progress.set_text("Downloading")
        self.update()

    def download_prog(self, fract):
        if fract > 1.0:
            fract = 1.0
        self.progress.set_fraction(fract)
        self.update()

    def start_import(self):
        self.progress.set_text("Importing")
        self.progress.set_pulse_step(0.0075)
        self.update()

    def import_prog(self):
        self.progress.pulse()
        self.update()

    def end_import(self):
        self.progress.set_text("Complete")
        self.progress.set_fraction(1.0)
        self.update()

    def cancel(self, dialog, response):
        self.hide_all()

    def start(self):
        self.show_all()
        self.update()

    def stop(self):
        self.hide_all()

    def update(self):
        while gtk.events_pending():
            not gtk.main_iteration(block=True)
