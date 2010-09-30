#!/usr/bin/env python

import gtk, gtk.gdk
import xklavier

class group_policy:
    GLOBAL = 0
    PER_WINDOW = 1
    PER_APPLICATION = 2

class xkb_kbd_config:
    model = None
    layouts = None
    variants = None
    options = None
    toggle_option = None


class xkb_settings:
    #plugin = None
    mainw = None
    tray_icon = None
    current = None
    group_policy = None
    default_group = None
    never_modify_config = None
    config_changed = None
    kbd_config = None
    next = None
    
class xkb_config:
    def __init__(self, settings, callback, callback_data):
        self.settings = settings
        self.callback = callback
        self.callback_data = callback_data
        
        self.config_rec = None
        
        self.engine = xklavier.Engine(gtk.gdk.display_get_default())
        
        if not self.engine:
            return None
        
        self.update_settings(settings);
        
        self.engine.set_group_per_toplevel_window (False);
        
        cur = self.get_current_group()
        self.settings.current = cur
        
        self.engine.start_listen(xklavier.XKLL_TRACK_KEYBOARD_STATE);
        
        self.engine.connect("X-state-changed", self.state_changed, None)
        self.engine.connect("X-config-changed", self.config_changed, None)
        
        #gdk_window_add_filter (NULL, (GdkFilterFunc) handle_xevent, NULL);
        
        return None
        
    def initialize_xkb_options(self, settings):
        state = self.engine.get_current_state()
        self.group_count = len(self.config_rec.get_layouts())
        
        self.window_map = {}
        self.application_map = {}
        
        registry = xklavier.ConfigRegistry(self.engine)
        registry.load(False)
        config_item = xklavier.ConfigItem()
        
        self.group_names = []
        self.variants = []
        self.variant_index_by_group = {}
        index_variants = {}
        
        for i in xrange(self.group_count):
            config_item.name = self.config_rec.get_layouts()[i]
            self.group_names.append(self.config_rec.get_layouts()[i])
            
            try:
                config_item.name = self.config_rec.get_variants()[i]
            except:
                pass
                
            try:
                self.variants.append(self.config_rec.get_variants()[i])
            except:
                self.variants.append("")
            
            val = index_variants.get(self.group_names[i])
            
            self.variant_index_by_group[self.group_names[i]] = val
            index_variants[self.group_names[i]] = val
        
    def get_current_group(self):
        state = self.engine.get_current_state()
        print state
        return state["group"]
        
    def set_group(self, grooup):
        if group <0 or group > self.group_count:
            return False
        
        #xkl_engine_lock_group (config->engine, group);
        return True
    
    def next_group(self):
        #xkl_engine_lock_group (config->engine,
        #xkl_engine_get_next_group (config->engine));
        print "next group"
        pass
    
    def update_settings(self, settings):
        if not self.config_rec:
            self.config_rec = xklavier.ConfigRec()
    
        if (settings.kbd_config == None) or (settings.never_modify_config):
            self.config_rec.get_from_server (self.engine)
            activate_settings = False
            settings.kbd_config = xkb_kbd_config()
            settings.kbd_config.model = self.config_rec.get_model()
            settings.kbd_config.layouts = ",".join(self.config_rec.get_layouts())
            settings.kbd_config.variants = ",".join(self.config_rec.get_variants())
            settings.kbd_config.options = ["grp:alt_shift_toggle"]
        else:
            activate_settings = True
            settings.kbd_config.model = self.config_rec.model
            settings.kbd_config.layouts = self.config_rec.layouts.split(",")
            settings.kbd_config.variants = self.config_rec.variants.split(",")
            settings.kbd_config.options = self.config_rec.options.split(",")
        
        for opt in settings.kbd_config.options:
            if opt.startswith("grp:"):
                settings.kbd_config.toggle_option = opt
                break
        
        if activate_settings and not settings.never_modify_config:
            self.config_rec.activate(self.engine)
        
        self.initialize_xkb_options(settings)
        #self.update_display
        
        return True
    
        
    def window_changed(self, new_window_id, application_id):
        if self.settings.group_policy == group_policy.GLOBAL:
            return None
        elif self.settings.group_policy == group_policy.PER_WINDOW:
            hashtable = self.window_map
            id = new_window_id
            self.current_window_id = id
        elif self.settings.group == group_policy.PER_APPLICATION:
            hashtable = self.application_map
            id = aplication_id
            self.current_application_id = id
            
        group = self.settings.default_group
        
        if hashtable.has_key(id):
            group = hashtable[id]
        
        hashtable[id] = group
        
        self.set_group(group)
    
    def application_closed(self, application_id):
        if self.settings.group_policy == group_policy.PER_APPLICATION:
            self.application_map.remove(application_id)
    
    def window_closed(self, window_id):
        if self.settings.group_policy == group_policy.PER_WINDOW:
            self.window_map.remove(window_id)
    
    def get_group_count(self):
        return self.group_count
    
    def get_group_map(self, group):
        if group > self.group_count:
            return False
        
        if group == -1:
            pass
            #group = xkb_config_get_current_group ()
        
        return self.group_names[group]
    
    def get_variant_map(self, group):
        if group > self.group_count:
            return False
        
        if group == -1:
            pass
            #group = xkb_config_get_current_group ()
        
        return self.variants[group]
    
    def state_changed(engine, change, group, restore):
        pass
    
    def config_changed(engine):
        self.kbd_config = None
        self.update_settings(self.settings)
        
        if self.callback:
            self.callback(self.get_current_group(), True, self.callback_data)
        
    def get_xkl_registry(self):
        registry = xklavier.ConfigRegistry(self.engine)
        registry.load(False)
        
        return registry
    
    def get_layout_desc(self, group, variant):
        reg = xklavier.ConfigRegistry(self.engine)
        item = xklavier.ConfigItem()
        
        item.name = group
        reg.find_layout(item)
        
        description = item.get_description()
        
        if variant:
            item.name = variant
            reg.find_variant(group, item)
            
            description = "%s(%s)" % (description, item.description)
        
        return description