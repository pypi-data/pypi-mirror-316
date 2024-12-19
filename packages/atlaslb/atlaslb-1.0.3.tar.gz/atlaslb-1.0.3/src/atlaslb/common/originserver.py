import asyncio

class OriginServer:
    """
    Represents an origin server with various attributes such as host, weight, CPU usage, 
    local requests in flight (local_rif), and latency.
    """
    def __init__(self, host, weight=1, cpu=0, local_rif=0, latency=0):
        """
        Initialize the origin server with the given attributes.
        
        Args:
            host (str): The hostname or IP address of the server.
            weight (int, optional): The weight of the server for weighted load balancing. Defaults to 1.
            cpu (int, optional): The CPU usage of the server. Defaults to 0.
            local_rif (int, optional): The number of local requests in flight. Defaults to 0.
            latency (float, optional): The latency of the server. Defaults to 0.
        """
        self.host = host
        self.weight = weight
        self.local_rif = local_rif
        self.cpu = cpu
        self.latency = latency
        self.lock = asyncio.Lock()

    def __str__(self):
        """
        Return a string representation of the origin server.
        
        Returns:
            str: A string representation of the origin server.
        """
        return f"{self.host} ({self.weight}, {self.local_rif})"