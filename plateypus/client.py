"""A client for interacting with the Plateypus backend."""

from requests import get, post


class PlateypusClient:
    """A client for interacting with the Plateypus backend."""

    def __init__(self, cfg):
        self.backend_url = cfg.get("BACKEND", "url")

    def search(self, terms):
        """Search for the given terms."""
        endpoint = f"{self.backend_url}/search"
        payload = dict(fields=terms)
        resp = post(endpoint, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Unexpected result: {resp.status_code} ({resp.json()})")
        return resp.json()

    def vehicle(self, vehicle_id):
        """Return details for the given vehicle."""
        endpoint = f"{self.backend_url}/vehicle/{vehicle_id}"
        resp = get(endpoint)
        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            raise RuntimeError(f"Unexpected server status: {resp.status_code}")
        return resp.json()
