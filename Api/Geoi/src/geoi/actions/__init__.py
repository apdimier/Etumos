__all__ = ['action', 'params_action', 'toggle_action',
            "new", "exit", "about", "help", "show_params",
            "switch_to_std_dialog",
           'title', 'units', 'physics_software', 'chemistry', 'open_chemistry_db'
           , 'open_file', 'save_file', "save_file_as", 'open_shell', "inspector",
           'aqueous_master_species', 'aqueous_secondary_species', "mineral_phase", "exchange_master_species",
           'surface_master_species','surface_species', 'exchange_species',\
           'aqueous_state',\
           'equilibrium_state',\
           'exchange_state',\
           'surface_state',\
           "materials", "materials_e", "mesh_constructor","set_zones",\
           "set_DarcyVelocity","launching","set_PostProcessing","set_PyPostProcessing",\
           "simulate_elmer",\
           "set_VtkPostProcessing",\
           "mt3d_solver_parameters","coupling_algorithm"]

#for m in __all__:
#    try:
#        exec 'from ' + m  + ' import '  + m[0].upper
#    except ImportError:
#        print "ImportError"
