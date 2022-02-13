import os
from os.path import join as _j
import pathlib
from functools import lru_cache
from zipfile import ZipFile
import requests

ROOT = pathlib.Path(__file__).parent.parent


class ResumeExtractor:

    def __init__(self, content, filename, id, root=ROOT, artifact_file="resume.pdf"):
        self.content = content
        self.filename = filename
        self.artifact_file = artifact_file

        self._store_path = _j(root, 'store', str(id))

    def _write_and_extract_zip(self):
        # Write the zip only if it doesn't exist.
        if not os.path.exists(self._store_path):
            os.makedirs(self._store_path)
            file = _j(self._store_path, f'{self.filename}.zip')

            # Write the zip file to disk
            with open(file, 'wb') as f:
                f.write(self.content)

            # Extract the zip file
            with ZipFile(file, 'r') as zip:
                zip.extractall(self._store_path)

            # Rename the extracted file
            os.rename(_j(self._store_path, self.artifact_file),
                      _j(self._store_path, f'{self.filename}.pdf'))

    def _get_pdf_version(self):
        with open(_j(self._store_path, 'version.txt'), 'r') as f:
            return f.read()[:-1]

    def get_pdf(self):
        self._write_and_extract_zip()
        pdf_path = _j(self._store_path, f'{self.filename}.pdf')
        return (f'{self.filename}.pdf', pdf_path, self._get_pdf_version())


@lru_cache(maxsize=None)
def get_resume_from_artifact():
    """
    Get a list of all artifacts for a given repo
    """
    owner = os.environ.get("REPO_OWNER")
    repo = os.environ.get("REPO_NAME")
    token = os.environ.get("GITHUB_PAT")

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    _r = requests.get(url, headers=headers)

    # The artifact we require from github
    artifact_name = "ResumeShaiqKar"
    # The api will return all the artifacts including the ones from github pages
    # We need to filter out the ones that are not the artifact we want.
    artifacts = [a for a in _r.json()['artifacts'] if a['name']
                 == artifact_name]
    #  Sort the filtered artifacts to get the latest one
    artifacts.sort(key=lambda item: item['created_at'], reverse=True)
    artifact = artifacts[0]
    response = requests.get(
        artifact['archive_download_url'], headers=headers, stream=True)

    # Write the artifact to disk and extract the pdf
    pdf_data = ResumeExtractor(response.content,
                               filename="ResumeShaiqKar", id=artifact['id']).get_pdf()

    return pdf_data
