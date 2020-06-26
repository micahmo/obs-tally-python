import obspython as obs
import serial                  # pip install pyserial
import serial.tools.list_ports # pip install pyserial

# Properties
scenes = ""
comport = ""
onvalue = ""
offvalue = ""
debug = False

# Underlying objects
comport_device = None
ser = None

# Property names
scenes_property = "scenes"
comport_property = "comport"
on_value_property = "onvalue"
off_value_property = "offvalue"
debug_value_property = "debug-obs-tally"

def script_description():
	return "Allows writing a value to a COM port when a scene(s) is made active. " \
"Especially useful for activating a tally light on an Arduino.\r\n\r\n"

def script_properties():
    props = obs.obs_properties_create()

    # There seems to be an issue with the SWIG interop that prevents us from
    # enumerating over the scenes. As a result, the user will have to type in the scene name.
    # However, for multiple scene selection, that is probably the only possible way.
    obs.obs_properties_add_text(props, scenes_property, "Scene(s)", obs.OBS_TEXT_MULTILINE)
    
    comports_list = obs.obs_properties_add_list(props, comport_property, "COM Port", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    [obs.obs_property_list_add_string(comports_list, str(comport), comport.device) for comport in discover_comports()]

    obs.obs_properties_add_text(props, on_value_property, "Value when live", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, off_value_property, "Value when not live", obs.OBS_TEXT_DEFAULT)

    obs.obs_properties_add_bool(props, debug_value_property, "Debug")
    
    obs.obs_frontend_add_event_callback(frontend_event_callback)

    return props

def frontend_event_callback(event):
    if (event == obs.OBS_FRONTEND_EVENT_EXIT and ser is not None):
        obs.timer_remove(update)
        debug_write(f"Shutting down. Writing off value ({offvalue}) to COM port.")
        write_value(offvalue)
        ser.close()

def discover_comports():
    return serial.tools.list_ports.comports()

def write_value(value):
    global ser

    try:
        ser.write(str.encode(f"{value}\n"))
    except:
        # Try to close and re-open
        if (ser is not None):
            ser.close()
        
        try:
            if (comport_device is not None):
                ser = serial.Serial(comport_device.device)
                ser.write(str.encode(f"{value}\n"))
        except Exception as e:
            debug_write(f"Error writing to COM port. {e}")


def script_update(settings):
    global scenes
    global comport_device
    global onvalue
    global offvalue
    global ser
    global debug

    obs.timer_remove(update)

    scenes = obs.obs_data_get_string(settings, scenes_property).split("\n")
    comport = obs.obs_data_get_string(settings, comport_property)
    onvalue = obs.obs_data_get_string(settings, on_value_property)
    offvalue = obs.obs_data_get_string(settings, off_value_property)
    debug = obs.obs_data_get_bool(settings, debug_value_property)

    # Try to retrieve the real scene objects. Not to save, but just to log
    scene_names = [obs.obs_source_get_name(scene_obj) for scene_obj in [obs.obs_get_source_by_name(scene) for scene in scenes]]

    # Close a previous connection with the com port
    if (ser is not None):
        ser.close()
    
    # Try to retrieve the real COM port object
    try:
        comport_device = [match for match in discover_comports() if match.device == comport][0]
    except:
        debug_write("Error retrieving COM port '{comport}'. Does it still exist?")

    # Try to open a new connection with the com port
    if (comport_device is not None):
        try:
            ser = serial.Serial(comport_device.device)
        except Exception as e:
            debug_write(f"Error opening COM port. {e}")

    debug_write(f"Got COM port '{comport_device}', On Value '{onvalue}', Off Value '{offvalue}, Scene(s) '{', '.join(filter(None, scene_names))}', '")

    obs.timer_add(update, 100)

def update():
    current_scene = obs.obs_frontend_get_current_scene()
    current_scene_name = obs.obs_source_get_name(current_scene)

    if current_scene_name in scenes:
        debug_write(f"Currently on target scene. Writing on value ({onvalue}) to COM port.")
        write_value(onvalue)
    else:
        debug_write(f"Currently on non-target scene. Writing off value ({offvalue}) to COM port.")
        write_value(offvalue)

def debug_write(message):
    if (debug):
        print(message)