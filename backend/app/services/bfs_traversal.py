from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

from collections import deque
from sqlalchemy.orm import Session
from app.models.knowledge_node import KnowledgeNode


from app.models.hierarchy_level import HierarchyLevel


class BFSTraversal:

    def traverse(self, db: Session, entry_node_id: str) -> dict[str, int]:

        # ONE query, fetch everything upfront
        all_levels = db.query(HierarchyLevel).all()

        # Build in-memory lookup structures
        levels_by_id = {h.id: h for h in all_levels}

        # Precompute children map: parent_id -> [child_ids]
        children_by_parent = {}
        for h in all_levels:
            for parent_id in h.parent_ids:
                children_by_parent.setdefault(parent_id, []).append(h.id)

        entry = levels_by_id.get(entry_node_id)
        if entry is None:
            raise ValueError(f"Entry point '{entry_node_id}' not found.")

        entry_department = entry.department
        traverse_all = entry_department is None

        queue = deque()
        visited = set()
        reachable_nodes = {}

        queue.append((entry_node_id, 0))

        while queue:
            current_id, distance = queue.popleft()

            if current_id in visited:
                continue

            visited.add(current_id)
            reachable_nodes[current_id] = distance

            current = levels_by_id.get(current_id)
            if current is None:
                continue

            # Walk UP — no query, just dict lookups
            for parent_id in current.parent_ids:
                if parent_id not in visited:
                    queue.append((parent_id, distance + 1))

            # Sideways/down expansion — also no query
            should_expand = traverse_all or (current.department == entry_department)
            if should_expand:
                for child_id in children_by_parent.get(current_id, []):
                    if child_id not in visited:
                        queue.append((child_id, distance + 1))

        return reachable_nodes

    def fetch_reachable_nodes(self, db: Session, bfs_result: dict) -> list:
    #Takes BFS output (hierarchy_level_id -> distance) and returns
    #the actual knowledge_node rows attached to those levels.'''

        reachable_level_ids = list(bfs_result.keys())

        rowsoftuples = (
          db.query(
        KnowledgeNode,
        HierarchyLevel.level_number
    )
    .join(
        HierarchyLevel,
        KnowledgeNode.hierarchy_level_id == HierarchyLevel.id
    )
    .filter(
        KnowledgeNode.hierarchy_level_id.in_(reachable_level_ids)
    )
    .all()
       )

    # Attach each node's distance for later use (compression_hint depends on this)
        nodes = []
        for knode, level_number in rowsoftuples:
            knode.distance_from_entry = bfs_result[knode.hierarchy_level_id]
            knode.level_number = level_number  # attach for later use in output
            nodes.append(knode)

        return nodes



    def build_dag_payload(self, all_levels: list, bfs_result: dict, entry_point: str) -> dict:
        """Builds node/edge data for the frontend DAG visualization.
        Every hierarchy_level becomes a node, flagged reachable/unreachable.
        Every parent_id relationship becomes an edge.
        """
        nodes = []
        edges = []

        for h in all_levels:
            nodes.append({
                "id": h.id,
                "label": h.level_name,
                "level_number": h.level_number,
                "department": h.department,
                "reachable": h.id in bfs_result,
                "distance": bfs_result.get(h.id),
                "is_entry_point": h.id == entry_point,
            })

            for parent_id in h.parent_ids:
                edges.append({"source": h.id, "target": parent_id})

        return {"nodes": nodes, "edges": edges}

