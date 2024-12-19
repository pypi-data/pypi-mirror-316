from .originserver import OriginServer
from .roundrobinlb import RoundRobinLoadBalancer

class LeastLatencyLoadBalancer(RoundRobinLoadBalancer):
    """
    A load balancer that selects the origin server with the least latency.
    """
    def __init__(self, servers: dict[str, OriginServer] = None):
        """
        Initialize the least latency load balancer with the given servers.
        
        Args:
            servers (dict[str, OriginServer]): A dictionary of servers with hostnames as keys and OriginServer instances as values.
        """
        super().__init__(servers)
        
    async def get_next_server(self):
        """
        Get the next server with the least latency.
        
        Returns:
            OriginServer: The next server to handle the request.
        """
        print([server.latency for server in self.servers.values()])
        min_latency = float('inf')
        candiate_hosts = []
        host_indices = []
        async with self.lock:
            for index, host in enumerate(self.hosts):
                if self.servers[host].latency < min_latency:
                    min_latency = self.servers[host].latency
                    candiate_hosts = [host]
                    host_indices = [index]
                elif self.servers[host].latency == min_latency:
                    candiate_hosts.append(host)
                    host_indices.append(index)
        print(candiate_hosts, host_indices)
        if len(candiate_hosts) == 1:
            self.current_index = host_indices[0]
            return self.servers[candiate_hosts[0]]
        else:
            distance = float('inf')
            selected_index = None
            async with self.lock:
                for index, host in zip(host_indices, candiate_hosts):
                    curr_dist = (index - self.current_index) % len(self.hosts)
                    print(index, self.current_index, curr_dist, distance)
                    if curr_dist < distance and index != self.current_index:
                        distance = curr_dist
                        selected_index = index
            self.current_index = selected_index
            print(self.current_index)
            return self.servers[self.hosts[self.current_index]]