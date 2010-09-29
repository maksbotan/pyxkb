#!/usr/bin/env python

import gtk

class xkb_config:
	def __init__(self, callback, callback_data):
		self.callback = callback
		self.callback_data = callback_data
		
		
		#config->engine = xkl_engine_get_instance (GDK_DISPLAY ());
		self.engine = None
		
		if not self.engine:
			return False
		
		#    xkb_config_update_settings (settings);
		
		#xkl_engine_set_group_per_toplevel_window (config->engine, FALSE);
		
		cur = self.get_current_group()
		
		#    xkl_engine_start_listen (config->engine, XKLL_TRACK_KEYBOARD_STATE);
		
		self.engine.connect("X-state-changed", self.state_changed, None)
		self.engine.connect("X-config-changed", self.config_changed, None)
		
		#gdk_window_add_filter (NULL, (GdkFilterFunc) handle_xevent, NULL);
		
		return True
		
	def initialixe_xkb_options(self):
		#    XklState *state = xkl_engine_get_current_state (config->engine);
		self.group_count = len(self.config_rec.layouts)
		
		self.window_map = {}
		self.application_map = {}
		
		#~ registry = xkl_config_registry_get_instance (config->engine);
		#~ xkl_config_registry_load (registry);
		#~ config_item = xkl_config_item_new ();
		
		self.group_names = []
		self.variants = []
		self.variant_index_by_group = {}
		index_variants = {}
		
		for i in xrange(self.group_count):
			config_item.name = self.config_rec.layouts[i]
			self.group_names.append(self.config_rec.layouts[i])
			
			if self.config_rec.variants[i]:
				config_item.name = self.config_rec.variants[i]
			
			self.variants.append("" if not self.config_rec.variants[i] else self.config_rec.variants[i])
			val = index_variants.get(self.group_names[i])
			
			self.variant_index_by_group[self.group_names[i]] = val
			index_variants[self.group_names[i]] = val
		
	def get_current_group(self):
		#XklState* state = xkl_engine_get_current_state (config->engine);
		return state.group
		
	def set_group(self, grooup):
		pass
			
