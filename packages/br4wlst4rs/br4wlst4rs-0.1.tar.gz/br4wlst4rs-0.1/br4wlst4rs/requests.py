import frida
import sys
import threading
import time
from pynput import keyboard
from br4wlst4rs.core import *

def rec_post(session, base_address, config, callback=None):
    rec_post_offset = config["offsets"].get("rec_post")
    script_code = load_js(
        "rec_post.js",
        base_address=base_address,
        rec_post=rec_post_offset
    )

    stop_event = threading.Event()

    def on_message(message, data):
        if message['type'] == 'send':
            if callback:
                callback(message['payload'])
        elif message['type'] == 'error':
            print("[!] Error:", message['stack'])
            print("\n\n")

    script = session.create_script(script_code)
    script.on('message', on_message)
    script.load()

    def on_press(key):
        try:
            if key == keyboard.Key.space:
                stop_event.set()
                return False
        except AttributeError:
            pass

    def listen_for_exit():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    listener_thread = threading.Thread(target=listen_for_exit)
    listener_thread.start()

    try:
        stop_event.wait()
    except KeyboardInterrupt:
        stop_event.set()

    script.unload()
    listener_thread.join()