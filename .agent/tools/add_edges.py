import json, pathlib
g = pathlib.Path(".context/graph.json")
data = json.loads(g.read_text())
ids = {n["id"] for n in data["nodes"]}
edges = []
cat_prefix = "docs/skills/"
catalog = "docs/skills/README.md::skills"
for n in data["nodes"]:
    if n["content_ref"].startswith(cat_prefix) and n["content_ref"] != "docs/skills/README.md" and " -- " in n["summary"]:
        edges.append({"from": catalog, "to": n["id"], "type": "requires", "note": "catalog routes to each skill"})
res = "docs/resources/README.md::resources-skills-archive-provenance"
for nid in ["docs/skills/README.md::skills",
            "docs/resources/project-management.md::project-management-skills-shortlist"]:
    if nid in ids:
        edges.append({"from": res, "to": nid, "type": "requires", "note": "resources route to formatted catalogs"})
data["edges"] = edges
g.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"nodes: {len(data['nodes'])}, edges: {len(edges)}")
