from .roundrobinlb import RoundRobinLoadBalancer
from .originserver import OriginServer

class WeightedRoundRobinLoadBalancer(RoundRobinLoadBalancer):
    """
    A load balancer that selects the origin server in a weighted round-robin fashion.
    Servers with higher weights will be selected more frequently.
    """
    def __init__(self, servers: dict[str, OriginServer] = None):
        """
        Initialize the weighted round-robin load balancer with the given servers.

        Args:
            servers (dict[str, OriginServer]): A dictionary of servers with hostnames as keys and OriginServer instances as values.
        """
        super().__init__(servers)
        self.current_repeat_count = 0
        
    async def get_next_server(self):
        """
        Get the next server in a weighted round-robin fashion.
        
        Returns:
            OriginServer: The next server to handle the request.
        """
        host = self.hosts[self.current_index]
        async with self.lock:
            self.current_repeat_count += 1
            if self.current_repeat_count >= self.servers[host].weight:
                self.current_index = (self.current_index + 1) % len(self.hosts)
                self.current_repeat_count = 0
        return self.servers[host]