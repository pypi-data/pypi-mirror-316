from ..common.originserver import OriginServer
from .roundrobinlb import RoundRobinLoadBalancer

class LeastConnectionLoadBalancer(RoundRobinLoadBalancer):
    """
    A load balancer that selects the origin server with the least number of active connections.
    """
    def __init__(self, servers: dict[str, OriginServer] = None):
        """
        Initialize the least connection load balancer with the given servers.
        
        Args:
            servers (dict[str, OriginServer]): A dictionary of servers with hostnames as keys and OriginServer instances as values.
        """
        super().__init__(servers)
        
    async def get_next_server(self):
        """
        Get the next server with the least number of active connections.
        
        Returns:
            OriginServer: The next server to handle the request.
        """
        min_connections = float('inf')
        candiate_hosts = []
        host_indices = []
        async with self.lock:
            for index, host in enumerate(self.hosts):
                if self.servers[host].local_rif < min_connections:
                    min_connections = self.servers[host].local_rif
                    candiate_hosts = [host]
                    host_indices = [index]
                elif self.servers[host].local_rif == min_connections:
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