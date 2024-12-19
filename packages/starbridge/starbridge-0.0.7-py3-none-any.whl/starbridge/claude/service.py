import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import typer

from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool

from . import cli


class Service(MCPBaseService):
    """Service class for Claude operations."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_cli() -> tuple[str | None, typer.Typer | None]:
        """Get CLI for Claude service."""
        return "claude", cli.cli

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> str:
        """Check if Claude Desktop application is installed and is running."""
        if not self.is_installed():
            return "DOWN: Not installed"
        if not self.is_running():
            return "DOWN: Not running"
        return "UP"

    @mcp_tool()
    def info(self, context: MCPContext | None = None):
        """Get info about Claude Desktop application."""
        data = {
            "is_installed": self.is_installed(),
            "application_directory": None,
            "config_path": None,
            "log_path": None,
            "config": None,
        }
        if self.is_installed():
            data["application_directory"] = str(self.application_directory())
            if self.has_config():
                data["config_path"] = str(self.config_path())
                data["config"] = self.config_read()
                data["log_path"] = str(self.log_path())
        return data

    @mcp_tool()
    def restart(self, context: MCPContext | None = None):
        """Restart Claude Desktop application."""
        self._restart()
        return "Claude Desktop application restarted"

    @staticmethod
    def application_directory() -> Path:
        """Get path of Claude config directory based on platform."""
        if sys.platform == "darwin":
            return Path(Path.home(), "Library", "Application Support", "Claude")
        elif sys.platform == "win32":
            return Path(Path.home(), "AppData", "Roaming", "Claude")
        elif sys.platform == "linux":
            return Path(Path.home(), ".config", "Claude")
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    # Move all the static methods from Application
    @staticmethod
    def is_installed() -> bool:
        """Check if Claude Desktop application is installed."""
        return Service.application_directory().is_dir()

    @staticmethod
    def is_running() -> bool:
        """Check if Claude Desktop application is running."""
        if platform.system() != "Darwin":
            raise RuntimeError("This command only works on macOS")
        ps_check = subprocess.run(
            ["pgrep", "-x", "Claude"], capture_output=True, text=True, check=False
        )
        return ps_check.returncode == 0

    @staticmethod
    def config_path() -> Path:
        """Get path of Claude config based on platform."""
        return Service.application_directory() / "claude_desktop_config.json"

    @staticmethod
    def has_config() -> bool:
        """Check if Claud has configuration."""
        return Service.config_path().is_file()

    @staticmethod
    def config_read() -> dict:
        """Read config from file."""
        config_path = Service.config_path()
        if config_path.is_file():
            with open(config_path, encoding="utf8") as file:
                return json.load(file)
        raise FileNotFoundError(f"No config file found at '{config_path}'")

    @staticmethod
    def config_write(config: dict) -> dict:
        """Write config to file."""
        config_path = Service.config_path()
        with open(config_path, "w", encoding="utf8") as file:
            json.dump(config, file, indent=2)
        return config

    @staticmethod
    def log_directory() -> Path:
        """Get path of Claude log directory based on platform."""
        if sys.platform == "darwin":
            return Path(
                Path.home(),
                "Library",
                "Logs",
                "Claude",
            )
        elif sys.platform == "win32":
            return Path(
                Path.home(),
                "AppData",
                "Roaming",
                "Claude",
                "logs",
            )
        elif sys.platform == "linux":
            return Path(
                Path.home(),
                ".logs",
                "Claude",
            )
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    @staticmethod
    def log_path(mcp_server_name: str | None = "starbridge") -> Path:
        """Get path of mcp ."""
        path = Service.log_directory()
        if mcp_server_name is None:
            return path / "mcp.log"
        return path / f"mcp-server-{mcp_server_name}.log"

    @staticmethod
    def install_mcp_server(
        mcp_server_config: dict, mcp_server_name="starbridge", restart=True
    ) -> bool:
        """Install MCP server in Claude Desktop application."""
        if Service.is_installed() is False:
            raise RuntimeError(
                f"Claude Desktop application is not installed at '{Service.application_directory()}'"
            )
        try:
            config = Service.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}

        if (
            mcp_server_name in config["mcpServers"]
            and config["mcpServers"][mcp_server_name] == mcp_server_config
        ):
            return False

        config["mcpServers"][mcp_server_name] = mcp_server_config
        Service.config_write(config)
        if restart:
            Service.restart()
        return True

    @staticmethod
    def uninstall_mcp_server(mcp_server_name: str = "starbridge", restart=True) -> bool:
        """Uninstall MCP server from Claude Desktop application."""
        if Service.is_installed() is False:
            raise RuntimeError(
                f"Claude Desktop application is not installed at '{Service.application_directory()}'"
            )
        try:
            config = Service.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}
        if "name" not in config["mcpServers"]:
            return False
        del config["mcpServers"][mcp_server_name]
        Service.config_write(config)
        if restart:
            Service.restart()
        return True

    @staticmethod
    def _restart():
        """Restarts the Claude desktop application on macOS."""
        if platform.system() != "Darwin":
            raise RuntimeError("This command only works on macOS")

        ps_check = subprocess.run(
            ["pgrep", "-x", "Claude"], capture_output=True, text=True, check=False
        )

        if ps_check.returncode == 0:
            subprocess.run(["pkill", "-x", "Claude"], check=False)
            time.sleep(1)

        subprocess.run(["open", "-a", "Claude"], check=True)

    @staticmethod
    def _run_brew_command(args: list) -> tuple[int, str, str]:
        """Run a homebrew command and return (returncode, stdout, stderr)"""
        process = subprocess.run(
            ["brew"] + args, capture_output=True, text=True, check=False
        )
        return process.returncode, process.stdout, process.stderr

    @staticmethod
    def install_via_brew() -> bool:
        """Install Claude via Homebrew if not already installed."""
        if platform.system() != "Darwin":
            raise RuntimeError("Homebrew installation only supported on macOS")

        # Check if already installed
        returncode, _, _ = Service._run_brew_command(["list", "--cask", "claude"])
        if returncode == 0:
            return False  # Already installed

        # Install Claude
        returncode, _, stderr = Service._run_brew_command([
            "install",
            "--cask",
            "claude",
        ])
        if returncode != 0:
            raise RuntimeError(f"Failed to install Claude: {stderr}")

        return True

    @staticmethod
    def uninstall_via_brew() -> bool:
        """Uninstall Claude via Homebrew."""
        if platform.system() != "Darwin":
            raise RuntimeError("Homebrew uninstallation only supported on macOS")

        # Check if installed
        returncode, _, _ = Service._run_brew_command(["list", "--cask", "claude"])
        if returncode != 0:
            return False  # Not installed

        # Uninstall Claude
        returncode, _, stderr = Service._run_brew_command([
            "uninstall",
            "--cask",
            "claude",
        ])
        if returncode != 0:
            raise RuntimeError(f"Failed to uninstall Claude: {stderr}")

        return True
