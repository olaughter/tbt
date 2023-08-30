import logging
import os
from typing import List

import networkx as nx
import yaml
from networkx.classes.digraph import DiGraph

from tbt.definitions.definition_objects import Definition, Pipeline, Pipelines


class DefinitionsParser:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def parse(self):
        """Reads all tbt*.yaml files within the root_dir

        Includes any found recursively within subfolders, parses, validates and sorts
        the dependencies as an acyclic directed graph. Stores the parsed pipelines
        into a lookup table"""
        self.definitions = self.find_definitions()
        self.unsorted_pipelines = self.load_pipelines(self.definitions)
        self.pipelines = self.sort_pipelines(self.unsorted_pipelines)
        logging.info(
            f"Found: {len(self.definitions)} tbt files,"
            f"totalling {len(self.pipelines)} pipelines"
        )

    def find_definitions(self) -> List[Definition]:
        """Find all tbt*.yaml files within the root_dir

        Also recursively collects any found in subfolders
        """
        definitions_files = []
        for root, _, files in os.walk(self.root_dir):
            for f in files:
                if f.startswith("tbt") and f.endswith(".yaml"):
                    definition = Definition(
                        root=root,
                        file_name=f,
                    )
                    definitions_files.append(definition)
        return definitions_files

    def load_pipelines(self, definitions: List[Definition]) -> Pipelines:
        """Load all pipelines from the definition files"""
        all_pipelines = {}
        for definition in definitions:
            with open(definition.path, "r") as f:
                contents = yaml.safe_load(f)
                pipeline_definitions = contents.get("pipelines")
                for k, v in pipeline_definitions.items():
                    if k in all_pipelines:
                        logging.error(
                            f"Found pipeline: {k}, in definition files:"
                            f"\n - {f.name} \n - {all_pipelines[k].definition.path}"
                        )
                        raise ValueError(f"Duplicate pipeline definition for: {k}")
                    else:
                        pipeline = Pipeline(label=k, definition=definition, **v)
                        all_pipelines[pipeline.label] = pipeline

        return all_pipelines

    def sort_pipelines(self, pipelines: Pipelines) -> Pipelines:
        """Validates that the graph is valid, and sorts it

        Works by building a directed acyclic graph of the pipelines
        and their dependencies. If the graph is not acyclic, it will
        raise an error. Otherwise it will sort it based on dependencies
        """
        graph = nx.DiGraph()
        graph.add_nodes_from(self._get_nodes(pipelines))
        graph.add_edges_from(self._get_edges(pipelines))
        if not nx.is_directed_acyclic_graph(graph):
            broken_files, cycles = self._get_files_with_cycles(graph, pipelines)
            raise ValueError(
                f"Found circular dependencies in files: {broken_files}, "
                "cycles: {cycles}"
            )
        order = list(nx.topological_sort(graph))
        sorted_pipelines = {k: pipelines[k] for k in order}
        return sorted_pipelines

    def _get_nodes(self, pipelines: Pipelines) -> List[str]:
        """Get all pipeline labels as a list"""
        return [p.label for p in pipelines.values()]

    def _get_edges(self, pipelines: Pipelines) -> List[tuple[str, str]]:
        """Get all graph connections as a list of tuples

        Also validates that the depends_on list is valid.
        """
        edges = []
        for pipeline in pipelines.values():
            if pipeline.depends_on:
                if not isinstance(pipeline.depends_on, list):
                    raise ValueError(
                        f"depends_on must be a list for: {pipeline.label}, "
                        "in {pipeline.definition.path}"
                    )
                for dependency in pipeline.depends_on:
                    if dependency not in pipelines:
                        raise ValueError(
                            f"Dependency: {dependency}, for pipeline: {pipeline.label},"
                            " in {pipeline.definition.path}, does not exist"
                        )
                    edges.append((dependency, pipeline.label))
        return edges

    def _get_files_with_cycles(
        self, graph: DiGraph, pipelines: Pipelines
    ) -> tuple[list[str], list[tuple[str]]]:
        """Get a list of files containing pipelines with circular dependencies"""
        cycles = nx.find_cycle(graph)
        broken_files = []
        for cycle in cycles:
            for node in cycle:
                path = pipelines[node].definition.path
                if path not in broken_files:
                    broken_files.append(path)
        return broken_files, cycles
