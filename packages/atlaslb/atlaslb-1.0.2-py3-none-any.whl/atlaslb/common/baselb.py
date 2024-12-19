import asyncio
from .originserver import OriginServer
from django.http import HttpResponse
import aiohttp
import time

class BaseLoadBalancer:
    """
    The base class for the load balancer. 
    Maintains a list of the origin servers and a mapping of the hostnames to the server objects.
    """
    def __init__(self, servers: dict[str, OriginServer] = None):
        """
        Initialize the load balancer object with the given servers.

        Args:
            servers (dict[str, OriginServer]): A dictionary of servers with hostnames as keys and OriginServer instances as values.
        """
        self.servers = servers if servers is not None else {}
        self.hosts = list(self.servers.keys())
        self.lock = asyncio.Lock()

    async def add_server(self, server: OriginServer):
        """
        Add a server to the load balancer.

        Args:
            server (OriginServer): The server to add.
        """
        async with self.lock:
            if server.host not in self.servers:
                self.hosts.append(server.host)
            self.servers[server.host] = server

    async def forward_request(self, request, path: str):
        """
        Forward the request to the appropriate origin server based on the load balancing algorithm.
        The algorithm is implemented in the derived classes. This method also maintains the requests-in-flight count and the exponential moving average of latency for each server.

        Args:
            request (HttpRequest): The incoming HTTP request.
            path (str): The path to forward the request to.

        Returns:
            HttpResponse: The response from the origin server.
        """
        if not self.servers or len(self.servers) == 0:
            return HttpResponse("Service unavailable, please try again after some time.", status=503)
        
        origin = await self.get_next_server()
        url = f"http://{origin.host}/{path}"

        async with origin.lock:
            origin.local_rif += 1
         
        request_start_time = time.time()
        async with aiohttp.ClientSession() as session: 
            async with session.get(url) as response:
                response = await response.text()
        request_end_time = time.time()
        elapsed_time = request_end_time - request_start_time

        async with origin.lock:
            origin.local_rif -= 1
            origin.latency = (elapsed_time + origin.latency)/2

        proxyResponse = HttpResponse(response)
        proxyResponse["X-Atlas-Origin-Server"] = origin.host
        return proxyResponse
        
    def __str__(self):
        """
        Return a string representation of the load balancer.

        Returns:
            str: A string representation of the load balancer.
        """
        return ", ".join([str(server) for server in self.servers.values()])