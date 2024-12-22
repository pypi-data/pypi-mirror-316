from abc import ABC, abstractclassmethod, abstractmethod
import threading


class AbstractInteractiveGUI(ABC):
    """
        Base class visualizer for building blocks

        Attributes
        ----------
        port: int
            port of the GUI server
        endpoint: str
            endpoint of the GUI server (the same as the host of the backend)
        settings_GUI: dict
            settings dictionary used to configure building block
        inputs_name: list
            list containing the names of inputs that required by the GUI
        event_lock: object
            event lock object used to block the process to wait for the user inputs
        building_block: object
            the associated building block object
        app: server object
            GUI server object
        """
    def __init__(self, endpoint, port, building_block):
        self.port = port
        self.endpoint = endpoint

        self.settings_GUI = None

        self.inputs_name = []  # gui input name list, empty, if no input is required
        self.inputs = {}  # gui input dict
        self.settings = {}

        self.event_lock = threading.Event()
        self.building_block = building_block

        self.app = None

    @abstractmethod
    def run_interactive_gui(self, **kwargs):
        pass

    def _show_layout(self):
        """
        start GUI and wait for the user inputs

        """
        #self.app = self.settings_GUI.show(open=True, threaded=True, address=self.endpoint, port=self.port,
        #                 websocket_origin=[f'{self.endpoint}:{self.port}', f'{self.port}.0.0.0.0'])
                         
        self.app = self.settings_GUI.show(open=False, threaded=True, address=self.endpoint, port=self.port,
                         websocket_origin=[f'{self.endpoint}:{self.port}', f'{self.port}.localhost'])
        if self.event_lock.is_set():
            self.event_lock.clear()
        self.event_lock.wait()

    def terminate(self):
        """
        terminate a running bokeh server
        """
        if self.app:
            #self.event_lock.set()
            self.app.stop()
