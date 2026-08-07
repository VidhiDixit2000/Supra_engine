from sqlalchemy.orm import Session
from app.models.knowledge_node import KnowledgeNode
from app.models.hierarchy_level import HierarchyLevel


class Zone2Injector:

    def inject(self, db: Session, reachable_nodes: list) -> list:
        """
        Takes the BFS-reached knowledge nodes and adds every Zone 2
        (GLOBAL) node not already present. Zone 2 nodes still need
        to pass all 5 checks afterward — this step only merges them
        into the candidate pool.
        """
        zone2_nodesrows_tuples = (
    db.query(
        KnowledgeNode,
        HierarchyLevel.level_number
    )
    .join(
        HierarchyLevel,
        KnowledgeNode.hierarchy_level_id == HierarchyLevel.id
    )
    .filter(
        KnowledgeNode.zone == 2
    )
    .all()
)

        existing_ids = {n.id for n in reachable_nodes}
        combined = list(reachable_nodes)

        for node, level_number in zone2_nodesrows_tuples:
            node.level_number = level_number  # attach, consistent with fetch_reachable_nodes
            if node.id not in existing_ids:
                node.distance_from_entry = None
                combined.append(node)


        return combined