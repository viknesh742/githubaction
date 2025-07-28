import yaml
import os

# Load blueprint config
with open("blueprint.yml") as f:
    config = yaml.safe_load(f)

# ✅ Define pipeline first
pipeline = {
    "name": "Generated Pipeline",
    "on": {
        "workflow_dispatch": {}
    },
    "jobs": {}
}

# ✅ Add branching/tag strategy if defined
if "branching" in config:
    pipeline["on"]["push"] = {
        "branches": config["branching"].get("rules", ["main"])
    }

    if "tags" in config["branching"]:
        pipeline["on"]["push"]["tags"] = config["branching"]["tags"]

# Add language + build job
language_template = f"templates/{config['language']}/{config['build_tool']}.yml"
if os.path.exists(language_template):
    with open(language_template) as f:
        pipeline["jobs"].update(yaml.safe_load(f))

# Add each stage
for stage in config["stages"]:
    stage_path = f"stages/{stage}.yml"
    if os.path.exists(stage_path):
        with open(stage_path) as f:
            pipeline["jobs"].update(yaml.safe_load(f))

# Add deploy method
deploy_path = f"deploy/{config['deployment']}.yml"
if os.path.exists(deploy_path):
    with open(deploy_path) as f:
        pipeline["jobs"].update(yaml.safe_load(f))

# Save the generated workflow
with open(".github/workflows/generated.yml", "w") as f:
    yaml.dump(pipeline, f, default_flow_style=False)
