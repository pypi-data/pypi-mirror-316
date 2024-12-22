from collections import deque

import networkx as nx
import numpy as np
from jax.experimental.sparse import BCOO
from random_events.variable import Continuous
from sortedcontainers import SortedSet
from typing_extensions import List, Self, Type

from ...distributions import GaussianDistribution
from ...probabilistic_circuit.jax import SumLayer, ProductLayer
from ...probabilistic_circuit.jax.gaussian_layer import GaussianLayer
from ...probabilistic_circuit.nx.probabilistic_circuit import ProbabilisticCircuit, SumUnit, ProductUnit
from ...probabilistic_circuit.nx.distributions.distributions import UnivariateContinuousLeaf
from ...probabilistic_circuit.jax.probabilistic_circuit import ProbabilisticCircuit as JPC
import jax.numpy as jnp
import jax.random


class Region:
    variables: SortedSet

    def __init__(self, variables: SortedSet):
        self.variables = variables

    def __hash__(self) -> int:
        return id(self)

    def random_partition(self, k=2) -> List[Self]:
        indices = np.arange(len(self.variables))
        np.random.shuffle(indices)
        partitions = [Region(SortedSet([self.variables[index] for index in split])) for split in np.array_split(indices, k)]
        return partitions

    def __repr__(self) -> str:
        return "{" + ", ".join([v.name for v in self.variables]) + "}"

class Partition:
    def __hash__(self) -> int:
        return id(self)


class RegionGraph(nx.DiGraph):

    variables: SortedSet

    def __init__(self, variables: SortedSet,
                 partitions: int = 2,
                 depth:int = 2,
                 repetitions:int = 2):
        super().__init__()
        self.variables = variables
        self.partitions = partitions
        self.depth = depth
        self.repetitions = repetitions


    def create_random_region_graph(self):
        root = Region(self.variables)
        self.add_node(root)
        for repetition in range(self.repetitions):
            self.recursive_split(root)
        return self

    def regions(self):
        for node in self.nodes:
            if isinstance(node, Region):
                yield node

    def partition_nodes(self):
        for node in self.nodes:
            if isinstance(node, Partition):
                yield node

    def recursive_split(self, node: Region):
        root_partition = Partition()
        self.add_edge(node, root_partition)
        remaining_regions = deque([(node, self.depth, root_partition)])

        while remaining_regions:
            region, depth, partition = remaining_regions.popleft()


            if len(region.variables) == 1:
                continue

            if depth == 0:
                for variable in region.variables:
                    self.add_edge(partition, Region(SortedSet([variable])))
                continue

            new_regions = region.random_partition(self.partitions)
            for new_region in new_regions:
                self.add_edge(partition, new_region)
                new_partition = Partition()
                self.add_edge(new_region, new_partition)
                remaining_regions.append((new_region, depth - 1, new_partition))

    @property
    def root(self) -> Region:
        """
        The root of the circuit is the node with in-degree 0.
        This is the output node, that will perform the final computation.

        :return: The root of the circuit.
        """
        possible_roots = [node for node in self.nodes() if self.in_degree(node) == 0]
        if len(possible_roots) > 1:
            raise ValueError(f"More than one root found. Possible roots are {possible_roots}")

        return possible_roots[0]


    def as_probabilistic_circuit(self, continuous_distribution_type: Type = GaussianLayer,
                                 input_units: int = 5, sum_units: int = 5, key=jax.random.PRNGKey(69)) -> JPC:
        root = self.root

        # create nodes for each region
        for layer in reversed(list(nx.bfs_layers(self, root))):
            for node in layer:
                children = list(self.successors(node))
                parents = list(self.predecessors(node))
                if isinstance(node, Region):
                    # if the region is a leaf
                    if len(children) == 0:
                        variable = node.variables[0]
                        variable_index = self.variables.index(variable)
                        if isinstance(variable, Continuous):
                            location = jax.random.uniform(key, shape=(input_units,), minval=-1., maxval=1.)
                            log_scale = jnp.log(jax.random.uniform(key, shape=(input_units,), minval=0.01, maxval=1.))
                            node.layer = GaussianLayer(variable_index, location=location, log_scale=log_scale, min_scale=jnp.full_like(location, 0.01))
                            node.layer.validate()
                        else:
                            raise NotImplementedError

                    # if the region is root or in the middle
                    else:
                        # if the region is root
                        if len(parents) == 0:
                            sum_units = 1

                        log_weights = [BCOO.fromdense(jax.random.uniform(key, shape=(sum_units, child.layer.number_of_nodes), minval=0., maxval=1.)) for child in children]
                        for log_weight in log_weights:
                            log_weight.data = jnp.log(log_weight.data)
                        node.layer = SumLayer([child.layer for child in children], log_weights=log_weights)
                        node.layer.validate()


                elif isinstance(node, Partition):
                    node_lengths = [child.layer.number_of_nodes for child in children]
                    assert (len(set(node_lengths)) == 1), "Node lengths must be all equal. Got {}".format(node_lengths)

                    edges = jnp.arange(node_lengths[0]).reshape(1, -1).repeat(len(children), axis=0)
                    sparse_edges = BCOO.fromdense(jnp.ones_like(edges))
                    sparse_edges.data = edges.flatten()
                    node.layer = ProductLayer([child.layer for child in children], sparse_edges)
                    node.layer.validate()

        model = JPC(self.variables, root.layer)
        return model
