import yaml
import os

with open("blueprint.yml") as f:
    config = yaml.safe_load(f)

pipeline = {
    "name": "Generated Pipeline",
    "on": {"workflow_dispatch": {}},
    "jobs": {}
}

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

# Save to GitHub Actions workflow path
with open(".github/workflows/generated.yml", "w") as f:
    yaml.dump(pipeline, f, default_flow_style=False)

import glob

for file in glob.glob("templates/**/*.yml", recursive=True) + \
            glob.glob("stages/*.yml") + \
            glob.glob("deploy/*.yml"):
    with open(file) as f:
        if "@v3" in f.read():
            print(f"⚠️ WARNING: Deprecated @v3 found in {file}")
