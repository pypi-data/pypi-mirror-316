from .roundrobinlb import RoundRobinLoadBalancer
from .randomlb import RandomLoadBalancer
from .weightedroundrobinlb import WeightedRoundRobinLoadBalancer
from .leastconnectionlb import LeastConnectionLoadBalancer
from .leastconnectionpoweroftwolb import LeastConnectionPowerOfTwoLoadBalancer
from .leastlatencylb import LeastLatencyLoadBalancer
from .leastlatencypoweroftwolb import LeastLatencyPowerOfTwoLoadBalancer

class LoadBalancerFactory:
    """
    Factory class to create different types of load balancers based on the given configuration.
    """
    def CreateLoadBalancer(self, configuration):
        """
        Create a load balancer based on the provided configuration.
        
        Args:
            configuration (dict): A dictionary containing the configuration for the load balancer.
                The dictionary should have the following keys:
                - 'algorithm': The algorithm to use for the load balancer (e.g., 'random', 'roundrobin', etc.).
                - 'servers': A dictionary of servers with hostnames as keys and OriginServer instances as values.
        
        Returns:
            An instance of a load balancer based on the specified algorithm.
        
        Raises:
            ValueError: If the specified algorithm is unknown.
        """
        match configuration['algorithm']:
            case 'random':
                return RandomLoadBalancer(configuration['servers'])
            case 'roundrobin':
                return RoundRobinLoadBalancer(configuration['servers'])
            case 'weightedroundrobin':
                return WeightedRoundRobinLoadBalancer(configuration['servers'])
            case 'leastconnection':
                return LeastConnectionLoadBalancer(configuration['servers'])
            case 'leastconnectionpoweroftwo':
                return LeastConnectionPowerOfTwoLoadBalancer(configuration['servers'])
            case 'leastlatency':
                return LeastLatencyLoadBalancer(configuration['servers'])
            case 'leastlatencypoweroftwo':
                return LeastLatencyPowerOfTwoLoadBalancer(configuration['servers'])
            case _:
                raise ValueError(f"Unknown load balancer algorithm: {configuration['algorithm']}")