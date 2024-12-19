from .originserver import OriginServer
from .baselb import BaseLoadBalancer
import random

class LeastConnectionPowerOfTwoLoadBalancer(BaseLoadBalancer):
    """
    A load balancer that selects the origin server with the least number of active connections
    using the power of two choices algorithm.
    """
    def __init__(self, servers: dict[str, OriginServer] = None):
        """
        Initialize the least connection power of two load balancer with the given servers.
        
        Args:
            servers (dict[str, OriginServer]): A dictionary of servers with hostnames as keys and OriginServer instances as values.
        """
        super().__init__(servers)
        
    async def get_next_server(self):
        """
        Get the next server with the least number of active connections using the power of two choices algorithm.
        
        Returns:
            OriginServer: The next server to handle the request.
        """
        if len(self.hosts) == 1:
            return self.servers[self.hosts[0]]
        else:
            candidates = random.sample(self.hosts, 2)
            if self.servers[candidates[0]].local_rif < self.servers[candidates[1]].local_rif:
                return self.servers[candidates[0]]
            else:
                return self.servers[candidates[1]]