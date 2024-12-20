from decouple import config
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy
from langgraph.graph.state import Runnable
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field, field_validator
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from typing import (
    Callable,
    Sequence,
    Any,
    List,
    Union,
    Awaitable,
    Optional,
    Hashable,
    Type,
    Mapping,
    Iterator,
    AsyncIterator,
    TypeVar,
)

Input = TypeVar("Input", contravariant=True)
Output = TypeVar("Output", covariant=True)


class NodeConfig(BaseModel):
    name: Optional[str] = Field(default=None, description="The name of the node.")
    runnable: Optional[
        Union[
            Callable[[Input], Output],
            Callable[[Input], Awaitable[Output]],
            Callable[[Iterator[Input]], Iterator[Output]],
            Callable[[AsyncIterator[Input]], AsyncIterator[Output]],
            Mapping[str, Any],
        ]
    ] = Field(default=None, description="The runnable for the node.")
    retry_policy: Optional[RetryPolicy] = Field(default_factory=RetryPolicy)
    nodes: Optional[Sequence["NodeConfig"]] = Field(
        default=None, description="Sequence of nodes to be executed"
    )

    @field_validator("nodes", mode="after")
    def validate_nodes(cls, nodes: Optional[Sequence["NodeConfig"]]):
        if nodes:
            for sub_node in nodes:
                if not sub_node.name or not sub_node.runnable:
                    raise ValueError(
                        "Each node in the sequence must have a 'name' and a 'runnable'."
                    )
        return nodes

    @field_validator("name", "runnable", mode="after")
    def validate_node_config(cls, value, values):
        if values.get("nodes") is None and (
            values.get("name") is None or values.get("runnable") is None
        ):
            raise ValueError(
                "A NodeConfig must have a 'name' and a 'runnable' if no nested nodes are defined."
            )
        return value

    class Config:
        arbitrary_types_allowed = True


class EdgeConfig(BaseModel):
    start_key: Union[str, list[str]] = Field(
        ..., description="The starting node(s) key(s) for the edge."
    )
    end_key: str = Field(..., description="The ending node key for the edge.")

    class Config:
        arbitrary_types_allowed = True


class ConditionalEdgeConfig(BaseModel):
    source: str = Field(
        ..., description="The source node key for the conditional edge."
    )
    path: Union[
        Callable[..., Union[Hashable, list[Hashable]]],
        Callable[..., Awaitable[Union[Hashable, list[Hashable]]]],
        Runnable[Any, Union[Hashable, list[Hashable]]],
    ] = Field(..., description="The callable or runnable defining the path logic.")
    path_map: Optional[Union[dict[Hashable, str], list[str]]] = Field(
        None, description="Mapping of path results to next node keys."
    )
    then: Optional[str] = Field(
        None, description="The fallback node key if no path matches."
    )

    class Config:
        arbitrary_types_allowed = True


class GraphBuilderConfig(BaseModel):
    state_schema: Type[Union[BaseModel, Any]] = Field(
        ..., description="The schema for the state managed by the graph."
    )
    config_schema: Optional[Type[Union[BaseModel, Any]]] = Field(
        None, description="Optional schema for the graph configuration."
    )
    nodes: List[NodeConfig] = Field(
        ..., description="List of node configurations for the graph."
    )
    edges: List[EdgeConfig] = Field(
        default_factory=list, description="List of edges connecting the nodes."
    )
    conditional_edges: List[ConditionalEdgeConfig] = Field(
        default_factory=list,
        description="List of conditional edges defining dynamic transitions.",
    )
    db_conn_string: Optional[str] = Field(
        default=config("DB_CONN_STRING"), description="Database connection string"
    )

    class Config:
        arbitrary_types_allowed = True


class GraphBuilder:
    def __init__(self, config: GraphBuilderConfig):
        self.workflow = StateGraph(
            state_schema=config.state_schema, config_schema=config.config_schema
        )
        self.config = config
        self.DB_CONN_STRING = config.db_conn_string

    def __add_nodes(self):
        for node_config in self.config.nodes:
            if node_config.nodes:
                self.workflow.add_sequence(
                    nodes=[
                        (node.name, node.runnable)
                        for node in node_config.nodes
                        if node.name is not None and node.runnable is not None
                    ]
                )
            elif node_config.name and node_config.runnable:
                self.workflow.add_node(
                    node_config.name,
                    node_config.runnable,
                    retry=node_config.retry_policy,
                )
            else:
                raise ValueError(
                    "Node config must define either a single node with 'name' and 'runnable' or a valid sequence of nodes."
                )

    def __add_edges(self):
        for edge in self.config.edges:
            self.workflow.add_edge(edge.start_key, edge.end_key)

    def __add_conditional_edges(self):
        for conditional_edge in self.config.conditional_edges:
            self.workflow.add_conditional_edges(
                path=conditional_edge.path,
                path_map=conditional_edge.path_map,
                then=conditional_edge.then,
                source=conditional_edge.source,
            )

    def __compile(self, with_memory: Optional[bool] = False) -> CompiledStateGraph:
        """Compile the graph using a synchronous PostgresSaver checkpointer."""
        self.__add_nodes()
        self.__add_edges()
        self.__add_conditional_edges()
        if with_memory:
            with PostgresSaver.from_conn_string(self.DB_CONN_STRING) as checkpointer:
                return self.workflow.compile(checkpointer=checkpointer)
        else:
            return self.workflow.compile()

    async def __acompile(
        self, with_memory: Optional[bool] = False
    ) -> CompiledStateGraph:
        """Compile the graph using an asynchronous AsyncPostgresSaver checkpointer."""
        self.__add_nodes()
        self.__add_edges()
        self.__add_conditional_edges()
        if with_memory:
            async with AsyncPostgresSaver.from_conn_string(
                self.DB_CONN_STRING
            ) as checkpointer:
                return self.workflow.compile(checkpointer=checkpointer)
        else:
            return self.workflow.compile()

    @classmethod
    def from_config(
        cls, config: GraphBuilderConfig, with_memory: Optional[bool] = False
    ) -> CompiledStateGraph:
        """Create a GraphBuilder instance from a config and compile the graph synchronously."""
        builder = cls(config)
        return builder.__compile(with_memory=with_memory)

    @classmethod
    async def afrom_config(
        cls, config: GraphBuilderConfig, with_memory: Optional[bool] = False
    ) -> CompiledStateGraph:
        """Create a GraphBuilder instance from a config and compile the graph asynchronously."""
        builder = cls(config)
        return await builder.__acompile(with_memory=with_memory)
