#!/usr/bin/env python

import gtk

layouts = {
    "us": "U.S.English",
    "es": "Spain/Mexico",
    "cf": "Canada/Quebec",
    "hu": "Hungria",
    "it": "Italia",
    "ru": "Russia",
    "uk": "United Kingdom",
    "fr-latin1": "France",
    "be-latin1": "Belgique",
    "br-abnt2": "Brazil",
    "croat": "Croat",
    "cz-lat2": "Czech",
    "de_CH-latin1": "Schweizer Deutsch",
    "nl2": "Netherlands",
    "no-latin1": "Norway",
    "pl2": "Poland",
    "pt-latin1": "Portugal",
    "se-lat6": "Sweden",
    "sg-latin1": "Singapore"}

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

xkb_settings_layout_dialog_run()
