import time

from app.models.knowledge_node import KnowledgeNode
from app.services.assembler import assemble_candidate_set
from app.models.hierarchy_level import HierarchyLevel


def run_pipeline(db, user_id: str) -> dict:
    from app.models.user import User
    from app.services.permission_compiler import PermissionCompiler
    from app.services.entry_point_resolver import EntryPointResolver
    from app.services.bfs_traversal import BFSTraversal
    from app.services.zone2_injector import Zone2Injector
    from app.services.five_checks import FiveCheckFilter

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError(f"User '{user_id}' not found.")

    timing = {}
    t0 = time.perf_counter()

    t = time.perf_counter()
    permission_lookup = PermissionCompiler().compile(db=db, user_id=user.id)
    timing["permission_compile_ms"] = round((time.perf_counter() - t) * 1000, 2)

    t = time.perf_counter()
    entry_point = EntryPointResolver().resolve(db=db, user_id=user.id)
    bfs_result = BFSTraversal().traverse(db=db, entry_node_id=entry_point)
    reachable_nodes = BFSTraversal().fetch_reachable_nodes(db=db, bfs_result=bfs_result)
    timing["bfs_ms"] = round((time.perf_counter() - t) * 1000, 2)

    all_levels = db.query(HierarchyLevel).all()
    dag = BFSTraversal().build_dag_payload(all_levels, bfs_result, entry_point)

    t = time.perf_counter()
    combined = Zone2Injector().inject(db=db, reachable_nodes=reachable_nodes)
    timing["zone2_inject_ms"] = round((time.perf_counter() - t) * 1000, 2)

    funnel = {"total_nodes": db.query(KnowledgeNode).count(),
              "after_bfs": len(reachable_nodes),
              "after_zone2": len(combined)}

    filter_obj = FiveCheckFilter()
    final_nodes, check_timing, check_funnel = filter_obj.run_with_timing(
        nodes=combined, user=user, permission_lookup=permission_lookup
    )
    timing.update(check_timing)
    funnel.update(check_funnel)

    timing["total_ms"] = round((time.perf_counter() - t0) * 1000, 2)

    candidate_set = assemble_candidate_set(final_nodes)

    return {
        "user": user.id,
        "user_name": user.name,
        "role": user.role,
        "ceiling_level": user.ceiling_level,
        "entry_point": entry_point,
        "pipeline_timing": timing,
        "funnel": funnel,
        "candidate_set": candidate_set,
        "dag": dag,
    }