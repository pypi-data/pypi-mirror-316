import os
import sys
import subprocess
import json
import logging
from pathlib import Path
import pkg_resources

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Add project base directory to sys.path
PROJECT_BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_BASE_DIR))

# Project-specific imports
from monopylib.common.config_manager import ConfigManager
from monopylib.init.service_runner import DynamicServiceRunner

class DependencyInstaller:
    def __init__(self, target: str, project_root: Path = None):
        self.target = target
        self.project_root = project_root or Path.cwd()
        self.config = ConfigManager.get_config(self.project_root / "config.json")
        self.venv_dir_name = self.config.get("venv_dir_name", ".venv")
        self.repo_name = self.config.get("repo_name", "demo-repo")
        self.repo_base_dir = self.project_root / self.repo_name

    @staticmethod
    def load_json(file_path: Path) -> dict:
        """Load a JSON file."""
        try:
            with file_path.open("r") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return {}

    def create_venv(self, target_dir: Path) -> Path:
        """Create a virtual environment in the target directory."""
        venv_path = target_dir / self.venv_dir_name
        if venv_path.exists():
            logger.info(f"Virtual environment already exists at {venv_path}")
        else:
            logger.info(f"Creating virtual environment in {venv_path}")
            try:
                subprocess.run(["python", "-m", "venv", str(venv_path)], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to create virtual environment: {e}")
                sys.exit(1)
        return venv_path

    def install_packages(self, venv_path: Path, packages: list[str]) -> None:
        """Install requirements using pip."""
        pip_executable = venv_path / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
        if not pip_executable.exists():
            logger.error(f"Pip executable not found: {pip_executable}")
            sys.exit(1)

        valid_packages = [pkg for pkg in packages if self.validate_package(pkg)]

        if not valid_packages:
            logger.warning("No valid packages to install.")
            return

        try:
            subprocess.run([str(pip_executable), "install", *valid_packages], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install packages: {e}")
            sys.exit(1)

    @staticmethod
    def validate_package(package: str) -> bool:
        """Validate the package format."""
        try:
            pkg_resources.Requirement.parse(package)
            return True
        except pkg_resources.RequirementParseError:
            logger.warning(f"Skipping invalid package: {package}")
            return False

    def resolve_dependencies(self, base_dir: Path, dependencies: list[str]) -> list[str]:
        """Recursively resolve dependencies specified in local-utils.json."""
        resolved_packages = []

        for dependency in dependencies:
            dependency_path = base_dir / self.config["utils_dir"] / dependency
            local_utils_file = dependency_path / self.config["local_utils_file"]

            if local_utils_file.exists():
                data = self.load_json(local_utils_file)
                resolved_packages.extend(data.get("requirements", []))
                resolved_packages.extend(self.resolve_dependencies(base_dir, data.get("local_dependencies", [])))
            else:
                logger.warning(f"Dependency {dependency} not found at {local_utils_file}. Skipping.")

        return resolved_packages

    def run_service(self, service_file: Path, args) -> None:
        """Run the specified service using DynamicServiceRunner."""
        try:
            logger.info(f"Initializing service run for: {service_file}")
            runner = DynamicServiceRunner()
            runner.run_service(service_file, args)
        except Exception as e:
            logger.error(f"Failed to run the service: {e}")
            sys.exit(1)

    def process_service_or_util(self, target_dir: Path, args) -> None:
        """Process a single service or utility."""
        logger.info(f"Processing {target_dir}...")
        venv_path = self.create_venv(target_dir)

        local_utils_file = target_dir / "local-utils.json"
        if not local_utils_file.exists():
            logger.warning(f"{local_utils_file} not found. Skipping.")
            return
        
        data = self.load_json(local_utils_file)
        requirements = data.get("requirements", [])
        local_dependencies = data.get("local_dependencies", [])
        local_dependency_requirements = data.get("local_dependencies_requirements", [])

        resolved_dependencies = self.resolve_dependencies(self.repo_base_dir, local_dependencies)

        all_requirements = list(set(requirements + local_dependency_requirements + resolved_dependencies))

        logger.info(f"Installing requirements for {target_dir}: {all_requirements}")
        self.install_packages(venv_path, all_requirements)

        # Determine if target is a service or utility
        main_service_file = target_dir / "app" / self.config["service_main_file"]
        util_file = target_dir / "app" / f"{target_dir.name}.py"

        if main_service_file.exists():
            logger.info(f"Detected service. Running: {main_service_file}")
            self.run_service(main_service_file, args)
        elif util_file.exists():
            logger.info(f"Detected utility. Executing: {util_file}")
            subprocess.run(["python", str(util_file)], check=True)
        else:
            logger.info(f"No executable file found in {target_dir}. Skipping.")

    def process_all(self, args) -> None:
        """Process all services and utilities."""
        for subdir in [self.config["services_dir"], self.config["utils_dir"]]:
            target_dir = self.repo_base_dir / subdir
            for item in target_dir.iterdir():
                if item.is_dir():
                    self.process_service_or_util(item, args)

    def process_specific(self, args) -> None:
        """Process a specific service or utility."""

        target_path = self.repo_base_dir / self.target
        if target_path.exists() and target_path.is_dir():
            self.process_service_or_util(target_path, args)
        else:
            logger.error(f"Target not found: {target_path}")
            sys.exit(1)

    def run(self, args) -> None:
        """Main function to process the target."""
        # args = "local-case"                 # Example arguments

        if self.target == "all":
            self.process_all(args)
        else:
            self.process_specific(args)

def main():
    """Main function to parse arguments and execute the script."""
    if len(sys.argv) < 2:
        logger.error("Usage: python installation.py [all|service/util_name]")
        sys.exit(1)
    args = "local-case"   

    target = sys.argv[1]
    installer = DependencyInstaller(target)
    installer.run(args)

if __name__ == "__main__":
    main()
