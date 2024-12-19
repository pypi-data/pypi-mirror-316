from ..common.baselb import BaseLoadBalancer
from ..common.originserver import OriginServer

class RoundRobinLoadBalancer(BaseLoadBalancer):
    """
    A load balancer that selects the origin server in a round-robin fashion.
    """
    def __init__(self, servers: dict[str, OriginServer] = None):
        """
        Initialize the round-robin load balancer with the given servers.
        
        Args:
            servers (dict[str, OriginServer]): A dictionary of servers with hostnames as keys and OriginServer instances as values.
        """
        super().__init__(servers)
        self.current_index = 0
        
    async def get_next_server(self):
        """
        Get the next origin server based on the round-robin selection algorithm.
        
        Returns:
            OriginServer: The next server to handle the request.
        """
        host = self.hosts[self.current_index]
        async with self.lock:
            self.current_index = (self.current_index + 1) % len(self.hosts)
        return self.servers[host]