import frida
import time
import sys

#Usage ./frida-skeleton.py <script.js> <packagename>

jsscript = sys.argv[1] #js to inject
package_name = sys.argv[2] #package name to spawn

device = frida.get_usb_device()
pid = device.spawn([package_name])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
script = session.create_script(open(jsscript).read())
script.load()

raw_input()
