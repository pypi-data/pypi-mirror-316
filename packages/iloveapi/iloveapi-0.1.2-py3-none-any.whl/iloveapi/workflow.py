from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from iloveapi.iloveapi import ILoveApi


class Workflow:
    def __init__(self, client: ILoveApi) -> None:
        self.client = client

    def compressimage(self, file: str | Path) -> None:
        task_response = self.client.rest.start("compressimage")
        task_response.raise_for_status()
        task_json = task_response.json()
        server = task_json["server"]
        task_id = task_json["task"]

        upload_response = self.client.rest.upload(server, task_id, file)
        upload_json = upload_response.json()
        server_filename = upload_json["server_filename"]

        process_response = self.client.rest.process(
            server,
            task_id,
            "compressimage",
            [{"server_filename": server_filename, "filename": file}],
        )

        download_response = self.client.rest.download(server, task_id)
