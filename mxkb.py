#!/usr/bin/env python

import gtk, gtk.gdk, gobject
import xklavier
from xkb_config import xkb_config, xkb_settings, group_policy
data = [
    ["us", "U.S.English"],
    ["es", "Spain/Mexico"],
    ["cf", "Canada/Quebec"],
    ["hu", "Hungria"],
    ["it", "Italia"],
    ["ru", "Russia"],
    ["uk", "United Kingdom"],
    ["fr-latin1", "France"],
    ["be-latin1", "Belgique"],
    ["br-abnt2", "Brazil"],
    ["croat", "Croat"],
    ["cz-lat2", "Czech"],
    ["de_CH-latin1", "Schweizer Deutsch"],
    ["nl2", "Netherlands"],
    ["no-latin1", "Norway"],
    ["pl2", "Poland"],
    ["pt-latin1", "Portugal"],
    ["se-lat6", "Sweden"],
    ["sg-latin1", "Singapore"]]

treeview = None

def xci_desc_to_utf8 (ci):
    sd = ci.get_description()
    
    return ci.name if not sd else sd
        
class PyXKB:
    
    def __init__(self):
        self.iter = None
        self.child = None
        self.selection = None 
        
        xkb = xkb_settings()
        
        xkb.group_policy = group_policy.GLOBAL
        xkb.never_modify_config = False
        xkb.current = "us"
        xkb.tray_icon = gtk.Label(xkb.current)
        xkb.config_changed = False
        xkb.next = 1
        self.xkb_config = xkb_config(xkb, self.xkb_state_changed, xkb)
        
        self.open_config()
        
        xkb.mainw = gtk.EventBox()
        xkb.mainw.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        xkb.mainw.set_size_request(24, 24)
        
        xkb.mainw.add(xkb.tray_icon)
        
        xkb.mainw.show_all()
        xkb.mainw.set_tooltip_text("KeyBoard Layout Switcher")
        xkb.mainw.connect("button-press-event", self.tray_icon_press, xkb)
        
        wnd = gtk.Window()
        wnd.add(xkb.mainw)
        wnd.show_all()
        
        wnd.connect("destroy", gtk.main_quit)
        
        gtk.main()
        
    def add_layout(self, btn, combo):
        sel_layout = self.layout_dialog_run().split(",")
                
        model = self.treeview.get_model()
        self.iter = model.append(None)
    
        model.set(self.iter,
            0, False,
            1, sel_layout[0],
            2, sel_layout[2])
    
        #self.xkb_config.add_layout(sel_layout[0], sel_layout[1])
    
    def remove_layout(self, menuitem, userdata):
        self.selection = self.treeview.get_selection()
        model = self.treeview.get_model()
    
        if not self.selection.get_selected():
            temp, self.iter = selection.get_selected()
            del temp
    
            path = model.get_path(self.iter)
            layout_selected = path[0]
        
            model.remove(self.iter)

            #xkb_config_remove_group(layout_selected);

    def fixed_toggle(self, cell, path_str, model):
                
                cur = self.xkb_config.get_current_group()
                path = tuple(path_str.split(":"))
                                
                ind = path[0]
                
                if ind != cur:
                        self.iter = model.get_iter(path_str)
                        iter_old = model.get_iter(cur)
                
                        model.set(self.iter,
                                0, True)
                        model.set(iter_old,
                                0, False)
                print # xkb_config_set_group(*ind);
        
    def add_columns_selected_layouts(self):
        model = self.treeview.get_model()
                
        #column for fixed toggles
        renderer = gtk.CellRendererToggle()
        renderer.connect("toggled", self.fixed_toggle, model)
        
        renderer.set_radio(True)
        
        column = gtk.TreeViewColumn("default",
                renderer,
                active=0)

        self.treeview.append_column(column)
        
        #column for bug numbers
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Layout",
                renderer,
                text=1)
        
        column.set_sort_column_id(1)
        self.treeview.append_column(column)
        
        #column for severities
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Description",
                renderer,
                text=2)
        column.set_sort_column_id(2)
        self.treeview.append_column(column)

    def create_model_selected_layouts(self):
        store = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)
                
        current_group = self.xkb_config.get_current_group();
        group_count = self.xkb_config.get_group_count();
                
        for i in xrange(group_count):
            group_map = self.xkb_config.get_group_map(i);
            variant_map = self.xkb_config.get_variant_map(i);
            self.iter = store.append(None)

            store.set(self.iter,
                0, False if i != current_group else True,
                1, group_map,
                2, self.xkb_config.get_layout_desc(group_map, variant_map))
                
        return store
        
    def create_combo_box_model(self):
        #registry = xkb_config_get_xkl_registry ();
           
        store = gtk.TreeStore(gobject.TYPE_STRING)
            
        for i in xrange(len(data)):
            it = store.append(None)
            store.set(it,
                0, data[i][1])
                        
        return store
                
    def content_area(self):
        vbox = gtk.VBox(False, 0)
                
        #combo with layouts
        frame_layouts = gtk.Frame("Select one input language")
             
        hbox_layouts = gtk.HBox(False, 0)
               
        vbox.pack_start(frame_layouts, False, False, 0)
        hbox_layouts.set_border_width(5)
        frame_layouts.add(hbox_layouts)
             
        model = self.create_combo_box_model()
        combo_layouts = gtk.ComboBox(model)
        combo_layouts.set_active(0)
                
        hbox_layouts.add(combo_layouts)
                
        renderer = gtk.CellRendererText()
        combo_layouts.pack_start(renderer, False)
        combo_layouts.set_attributes(renderer, text=0)
              
        #treeview and buttons
        frame_tv = gtk.Frame("Selected Layouts")
        vbox_tv = gtk.VBox(False, 0)
        vbox.add(frame_tv)
        vbox_tv.set_border_width(5)
        frame_tv.add(vbox_tv)

        #scrolled window
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox_tv.pack_start(sw, True, True, 0)
        sw.set_size_request(-1, 150)
                
        #creating tree view
        model = self.create_model_selected_layouts()
        self.treeview = gtk.TreeView(model)
        sw.add(self.treeview)

        self.add_columns_selected_layouts()
         
        #creating buttons
        hbox_btn = gtk.HButtonBox()
        hbox_btn.set_border_width(5)
        vbox_tv.add(hbox_btn)
                
        hbox_btn.set_layout(gtk.BUTTONBOX_END)
        hbox_btn.set_spacing(8)
                
        button = gtk.Button(stock=gtk.STOCK_ADD)
        hbox_btn.add(button)
               
        button.connect("clicked", self.add_layout, None)
                
        button = gtk.Button(stock=gtk.STOCK_REMOVE)
        hbox_btn.add(button)
               
        button.connect("clicked", self.remove_layout, None)
                
        button = gtk.Button(stock=gtk.STOCK_EDIT)
        hbox_btn.add(button)
                
        #creating checkbox
        check = gtk.CheckButton("Manage layouts per application")
        vbox.pack_start(check, False, False, 0)
        vbox.set_border_width(5)
                
        return vbox
                
    def register_layout(self, config_registry, config_item, treestore):
        utf_layout_name = xci_desc_to_utf8(config_item)
        
        self.iter = treestore.append(None)
        treestore.set(self.iter,
            0, utf_layout_name,
            1, config_item.get_name())
        
        config_registry.foreach_layout_variant(config_item.get_name(),
            self.register_variant,
            treestore)
        
    def register_variant(self, config_registry, config_item, treestore):
        utf_variant_name = xci_desc_to_utf8(config_item)
        
        self.child = treestore.append(self.iter)
        treestore.set(self.child,
            0, utf_variant_name,
            1, config_item.get_name())
    #Switcher implementation
    def change_current_layout(self):
        self.xkb_config.next_group()
                
    def tray_icon_press(self, widget, event, userdata):
        if event.button == 3: #right button
            self.config()
            return True
    
        self.change_current_layout()

    def config(self):
        dlg = gtk.Dialog("Keyboard layouts settings",
            flags=gtk.DIALOG_MODAL,
            buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        
        dlg.resizable = False
        dlg.vbox.add(self.content_area())
             
        dlg.show_all()
        response = dlg.run()
                
        dlg.destroy()
                
    def save_config(self):
        pass

    def open_config(self):
        pass
        
    def layout_dialog_run(self):
        t_view = gtk.TreeView()
        
        registry = self.xkb_config.get_xkl_registry()
    
        dialog = gtk.Dialog("Add layout",
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
    
        treestore = gtk.TreeStore('gchararray', 'gchararray')
    
        registry.foreach_layout(self.register_layout, treestore);
    
        renderer = gtk.CellRendererText()
    
        column = gtk.TreeViewColumn(None,
            renderer,
            text=0)
            
        t_view.set_model(treestore)
        t_view.append_column(column)
        
        treestore.set_sort_column_id(0, gtk.SORT_ASCENDING)
        
        scrolledw = gtk.ScrolledWindow()
        dialog.vbox.add(scrolledw)
        scrolledw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolledw.show()
        scrolledw.add(t_view)
        
        t_view.show()
    
        dialog.set_default_size(360,420)
        dialog.show()
        response = dialog.run()
    
        if response == gtk.RESPONSE_OK:
            print "response_ok"
            self.selection = t_view.get_selection()
            
            model, self.iter = self.selection.get_selected()
            desc, id = model.get(self.iter, 0, 1)
            path = model.get_path(self.iter)
            
            if model.iter_depth(self.iter) == 0:
                strings = [id, ""]
            else:
                strings = [None, id]
                path = model.get_path(model.iter_parent(self.iter))
                self.iter = model.get_iter(path)
                group_desc, id = model.get(model, self.iter, 0, 1)
                strings[0] = id
                desc = "%s(%s)" % (group_desc, desc)
        
            dialog.destroy()
            
            return ",".join((strings[0], strings[1], desc))
                
        dialog.destroy()
        return None
    def xkb_state_changed(self, current_group, config_changed, settings):
        self.update_display(settings)
    
    def update_display(self, settings):
        pass
#wnd = gtk.Window()
#vbox = lxkb_content_area()
#vbox.show_all()
#wnd.add(vbox)
#wnd.show()
#gtk.main()

pyxkb = PyXKB()
#pyxkb.config()

#lxkb_config()

#xkb_settings_layout_dialog_run()
