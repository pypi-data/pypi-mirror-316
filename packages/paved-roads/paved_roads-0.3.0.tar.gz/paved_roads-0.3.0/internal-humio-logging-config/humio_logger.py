import logging
import requests
import json

class HumioLogger:
    def __init__(self, humio_url, token=None):
        """
        Initialize the Humio Logger.

        Args:
            humio_url (str): The Humio API endpoint.
            token (str): The Humio API token for authentication.
        """
        self.humio_url = humio_url
        self.token = token

    def send_log(self, level, message, tags=None, fields=None):
        """
        Send a log message to Humio.

        Args:
            level (str): Log level (e.g., 'INFO', 'ERROR').
            message (str): Log message.
            tags (dict): Tags to attach to the log (optional).
            fields (dict): Additional fields for context (optional).
        """
        if not self.humio_url:
            raise ValueError("Humio URL is not configured.")

        log_entry = {
            "tags": tags or {},
            "events": [
                {
                    "timestamp": self._get_iso_timestamp(),
                    "level": level,
                    "message": message,
                    "fields": fields or {},
                }
            ]
        }

        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = requests.post(
                self.humio_url,
                headers=headers,
                data=json.dumps(log_entry),
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send log to Humio: {e}")
            raise

    def _get_iso_timestamp(self):
        """Helper function to generate an ISO 8601 timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"

# Global logger instance for convenience
_humio_logger = None

def configure_humio_logger(humio_url, token=None):
    """
    Configure the global Humio logger.

    Args:
        humio_url (str): The Humio API endpoint.
        token (str): The Humio API token for authentication.
    """
    global _humio_logger
    _humio_logger = HumioLogger(humio_url, token)

def log_to_humio(level, message, tags=None, fields=None):
    """
    Send a log to Humio using the global logger.

    Args:
        level (str): Log level (e.g., 'INFO', 'ERROR').
        message (str): Log message.
        tags (dict): Tags to attach to the log (optional).
        fields (dict): Additional fields for context (optional).
    """
    if not _humio_logger:
        raise RuntimeError("Humio logger is not configured. Call configure_humio_logger first.")
    _humio_logger.send_log(level, message, tags, fields)

