import os
import json
from monopylib.common.logging_config import get_logger

logger = get_logger(__name__)


def update_dockerignore(repo_base_dir, services_dir, caller_dir, utils_dir, config_file):
    """Generates `.dockerignore` based on resolved dependencies."""
    python_ignores = [
        "__pycache__/", "*.pyc", "*.pyo", "*.egg-info/", ".eggs/", ".mypy_cache/", ".pytest_cache/"
    ]
    visited = set()

    def resolve_dependencies(dep_file, stack):
        if dep_file in visited:
            raise RuntimeError(f"Circular dependency detected: {' -> '.join(stack)} -> {dep_file}")
        visited.add(dep_file)
        stack.append(dep_file)
        if not os.path.exists(dep_file):
            logger.warning(f"Dependency config file {dep_file} not found. Skipping.")
            return set()

        with open(dep_file, "r") as f:
            dependencies = json.load(f).get("local_dependencies", [])

        resolved_deps = set(dependencies)
        for dep in dependencies:
            dep_config = os.path.join(repo_base_dir, utils_dir, dep, "local-utils.json")
            resolved_deps.update(resolve_dependencies(dep_config, stack))
        stack.pop()
        return resolved_deps

    resolved_dependencies = resolve_dependencies(config_file, [])
    services_path = os.path.join(repo_base_dir, services_dir)
    utils_path = os.path.join(repo_base_dir, utils_dir)

    ignored_services = [
        f"{services_dir}/{child}/" for child in os.listdir(services_path)
        if child != os.path.basename(caller_dir) and os.path.isdir(os.path.join(services_path, child))
    ]
    ignored_utils = [
        f"{utils_dir}/{child}/" for child in os.listdir(utils_path)
        if child not in resolved_dependencies and os.path.isdir(os.path.join(utils_path, child))
    ]

    dockerignore_path = os.path.join(repo_base_dir, ".dockerignore")
    with open(dockerignore_path, "w") as f:
        f.write("\n".join(python_ignores + ignored_services + ignored_utils) + "\n")
    logger.info(f"Updated .dockerignore with ignored paths.")

def update_requirements(repo_base_dir, utils_dir, config_file):
    """Appends resolved requirements to the `local_dependencies_requirements` field in local-utils.json."""
    visited = set()
    local_dep_reqs = set()

    def collect_requirements(dep_file, stack):
        if dep_file in visited:
            raise RuntimeError(f"Circular dependency detected: {' -> '.join(stack)} -> {dep_file}")
        visited.add(dep_file)
        stack.append(dep_file)

        if not os.path.exists(dep_file):
            logger.warning(f"Dependency config file {dep_file} not found. Skipping.")
            return set()

        with open(dep_file, "r") as f:
            data = json.load(f)
            local_dependencies = data.get("local_dependencies", [])
            requirements = data.get("requirements", [])
            local_dep_reqs.update(requirements)

            for dep in local_dependencies:
                dep_config = os.path.join(repo_base_dir, utils_dir, dep, "local-utils.json")
                local_dep_reqs.update(collect_requirements(dep_config, stack))
        stack.pop()
        return local_dep_reqs

    collect_requirements(config_file, [])

    # Update `local_dependencies_requirements` in the current config file
    with open(config_file, "r") as f:
        data = json.load(f)

    data["local_dependencies_requirements"] = sorted(local_dep_reqs)

    with open(config_file, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Updated {config_file} with resolved local dependencies requirements.")
