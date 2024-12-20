import sys
import os
import json
from monopylib.common.logging_config import get_logger

logger = get_logger(__name__)

def resolve_requirements(dep_file, repo_base_dir, component_dir, visited):
    """Helper function to resolve requirements recursively."""
    if dep_file in visited:
        return set()  # Avoid circular dependencies
    visited.add(dep_file)

    if not os.path.exists(dep_file):
        logger.warning(f"Dependency config file {dep_file} not found. Skipping.")
        return set()

    with open(dep_file, "r") as f:
        data = json.load(f)

    # Collect direct requirements and transitive dependencies
    requirements = set(data.get("requirements", []))
    local_dependencies = data.get("local_dependencies", [])
    for dep in local_dependencies:
        dep_config = os.path.join(repo_base_dir, component_dir, dep, "local-utils.json")
        requirements.update(resolve_requirements(dep_config, repo_base_dir, component_dir, visited))

    return requirements

def update_local_dependencies_requirements(repo_base_dir: str, component_dir: str, config_file: str):
    """Updates the `local_dependencies_requirements` field in the `local-utils.json` file."""
    visited = set()

    # Resolve all transitive requirements
    transitive_requirements = resolve_requirements(config_file, repo_base_dir, component_dir, visited)

    # Load current config file
    with open(config_file, "r") as f:
        data = json.load(f)

    # Update local_dependencies_requirements
    data["local_dependencies_requirements"] = sorted(transitive_requirements - set(data.get("requirements", [])))

    # Write the updated config back to file
    with open(config_file, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Updated {config_file} with resolved local dependencies requirements.")

def resolve_dependencies(dep_file, stack, repo_base_dir, component_dir, visited, logger):
    """Helper function to resolve dependencies recursively."""
    if dep_file in visited:
        raise RuntimeError(f"Circular dependency detected: {' -> '.join(stack)} -> {dep_file}")
    visited.add(dep_file)
    stack.append(dep_file)
    if not os.path.exists(dep_file):
        logger.warning(f"Dependency config file {dep_file} not found. Skipping.")
        return

    with open(dep_file, "r") as f:
        dependencies = json.load(f).get("local_dependencies", [])

    for dep in dependencies:
        dep_config = os.path.join(repo_base_dir, component_dir, dep, "local-utils.json")
        dep_app_path = os.path.abspath(os.path.join(repo_base_dir, component_dir, dep, "app"))

        if dep_app_path not in sys.path:
            sys.path.insert(0, dep_app_path)
            logger.info(f"Added {dep_app_path} to PYTHONPATH.")

        resolve_dependencies(dep_config, stack, repo_base_dir, component_dir, visited, logger)
    stack.pop()

def load_dependencies(repo_base_dir: str, component_dir: str, config_file: str):
    """Recursively loads dependencies for a component."""
    visited = set()
    resolve_dependencies(config_file, [], repo_base_dir, component_dir, visited, logger)
    
    # Update local dependencies requirements after loading all dependencies
    update_local_dependencies_requirements(repo_base_dir, component_dir, config_file)

    logger.info("All dependencies loaded successfully.")

