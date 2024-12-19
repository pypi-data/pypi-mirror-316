import os

import matplotlib.pyplot as plt
import networkx as nx
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.util import CommandError

from pylembic.exceptions import CircularDependencyError
from pylembic.logger import configure_logger


logger = configure_logger()


class Validator:
    """This class provides methods to validate Alembic migrations for linearity,
    missing nodes, and circular dependencies.

    Here is a summary of the checks performed:
        - Linearity: Ensures a clean and predictable migration chain.
        - Circular dependencies: Prevents migration failures due to loops in the
        dependency chain.
        - Disconnected roots: Identifies migrations improperly created without linking
        to the base.
        - Disconnected leaves: Flags migrations that are improperly disconnected from
        subsequent migrations.
        - Multiple roots/heads: Warns about unintentional forks or branching.
        - Graph visualization: Provides a visual way to catch anomalies and understand
        migration flow.
    """

    ALEMBIC_CONFIG_FILE = "alembic.ini"

    def __init__(
        self, alembic_config_path: str, alembic_config_file: str = None
    ) -> None:
        if not os.path.exists(alembic_config_path):
            raise FileNotFoundError(f"Path '{alembic_config_path}' does not exist!")

        self.alembic_config_path = alembic_config_path
        self.alembic_config_file = alembic_config_file or self.ALEMBIC_CONFIG_FILE
        self.graph = nx.DiGraph()
        self.verbose = False
        self.script: ScriptDirectory = None

        # Load the Alembic configuration
        self._load_alembic_config()

        # Build the migration graph
        self._build_graph()

    def _load_alembic_config(self) -> None:
        """Loads the Alembic configuration file and initializes the script directory."""
        alembic_config = Config(
            os.path.join(self.alembic_config_path, self.alembic_config_file)
        )
        alembic_config.set_main_option("script_location", self.alembic_config_path)
        self.script = ScriptDirectory.from_config(alembic_config)

    def _build_graph(self) -> None:
        """Builds a directed graph of migrations."""
        graph = nx.DiGraph()
        try:
            for revision in self.script.walk_revisions():
                graph.add_node(revision.revision)
                if revision.down_revision:
                    if isinstance(revision.down_revision, tuple):
                        # Handle branching migrations
                        for down_rev in revision.down_revision:
                            graph.add_edge(revision.revision, down_rev)
                    else:
                        graph.add_edge(revision.revision, revision.down_revision)
        except CommandError as exc:
            raise CircularDependencyError(str(exc)) from exc

        self.graph = graph

    def _orphans(self) -> bool:
        """
        Checks for orphan migrations in the Alembic script directory.
        As the orphan migrations are not connected to the migration graph, they are
        considered as a valid base and head.

        Returns:
            bool: True if orphan migrations are found.
        """
        bases = set(self.script.get_bases())
        heads = set(self.script.get_heads())
        orphans = bases.intersection(heads)
        if orphans:
            logger.warning("Orphan migrations detected.", extra={"orphans": orphans})
            return True

        logger.info("No orphan migrations detected.")
        return False

    def _multiple_bases_or_heads(self) -> bool:
        """
        Checks if there are multiple bases or heads in the migration graph.

        Returns:
            bool: True if multiple bases or heads are found.
        """
        bases = set(self.script.get_bases())
        if len(bases) > 1:
            logger.info("Multiple bases detected", extra={"bases": bases})
            return True

        heads = set(self.script.get_heads())
        if len(heads) > 1:
            logger.info("Multiple heads detected", extra={"heads": heads})
            return True

        return False

    def validate(self, verbose: bool = False) -> bool:
        """This method validates the Alembic migrations for linearity and missing nodes.

        Args:
            verbose (bool): If True, the logger verbosity is increased.

        Returns:
            bool: True if the migrations are valid.
        """
        # Reconfigure the logger verbosity
        logger = configure_logger(verbose)  # noqa F841

        # Perform validation checks within the graph
        return not (self._orphans() or self._multiple_bases_or_heads())

    def show_graph(self) -> None:
        """
        Visualizes the migration dependency graph.
        """
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)
        labels = {node: f"{node[:8]}" for node in self.graph.nodes}  # Short revision ID
        nx.draw(
            self.graph,
            pos,
            labels=labels,
            node_size=3000,
            node_color="lightblue",
            font_size=10,
            font_weight="bold",
            label="Alembic Migration Graph",
        )
        # Set the custom window title
        manager = plt.get_current_fig_manager()
        manager.set_window_title("Alembic Migration Dependency Graph")
        plt.show()
