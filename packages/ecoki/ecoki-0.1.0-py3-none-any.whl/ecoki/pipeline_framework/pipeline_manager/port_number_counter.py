class PortNumberCounter:
    """
        class bokeh server port generator

        Attributes
        ----------
        begin_port: int
            starting port of the available bokeh server port range: 27500
        end_port: int
            end port of the available bokeh server port range: 27969
        generated_ports: list
            list of used ports by bokeh server
    """
    def __init__(self, begin_port=27500, end_port=27969):
        self.begin_port = begin_port
        self.end_port = end_port
        self.generated_ports = []
        
    def generate_port(self):
        """
        generate a port for bokeh server
        """
        for port in range(self.begin_port, self.end_port, 1):
            if not self.port_busy(port):
                self.generated_ports.append(port)
                return port
        return None
    
    def free_port(self, port):
        """
        free an occupied bokeh server port
        :param port: bokeh server port
        """
        if self.port_busy(port):
            self.generated_ports.remove(port)
        
    def port_busy(self, port):
        """
        check whether the given port is occupied
        :param port: bokeh server port
        :return: if the given port is occupied: True, otherwise: False
        """
        return port in self.generated_ports
