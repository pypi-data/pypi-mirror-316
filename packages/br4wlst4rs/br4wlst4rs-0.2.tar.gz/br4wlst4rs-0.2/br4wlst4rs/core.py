import json
import os
import sys
import threading
import requests
import importlib.resources as resources
import frida

def need_update(config):
    package_name = "br4wlst4rs"
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    latest_version = response.json()['info']['version']
    
    current_version = config["lib"].get("version")
    
    if float(current_version) != float(latest_version):
        return True
    else:
        return False

def load_config():
    with resources.open_text('br4wlst4rs.config', 'config.json') as file:
        config = json.load(file)
    
    return config

def load_js(filename, **kwargs):
    with resources.open_text('br4wlst4rs.js', filename) as file:
        script_code = file.read()

    for key, value in kwargs.items():
        placeholder = f"{{{key}}}"
        script_code = script_code.replace(placeholder, value)

    return script_code

def get_base_address(session, main_module):
    script_code = load_js("base_address.js", main_module=main_module)

    result = {"base_address": None}
    event = threading.Event()

    def on_message(message, data):
        if message['type'] == 'send':
            result["base_address"] = message['payload']
            event.set()

    script = session.create_script(script_code)
    script.on('message', on_message)
    script.load()

    event.wait()
    return result["base_address"]

def start():
    config = load_config()

    if need_update(config):
        print(f"New version available")
        print(f"Update using: pip install --upgrade br4wlst4rs")
        sys.exit()

    mode = config["frida-config"].get("mode")
    app = config["application"].get("app_name")
    main_module = config["application"].get("main_module")

    if mode == "remote":
        ip = config["frida-config"].get("ip")
        port = config["frida-config"].get("port")
        remote_ip = f"{ip}:{port}"
        device = frida.get_device_manager().add_remote_device(remote_ip)

    elif mode == "usb":
        device = frida.get_usb_device()

    pid = device.spawn([app])
    session = device.attach(pid)

    device.resume(pid)

    return session, config, main_module