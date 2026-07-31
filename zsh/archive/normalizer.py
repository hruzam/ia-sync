import json
import sys
import os

def normalize(machine_name, registry_path):
    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    except Exception as e:
        print(f"echo '[ERROR] Could not read registry: {e}'; return 1")
        sys.exit(1)

    machine_config = registry.get(machine_name, {})
    if not machine_config:
        print(f"echo '[ERROR] Machine {machine_name} not found in registry'; return 1")
        sys.exit(1)

    # Print general variables
    for key, val in machine_config.get("vars", {}).items():
        if isinstance(val, str) and "~" in val:
            val = val.replace("~", os.path.expanduser("~"))
        print(f"export {key}='{val}'")

    # Print project variables
    projects = machine_config.get("projects", {})
    for proj_key, proj_data in projects.items():
        prefix = f"PROJECT_{proj_key}"
        for k, v in proj_data.items():
            if isinstance(v, str) and "~" in v:
                v = v.replace("~", os.path.expanduser("~"))
            print(f"export {prefix}_{k}='{v}'")

    print(f"echo '[normalizer] Hydrated environment for {machine_name} from registry'")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("echo '[ERROR] normalizer.py requires <machine_name> <registry_path>'; return 1")
        sys.exit(1)
    
    normalize(sys.argv[1], sys.argv[2])
