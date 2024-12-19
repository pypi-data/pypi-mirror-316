from typing import List, Dict, Optional, Any
import pandas as pd

from .base_graph import BaseGraph

from tigergraphx.config import (
    GraphSchema,
    TigerGraphConnectionConfig,
)


class Graph(BaseGraph):
    """
    Represents a graph structure supporting both homogeneous and heterogeneous graphs.

    This class handles:

    - Undirected Homogeneous Graphs
    - Directed Homogeneous Graphs
    - Heterogeneous Graphs with multiple node and edge types
    """

    def __init__(
        self,
        graph_schema: GraphSchema,
        tigergraph_connection_config: Optional[TigerGraphConnectionConfig] = None,
        drop_existing_graph: bool = False,
    ):
        """
        Initialize the Graph instance.

        Args:
            graph_schema (GraphSchema): The schema of the graph.
            tigergraph_connection_config (Optional[TigerGraphConnectionConfig], optional): 
                Configuration for TigerGraph connection. Defaults to None.
            drop_existing_graph (bool, optional): Whether to drop the existing graph if it exists. 
                Defaults to False.
        """
        super().__init__(
            graph_schema=graph_schema,
            tigergraph_connection_config=tigergraph_connection_config,
            drop_existing_graph=drop_existing_graph,
        )

    # ------------------------------ Node Operations ------------------------------
    def add_node(
        self, node_id: str, node_type: str = "", **attr: Dict[str, Any]
    ) -> None:
        """
        Add a node to the graph.

        Args:
            node_id (str): The identifier of the node.
            node_type (str, optional): The type of the node. Defaults to "".
            **attr (Dict[str, Any]): Additional attributes for the node.
        """
        node_type = self._validate_node_type(node_type)
        self._add_node(node_id, node_type, **attr)

    def remove_node(self, node_id: str, node_type: str = "") -> bool:
        """
        Remove a node from the graph.

        Args:
            node_id (str): The identifier of the node.
            node_type (str, optional): The type of the node. Defaults to "".

        Returns:
            bool: True if the node was removed, False otherwise.
        """
        node_type = self._validate_node_type(node_type)
        return self._remove_node(node_id, node_type)

    def has_node(self, node_id: str, node_type: str = "") -> bool:
        """
        Check if a node exists in the graph.

        Args:
            node_id (str): The identifier of the node.
            node_type (str, optional): The type of the node. Defaults to "".

        Returns:
            bool: True if the node exists, False otherwise.
        """
        node_type = self._validate_node_type(node_type)
        return self._has_node(node_id, node_type)

    def get_node_data(self, node_id: str, node_type: str = "") -> Dict | None:
        """
        Get data of a specific node.

        Args:
            node_id (str): The identifier of the node.
            node_type (str, optional): The type of the node. Defaults to "".

        Returns:
            Dict | None: The node data or None if not found.
        """
        node_type = self._validate_node_type(node_type)
        return self._get_node_data(node_id, node_type)

    def get_node_edges(
        self,
        node_id: str,
        node_type: str = "",
        edge_types: List | str = [],
        num_edge_samples: int = 1000,
    ) -> List:
        """
        Get edges connected to a specific node.

        Args:
            node_id (str): The identifier of the node.
            node_type (str, optional): The type of the node. Defaults to "".
            edge_types (List | str, optional): Types of edges to include. Defaults to [].
            num_edge_samples (int, optional): Number of edge samples to retrieve. Defaults to 1000.

        Returns:
            List: A list of edges.
        """
        node_type = self._validate_node_type(node_type)
        edges = self._get_node_edges(
            node_id,
            node_type,
            edge_types,
            num_edge_samples,
        )
        result = [(edge["from_id"], edge["to_id"]) for edge in edges]
        return result

    # ------------------------------ Edge Operations ------------------------------
    def add_edge(
        self,
        src_node_id: str,
        tgt_node_id: str,
        src_node_type: str = "",
        edge_type: str = "",
        tgt_node_type: str = "",
        **attr: Dict[str, Any],
    ) -> None:
        """
        Add an edge to the graph.

        Args:
            src_node_id (str): Source node identifier.
            tgt_node_id (str): Target node identifier.
            src_node_type (str, optional): Source node type. Defaults to "".
            edge_type (str, optional): Type of the edge. Defaults to "".
            tgt_node_type (str, optional): Target node type. Defaults to "".
            **attr (Dict[str, Any]): Additional attributes for the edge.
        """
        src_node_type, edge_type, tgt_node_type = self._validate_edge_type(
            src_node_type, edge_type, tgt_node_type
        )
        self._add_edge(
            src_node_id,
            tgt_node_id,
            src_node_type,
            edge_type,
            tgt_node_type,
            **attr,
        )

    def has_edge(
        self,
        src_node_id: str | int,
        tgt_node_id: str | int,
        src_node_type: str = "",
        edge_type: str = "",
        tgt_node_type: str = "",
    ) -> bool:
        """
        Check if an edge exists in the graph.

        Args:
            src_node_id (str | int): Source node identifier.
            tgt_node_id (str | int): Target node identifier.
            src_node_type (str, optional): Source node type. Defaults to "".
            edge_type (str, optional): Type of the edge. Defaults to "".
            tgt_node_type (str, optional): Target node type. Defaults to "".

        Returns:
            bool: True if the edge exists, False otherwise.
        """
        src_node_type, edge_type, tgt_node_type = self._validate_edge_type(
            src_node_type, edge_type, tgt_node_type
        )
        return self._has_edge(
            src_node_id,
            tgt_node_id,
            src_node_type,
            edge_type,
            tgt_node_type,
        )

    def get_edge_data(
        self,
        src_node_id: str,
        tgt_node_id: str,
        src_node_type: str = "",
        edge_type: str = "",
        tgt_node_type: str = "",
    ) -> Dict | None:
        """
        Get data of a specific edge.

        Args:
            src_node_id (str): Source node identifier.
            tgt_node_id (str): Target node identifier.
            src_node_type (str, optional): Source node type. Defaults to "".
            edge_type (str, optional): Type of the edge. Defaults to "".
            tgt_node_type (str, optional): Target node type. Defaults to "".

        Returns:
            Dict | None: The edge data or None if not found.
        """
        src_node_type, edge_type, tgt_node_type = self._validate_edge_type(
            src_node_type, edge_type, tgt_node_type
        )
        return self._get_edge_data(
            src_node_id,
            tgt_node_id,
            src_node_type,
            edge_type,
            tgt_node_type,
        )

    # ------------------------------ Statistics Operations ------------------------------
    def degree(self, node_id: str, node_type: str = "", edge_types: List = []) -> int:
        """
        Get the degree of a node.

        Args:
            node_id (str): The identifier of the node.
            node_type (str, optional): The type of the node. Defaults to "".
            edge_types (List, optional): Types of edges to consider. Defaults to [].

        Returns:
            int: The degree of the node.
        """
        node_type = self._validate_node_type(node_type)
        return self._degree(node_id, node_type, edge_types)

    def number_of_nodes(self, node_type: Optional[str] = None) -> int:
        """
        Get the number of nodes in the graph.

        Args:
            node_type (Optional[str], optional): The type of nodes to count. Defaults to None.

        Returns:
            int: The number of nodes.
        """
        if node_type:
            node_type = self._validate_node_type(node_type)
        return self._number_of_nodes(node_type)

    def number_of_edges(self, edge_type: Optional[str] = None) -> int:
        """
        Get the number of edges in the graph.

        Args:
            edge_type (Optional[str], optional): The type of edges to count. Defaults to None.

        Returns:
            int: The number of edges.
        """
        return self._number_of_edges(edge_type)

    # ------------------------------ Query Operations ------------------------------
    def get_nodes(
        self,
        node_type: str = "",
        filter_expression: Optional[str] = None,
        return_attributes: Optional[str | List[str]] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve nodes from the graph.

        Args:
            node_type (str, optional): The type of nodes to retrieve. Defaults to "".
            filter_expression (Optional[str], optional): Filter expression. Defaults to None.
            return_attributes (Optional[str | List[str]], optional): Attributes to return. Defaults to None.
            limit (Optional[int], optional): Limit the number of results. Defaults to None.

        Returns:
            pd.DataFrame | None: DataFrame of nodes or None.
        """
        node_type = self._validate_node_type(node_type)
        return self._get_nodes(
            node_type=node_type,
            filter_expression=filter_expression,
            return_attributes=return_attributes,
            limit=limit,
        )

    def get_neighbors(
        self,
        start_nodes: str | List[str],
        start_node_type: str = "",
        edge_types: Optional[str | List[str]] = None,
        target_node_types: Optional[str | List[str]] = None,
        filter_expression: Optional[str] = None,
        return_attributes: Optional[str | List[str]] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame | None:
        """
        Get neighbors of specified nodes.

        Args:
            start_nodes (str | List[str]): Starting node(s).
            start_node_type (str, optional): Type of starting nodes. Defaults to "".
            edge_types (Optional[str | List[str]], optional): Types of edges to consider. Defaults to None.
            target_node_types (Optional[str | List[str]], optional): Types of target nodes. Defaults to None.
            filter_expression (Optional[str], optional): Filter expression. Defaults to None.
            return_attributes (Optional[str | List[str]], optional): Attributes to return. Defaults to None.
            limit (Optional[int], optional): Maximum number of neighbors to retrieve. Defaults to None.

        Returns:
            pd.DataFrame | None: DataFrame of neighbors or None.
        """
        start_node_type = self._validate_node_type(start_node_type)
        return self._get_neighbors(
            start_nodes=start_nodes,
            start_node_type=start_node_type,
            edge_types=edge_types,
            target_node_types=target_node_types,
            filter_expression=filter_expression,
            return_attributes=return_attributes,
            limit=limit,
        )

    # ------------------------------ Utilities ------------------------------
    def _validate_node_type(self, node_type: Optional[str]) -> str:
        """
        Validate and determine the effective node type.

        Args:
            node_type (Optional[str]): The node type to validate.

        Returns:
            str: The validated node type.

        Raises:
            ValueError: If the node type is invalid or not specified correctly.
        """
        if node_type:
            if node_type not in self.node_types:
                raise ValueError(
                    f"Invalid node type '{node_type}'. Must be one of {self.node_types}."
                )
            return node_type
        if len(self.node_types) == 0:
            raise ValueError("The graph has no node types defined.")
        if len(self.node_types) > 1:
            raise ValueError(
                "Multiple node types detected. Please specify a node type."
            )
        return next(iter(self.node_types))

    def _validate_edge_type(
        self,
        src_node_type: Optional[str],
        edge_type: Optional[str],
        tgt_node_type: Optional[str],
    ) -> tuple[str, str, str]:
        """
        Validate node types and edge type, and determine effective types.

        Args:
            src_node_type (Optional[str]): Source node type.
            edge_type (Optional[str]): Edge type.
            tgt_node_type (Optional[str]): Target node type.

        Returns:
            tuple[str, str, str]: Validated source node type, edge type, and target node type.

        Raises:
            ValueError: If the edge type is invalid or not specified correctly.
        """
        src_node_type = self._validate_node_type(src_node_type)
        tgt_node_type = self._validate_node_type(tgt_node_type)

        if edge_type:
            if edge_type not in self.edge_types:
                raise ValueError(
                    f"Invalid edge type '{edge_type}'. Must be one of {self.edge_types}."
                )
        else:
            if len(self.edge_types) == 0:
                raise ValueError("The graph has no edge types defined.")
            if len(self.edge_types) > 1:
                raise ValueError(
                    "Multiple edge types detected. Please specify an edge type."
                )
            edge_type = next(iter(self.edge_types))

        return src_node_type, edge_type, tgt_node_type
