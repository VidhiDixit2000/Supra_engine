# Data Sources

## Overview

All 50 knowledge nodes, the 15-level hierarchy, the 7 user profiles, and the edges used in this
project were **provided directly by Astroum AI** in the assessment's Setup Guide document
("SEED DATA — ORGANIZATION + HIERARCHY", "SEED DATA — 7 USERS", "SEED DATA — 50 KNOWLEDGE NODES",
"SEED DATA — EDGES"). No original clinical data collection, sourcing, or research was performed —
this project consumes the seed dataset exactly as supplied, loaded verbatim into Supabase via the
provided `schema.sql`/seed SQL.

## Nature of the underlying content

The seed data represents a **fictional hospital** ("Supra Multi-Specialty Hospital," `org_id =
'supra'`) and fictional patients (e.g., "Rajan," "Padma," "Aadhya"). It is explicitly a synthetic
dataset constructed for this assessment, not real patient records or an export from any real
hospital system.

That said, the *clinical facts embedded within* the synthetic protocols reflect genuine, publicly
known medical knowledge — for example:
- Warfarin + NSAID co-administration carrying elevated GI bleed risk is standard, widely
  documented pharmacology (not something specific to this fictional hospital).
- DVT prophylaxis timing conventions post-orthopaedic surgery, penicillin/cephalosporin
  cross-reactivity percentages, and WHO's 5-moment hand hygiene framework are all real, general
  clinical/public-health knowledge that the seed data's authors incorporated into fictional
  hospital-specific policy language (e.g., specific drug brand names, specific dosing schedules
  attributed to "Dr. Vikram" or "Supra policy").

No claim is made that any specific dosing figure, named decision-maker, incident date, or
hospital-specific numeric target (e.g., "88% hand hygiene compliance") in the seed data
corresponds to a real, verifiable clinical source — these are illustrative details invented for
the assessment's narrative, consistent with the assessment's own framing of "Supra Hospital" as a
fictional example organization.

## Schema and constraint modifications

One schema-level deviation from the provided `schema.sql` was made during setup: the
`UNIQUE(org_id, level_number, department)` constraint on `hierarchy_levels` was dropped, because
the provided seed data itself violates it (three legitimate distinct sub-unit rows share
`(supra, 8, ortho)`). This is a structural/schema fix, not a data-sourcing decision — documented in
full in `docs/architecture.md`, section 5.

## Summary

| Item | Source |
|---|---|
| Hierarchy structure (15 levels, DAG edges) | Provided by Astroum AI, Setup Guide |
| 50 knowledge nodes (content, tags, scores) | Provided by Astroum AI, Setup Guide |
| 7 user profiles | Provided by Astroum AI, Setup Guide |
| Underlying general clinical facts referenced within node content | Publicly known, standard medical/pharmacological knowledge (not independently re-verified against primary literature for this assessment) |
| Hospital name, patient names, specific incident narratives, internal policy numbers | Fictional, assessment-authored illustrative content |

---

## Runtime Data Flow

No external APIs, third-party datasets, or online clinical knowledge sources are queried during
pipeline execution — everything below operates on the seed dataset described above, already
loaded into Supabase via `schema.sql` and `seed.sql`.

### `users` table
Used for: user identification, role and department information, permission compilation, entry
point resolution.

### `hierarchy_levels` table
Used for: building the hospital hierarchy, BFS traversal (`parent_ids`), department-scoped
traversal, multi-parent relationship handling (e.g. `HL-08-POST-TKR`).

### `knowledge_nodes` table
Used for: candidate set generation, zone classification (Zone 1 department-specific / Zone 2
global), compliance tag filtering, temporal (supersession/expiry) checks, and derivability
filtering.

### Derived data (not persisted)
The following are computed fresh on each pipeline run and returned only in the API response —
never written back to the database: entry point, reachable hierarchy set, candidate set, filter
funnel counts, pipeline timing, summary metrics.

### Frontend access
The React frontend never queries Supabase directly. All data is retrieved from the FastAPI
backend via REST endpoints (e.g. `GET /users`, `GET /candidate-set/{user_id}`), which in turn
query the database and run the pipeline described above.
