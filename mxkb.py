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

    registry = xkb_config_get_xkl_registry()

    dialog = gt.Dialog("Add layout"
                      None,
                      gtk.GTK_DIALOG_MODAL | gtk.GTK_DIALOG_DESTROY_WITH_PARENT,
                      (gtk.GTK_STOCK_CANCEL, gtk.GTK_RESPONSE_CANCEL, gtk.GTK_STOCK_OK, gtk.GTK_RESPONSE_OK),
                      None)

    treestore = gtk_tree_store_new('gchararray', 'gchararray')

    #    xkl_config_registry_foreach_layout (registry, (ConfigItemProcessFunc)
    #            xkb_settings_add_layout_to_available_layouts_tree, treestore);

    renderer = gtk.CellRendererText()

    column = gtk.TreeViewVolumn(None,
                                renderer,
                                "text",
                                0,
                                None)


