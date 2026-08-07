
def compute_compression_hint(distance) -> str:
    """
    distance 0-1 -> FULL
    distance 2   -> COMPRESSED
    distance 3+  -> CONSTRAINT_ONLY
    distance is None (Zone 2 nodes bypassing BFS) -> treated as
    maximally compressed, since there's no personal proximity signal.
    """
    if distance is None:
        return "CONSTRAINT_ONLY"
    if distance <= 1:
        return "FULL"
    if distance == 2:
        return "COMPRESSED"
    return "CONSTRAINT_ONLY"


def assemble_candidate_set(nodes: list) -> list[dict]:
    candidate_set = []

    for node in nodes:
        distance = getattr(node, "distance_from_entry", None)

        candidate_set.append({
            "id": node.id,
            "type": node.type,
            "title": node.title,
            "content": node.content,
            "importance": float(node.importance),
            "zone": node.zone,  # raw integer (1/2/3), matching the JSON example
            "hierarchy_level": getattr(node, "level_number", None),
            "department": node.department,
            "distance_from_entry": distance,
            "compression_hint": compute_compression_hint(distance),
        })

    return candidate_set