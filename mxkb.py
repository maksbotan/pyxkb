#!/usr/bin/env python

import gtk, gobject

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
    #TODO: libxklavier
    pass

def xkb_settings_add_variant_to_available_layouts_tree (config_registry, config_item, treestore):
    #TODO: libxklavier
    pass

def xkb_settings_layout_dialog_run():
    t_view = gtk.TreeView()

#    registry = xkb_config_get_xkl_registry()

    dialog = gtk.Dialog("Add layout",
                      None,
                      gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                      (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))

    treestore = gtk.TreeStore('gchararray', 'gchararray')

    #    xkl_config_registry_foreach_layout (registry, (ConfigItemProcessFunc)
    #            xkb_settings_add_layout_to_available_layouts_tree, treestore);

    iter = treestore.append(None)
    treestore.set(iter, 0, "ru", 1, "ru")

    child = treestore.append(iter)
    treestore.set(child, 0, "ru-1", 1, "2")

    renderer = gtk.CellRendererText()

    column = gtk.TreeViewColumn(None,
                                renderer,
                                text=0)

    t_view.set_model(treestore)
    t_view.append_column(column)

    treestore.set_sort_column_id(0, gtk.SORT_ASCENDING)

    scrolledw = gtk.ScrolledWindow()
    scrolledw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrolledw.show()
    scrolledw.add(t_view)

    dialog.vbox.add(scrolledw)

    t_view.show()

    dialog.set_default_size(360,420)
    dialog.show()
    response = dialog.run()

    if response == gtk.RESPONSE_OK:
        selection = t_view.get_selection()
        
        model, iter = selection.get_selected()
        desc, id = model.get(iter, 0, 1)
        path = model.get_path(iter)
        
        if model.iter_depth(iter) == 1:
            strings = [id, ""]
        else:
            strings = [None, id]
            path = model.get_path(model.iter_parent(iter))
            iter = model.get_iter(path)
            group_desc, id = model.get(model, iter, 0, 1)
            string[0] = id
            desc = "%s(%s)" % (group_desc, desc)

        dialog.destroy()
        return ",".join((strings[0], strings[1], desc))
    
    dialog.destroy()
    return None

def lxkb_add_layout(btn, combo):
    sel_layout = xkb_settings_layout_dialog_run().split(",")

    model = treeview.get_model()
    iter = model.append

    model.set(iter,
        0, False,
        1, sel_layout[0],
        2, sel_layout[2])

     #xkb_config_add_layout(sel_layout[GROUP_MAP], sel_layout[VARIANT_MAP]);

def lxkb_remove_layout(menuitem, userdata):
    selection = treeview.get_selection()
    model = treeview.get_model()

    if not selection.get_selected():
        temp, iter = selection.get_selected()
        del temp

        path = model.get_path(iter)
        layout_selected = path[0]

        treestore.remove(model, iter)

#        xkb_config_remove_group(layout_selected);

def fixed_toggle(cell, path_str, model):
#      cur = xkb_config_get_current_group();
    path = path_str.split(":")
    path_old = (cur, )

    ind = path[0]

    if ind != cur:
        iter = model.get_iter(path)
        iter_old = model.get_iter(path_old)

        model.set(iter,
            0, True)
        model.set(iter_old,
            0, False)

#      xkb_config_set_group(*ind);

def lxkb_add_columns_selected_layouts():
    model = treeview.get_model()

    #column for fixed toggles
    renderer = gtk.CellRendererToggle()
    renderer.connect("toggled", fixed_toggle, model)

    renderer.set_radio(True)

    column = gtk.TreeViewColumn("default",
        renderer,
        active=0)

    treeview.append_column(column)
    
    #column for bug numbers
    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Layout",
        renderer,
        text=1)

    column.set_sort_column_id(1)
    treeview.append_column(column)

    #column for severities
    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Description",
        renderer,
        text=2)
    column.set_sort_column_id(2)
    treeview.append_column(column)

def lxkb_create_model_selected_layouts():
    store = gtk.ListStore(
        gobject.TYPE_BOOLEAN,
        gobject.TYPE_STRING,
        gobject.TYPE_STRING)

#  current_group = xkb_config_get_current_group();
#  group_count = xkb_config_get_group_count();
    current_group = 0
    group_count = 1

    for i in xrange(group_count):
#      group_map = xkb_config_get_group_map(i);
#      variant_map = xkb_config_get_variant_map(i);
        iter = store.append()
#        store.set(iter,
#            0, False if i != current_group else True,
#            1, group_map,
#            2, xkb_config_get_layout_desc(group_map, variant_map))

    return store

def lxkb_create_combo_box_model():
#   registry = xkb_config_get_xkl_registry ();
    
    store = gtk.TreeStore(gobject.TYPE_STRING)

    for i in xrange(len(data)):
        it = store.append(None)
        store.set(it,
            0, data[i][1])
    
    return store

def lxkb_content_area():
    vbox = gtk.VBox(False, 0)

    #combo with layouts
    frame_layouts = gtk.Frame("Select one input language")

    hbox_layouts = gtk.HBox(False, 0)

    vbox.pack_start(frame_layouts, False, False, 0)
    hbox_layouts.set_border_width(5)
    frame_layouts.add(hbox_layouts)

    model = lxkb_create_combo_box_model()

    combo_layouts = gtk.ComboBox(model)
    combo_layouts.set_active(0)

    hbox_layouts.add(combo_layouts)

    renderer = gtk.CellRendererText()
    combo_layouts.pack_start(renderer, False)
#    gtk.CellLayout.set_attributes(combo_layouts,text=0)

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
    model = lxkb_create_model_selected_layouts()
    treeview = gtk.TreeView(model)
    sw.add(treeview)

    #creating buttons
    hbox_btn = gtk.HButtonBox()
    hbox_btn.set_border_width(5)
    vbox_tv.add(hbox_btn)

    hbox_btn.set_layout(gtk.BUTTONBOX_END)
    hbox_btn.set_spacing(8)

    button = gtk.Button(stock=gtk.STOCK_ADD)
    hbox_btn.add(button)

    button.connect("clicked", lxkb_add_layout, None)

    button = gtk.Button(stock=gtk.STOCK_REMOVE)
    hbox_btn.add(button)

    button.connect("clicked", lxkb_remove_layout, None)

    button = gtk.Button(stock=gtk.STOCK_EDIT)
    hbox_btn.add(button)

    #creating checkbox
    check = gtk.CheckButton("Manage layouts per application")
    vbox.pack_start(check, False, False, 0)
    vbox.set_border_width(5)

    return vbox

#Switcher implementation
def change_current_layout():
#    xkb_config_next_group ()
    pass
    
def tray_icon_press(widget, event, userdata):
    if event.button == 3: #right button
        #popup menu
        return True

    change_current_layout()

def lxkb_config():
    dlg = gtk.Dialog("Keyboard layouts settings",
        flags=gtk.DIALOG_MODAL,
        buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

    dlg.resizable = False
    dlg.vbox.add(lxkb_content_area())

    dlg.show_all()
    response = dlg.run()
    
    dlg.destroy()

def lxkb_save_config():
    pass

def lxkb_open_config():
    pass

def lxkb_constructor():
    pass


#wnd = gtk.Window()
#vbox = lxkb_content_area()
#vbox.show_all()
#wnd.add(vbox)
#wnd.show()
#gtk.main()

lxkb_config()

#xkb_settings_layout_dialog_run()
