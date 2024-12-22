from logging import exception

import requests


class Image:
    _name: str
    _tag: str
    _digest: str

    def __init__(self, full_name: str):
        # image can also be specified with @ followed by digest hash
        # eg- "FROM node@abhst2783dhu"
        # https://docs.docker.com/reference/dockerfile/#from
        if "@" in full_name:
            components = full_name.split("@")
            self._name = full_name.split("@")[0]
            self._digest = (
                components[1]
                if len(components) > 1
                else self.get_image_digest("latest")
            )
        else:
            components = full_name.split(":")
            self._name = components[0]
            self._tag = components[1] if len(components) > 1 else "latest"

    def name(self) -> str:
        return self._name

    def tag(self) -> str:
        return self._tag

    def digest(self) -> str:
        return self._digest

    def full_name(self) -> str:
        return f"{self._name}:{self._tag}"

    def is_alpine_or_slim(self) -> bool:
        """
        Returns true if the image is a light one, ie, either alpine or slim
        """
        return "alpine" in self._tag or "slim" in self._tag

    def full_name_with_digest(self) -> str:
        return f"{self._name}@{self._digest}"

    def get_image_digest(self, tag) -> str:
        base_url = (
            f"https://registry-1.docker.io/v2/library/{self._name}/manifests/{tag}"
        )
        headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
        try:
            response = requests.head(base_url, headers=headers)
            if response.status_code == 200:
                return response.headers.get("Docker-Content-Digest", "Digest not found")
            elif response.status_code == 404:
                return "Image or tag not found"
            elif response.status_code == 401:
                return "Authentication required. Please log in to Docker Hub."
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
