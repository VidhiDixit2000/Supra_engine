from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.pipeline import router as pipeline_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipeline_router)




















'''from app.database import SessionLocal
from app.services.permission_compiler import PermissionCompiler
from app.services.entry_point_resolver import EntryPointResolver
from app.services.bfs_traversal import BFSTraversal
from app.services.zone2_injector import Zone2Injector
from app.models import user
from app.services.five_checks import FiveCheckFilter
from app.services.assembler import assemble_candidate_set
from app.services.pipeline_orchestrator import run_pipeline

db = SessionLocal()

compiler = PermissionCompiler()

context = compiler.compile(
    db=db,
    user_id="U-SURESH"
)

print('output:', list(context.items()))

db.close()


resolver = EntryPointResolver()

hierarchy = resolver.resolve(
    db=db,
    user_id="U-SURESH"
)

print('output:', hierarchy)

db.close()

#---------------------------


bfs = BFSTraversal()
result = bfs.traverse(db=db, entry_node_id="HL-05-ORTHO")

print(f"Total hierarchy levels reached: {len(result)}")
print("Reached levels (id → distance from entry):")
for node_id, distance in sorted(result.items(), key=lambda x: x[1]):
    print(f"  {node_id}: distance {distance}")

knodes= bfs.fetch_reachable_nodes(db=db, bfs_result=result)

print(f"Total knowledge nodes reached: {len(knodes)}")
for knode in knodes:
    print(f"  {knode.id}: {knode.title}")



# ... after your existing bfs.fetch_reachable_nodes() call ...

injector = Zone2Injector()
combined = injector.inject(db=db, reachable_nodes=knodes)

print(f"Total after Zone 2 injection: {len(combined)}")
for node in combined:
    print(f"  {node.id}: {node.title} (distance={node.distance_from_entry})")


filter_obj = FiveCheckFilter()


compiler = PermissionCompiler()

USER = db.query(user.User).filter(user.User.id == "U-VIKRAM").first()
context = compiler.compile(
    db=db,
    user_id=USER.id
)
final_nodes = filter_obj.run(

    nodes=combined,
    user=USER,
    permission_compiler_bool=context
)
print(f"Total after 5 checks: {len(final_nodes)}")
for node in final_nodes:
    print(f"  {node.id}: {node.title} (level={node.level_number}, distance={node.distance_from_entry})")

candidate_set = assemble_candidate_set(final_nodes)

print(f"Candidate set size: {len(candidate_set)}")
for c in candidate_set[:3]:
    print(c)


result = run_pipeline(db, "U-PRIYA")
print(result)

db.close()'''