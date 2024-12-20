import os
import sys
import threading

import numpy as np  # not needed but always nice to have

from bec_ipython_client.main import BECIPythonClient as _BECIPythonClient
from bec_ipython_client.main import main_dict as _main_dict
from bec_lib import plugin_helper
from bec_lib.logger import bec_logger as _bec_logger
from bec_lib.redis_connector import RedisConnector as _RedisConnector
from bec_lib.utils.proxy import Proxy

try:
    from bec_widgets.cli.client import BECDockArea as _BECDockArea
except ImportError:
    _BECDockArea = None

logger = _bec_logger.logger

bec = _BECIPythonClient(
    _main_dict["config"], _RedisConnector, wait_for_server=_main_dict["wait_for_server"]
)
_main_dict["bec"] = bec


class GuiProxy(Proxy):
    def close(self):
        gui = self.__factory__(ignore_event=True)
        gui.close()


if _BECDockArea is not None:

    class BECDockArea(_BECDockArea):
        def show(self):
            if self._process is not None:
                return self.show_all()
            else:
                # backward compatibility: show() was also starting server
                return self.start_server(wait=True)

        def hide(self):
            return self.hide_all()

        def start(self):
            return self.start_server()

else:
    BECDockArea = None

try:
    bec.start()
except Exception:
    sys.excepthook(*sys.exc_info())
else:
    if bec.started and not _main_dict["args"].nogui and BECDockArea is not None:
        _gui = BECDockArea()
        _gui.start()

        class get_gui:
            def __init__(self, gui, gui_started_event):
                self.gui = gui
                self.event = gui_started_event

            def __call__(self, ignore_event=False):
                if ignore_event:
                    return self.gui
                if self.gui is None:
                    return None
                self.event.wait(timeout=5)
                if not self.event.is_set():
                    self.gui = None
                return self.gui

        gui = bec.gui = GuiProxy(get_gui(_gui, _gui._gui_started_event))

        del _gui

    _available_plugins = plugin_helper.get_ipython_client_startup_plugins(state="post")
    if _available_plugins:
        for name, plugin in _available_plugins.items():
            logger.success(f"Loading plugin: {plugin['source']}")
            base = os.path.dirname(plugin["module"].__file__)
            with open(os.path.join(base, "post_startup.py"), "r", encoding="utf-8") as file:
                # pylint: disable=exec-used
                exec(file.read())

    else:
        bec._ip.prompts.status = 1

    if not bec._hli_funcs:
        bec.load_high_level_interface("bec_hli")

if _main_dict["startup_file"]:
    with open(_main_dict["startup_file"], "r", encoding="utf-8") as file:
        # pylint: disable=exec-used
        exec(file.read())
