import lib.launchcraft.assets as assets
import lib.launchcraft.command as command
import lib.launchcraft.java as java
import lib.launchcraft.libraries as libraries
import lib.launchcraft.version as version

DIRECTORY = "/Users/3124224/Library/Application Support/devnolauncher"
VERSION = "1.20.4"
PROXY = "192.168.86.68:1060"

version.run(DIRECTORY, VERSION, PROXY)
libraries.run(DIRECTORY, VERSION, PROXY)
assets.run(DIRECTORY, VERSION, PROXY)
java.run(DIRECTORY, VERSION, PROXY)
command.run(DIRECTORY, VERSION, PROXY)