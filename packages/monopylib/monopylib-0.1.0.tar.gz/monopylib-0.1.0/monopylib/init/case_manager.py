import os
import sys
from monopylib.common.dependency_manager import load_dependencies
from monopylib.common.file_manager import update_dockerignore, update_requirements
from monopylib.common.config_manager import ConfigManager  
from pathlib import Path

class CaseManager:
    def __init__(self, argv, caller_file, project_root):
        self.argv = argv
        self.caller_file = caller_file
        self.project_root = project_root
        self.config = ConfigManager.get_config(self.project_root / "config.json")
        self.services_dir = self.config["services_dir"]
        self.utils_dir = self.config["utils_dir"]
        self.case, self.project_base_dir, self.repo_base_dir, self.caller_dir, self.config_file = self._determine_paths()

    def _determine_paths(self):
        """
        Determine paths and configuration based on the caller's location.
        """
        case = self.argv 

        caller_dir = os.path.abspath(os.path.join(os.path.dirname(self.caller_file), ".."))
        project_base_dir = Path(caller_dir).resolve().parents[2]
        repo_base_dir = project_base_dir / self.config["repo_name"]
        config_file = caller_dir + "/" + self.config["local_utils_file"]

        print(f"Case: {case}, Project Base Dir: {project_base_dir}, Repo Base Dir: {repo_base_dir}, "
              f"Caller Dir: {caller_dir}, Config File: {config_file}")

        return case, project_base_dir, repo_base_dir, caller_dir, config_file

    def set_service_paths(self, services_dir, utils_dir):
        """
        Dynamically adjust service and utility directories.
        """
        self.services_dir = services_dir
        self.utils_dir = utils_dir

    def _setup_ci(self):
        update_dockerignore(self.repo_base_dir, self.services_dir, self.caller_dir, self.utils_dir, self.config_file)

    def _setup_build(self):
        update_requirements(self.repo_base_dir, self.utils_dir, self.config_file)

    def _setup_local(self):
        update_requirements(self.repo_base_dir, self.utils_dir, self.config_file)
        load_dependencies(self.repo_base_dir, self.utils_dir, self.config_file)

    def _setup_docker(self):
        load_dependencies(self.repo_base_dir, self.utils_dir, self.config_file)

    def initialize_environment(self):
        """
        Initialize the environment based on the specified case.
        """
        setup_methods = {
            "ci-case": self._setup_ci,
            "build-case": self._setup_build,
            "local-case": self._setup_local,
            "docker-case": self._setup_docker,
        }

        try:
            setup_method = setup_methods.get(self.case)
            if not setup_method:
                raise ValueError(f"Unknown case '{self.case}'. Valid options are: {', '.join(setup_methods.keys())}.")

            setup_method()

            # Exit early for specific cases
            if self.case in ["ci-case", "build-case"]:
                print(f"Setup completed for '{self.case}'. Exiting early.")
                sys.exit(0)

            return True
        except ValueError as e:
            print(f"Error during setup: {e}")
            return False

    @classmethod
    def initialize_service_environment(cls, argv, caller_file):
        """
        Initialize the environment for a service.
        """
        print(f"argv:{argv}")
        project_root = Path(caller_file).resolve().parents[2]
        initializer = cls(argv, caller_file, project_root)
        initializer.set_service_paths("services", "utils")
        return initializer.initialize_environment()

    @classmethod
    def initialize_util_environment(cls, argv, caller_file):
        """
        Initialize the environment for a utility.
        """
        project_root = Path(caller_file).resolve().parents[2]
        initializer = cls(argv, caller_file, project_root)
        initializer.set_service_paths("utils", "utils")
        return initializer.initialize_environment()
