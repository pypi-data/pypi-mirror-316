"""
A simple singleton class that loads custom integration mappings, if available
"""

# pylint: disable=C0415


class IntegrationOverride:
    """
    Custom Mapping class for findings
    """

    from threading import Lock
    from typing import Optional

    _instance = None
    _lock = Lock()  # Ensures thread safety for singleton instance creation

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:  # Double-checked locking
                    cls._instance = super(IntegrationOverride, cls).__new__(cls)
        return cls._instance

    def __init__(self, app):
        from rich.console import Console

        config = app.config
        self.mapping = self._get_mapping(config)
        if not hasattr(self, "_initialized"):
            self.console = Console()
            self._log_mappings()
            self._initialized = True

    def _log_mappings(self):
        """
        Notify the user that overrides are found
        """
        from rich.table import Table

        table = Table(title="Custom Integration Mappings", show_header=True, header_style="bold magenta")
        table.add_column("Integration", width=12, style="cyan")
        table.add_column("Field", width=12, style="orange3")  # Ensure this color is supported
        table.add_column("Mapped Value", width=20, style="red")

        for integration, fields in self.mapping.items():
            for field, value in fields.items():
                if value != "default":
                    table.add_row(integration, field, value)

        if table.row_count > 0:
            self.console.print(table)

    def _get_mapping(self, config: dict) -> dict:
        """
        Loads the mapping configuration from the application config.

        :param dict config: The application configuration
        :return: The mapping configuration
        :rtype: dict
        """
        return config.get("findingFromMapping", {})

    def load(self, integration: Optional[str], field_name: Optional[str]) -> Optional[str]:
        """
        Retrieves the mapped field name for a given integration and field name.

        :param Optional[str] integration: The integration name
        :param Optional[str] field_name: The field name
        :return: The mapped field name
        :rtype: Optional[str]
        """
        if integration and self.mapping_exists(integration, field_name):
            integration_map = self.mapping.get(integration.lower(), {})
            return integration_map.get(field_name.lower())
        return None

    def mapping_exists(self, integration: str, field_name: str) -> bool:
        """
        Checks if a mapping exists for a given integration and field name.

        :param str integration: The integration name
        :param str field_name: The field name
        :return: Whether the mapping exists
        :rtype: bool
        """
        the_map = self.mapping.get(integration.lower())
        return the_map and field_name.lower() in the_map and the_map.get(field_name.lower()) != "default"
