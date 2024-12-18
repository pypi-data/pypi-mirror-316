from typing import Optional, List
import aiohttp
from github import Github, Auth

from .errors import GitHubError


class GitHubAPI:
    """Wrapper for GitHub API operations"""

    def __init__(self, token: str, base_url: Optional[str] = None):
        """Initialize GitHub API client"""
        self.token = token
        self.base_url = base_url or "https://api.github.com"
        self.github = Github(auth=Auth.Token(token), base_url=self.base_url)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"token {self.token}",
                    "Accept": "application/vnd.github.v3+json",
                }
            )
        return self._session

    async def create_branch(
        self, repo: str, branch: str, base_branch: str = "main"
    ) -> None:
        """Create a new branch from base branch"""
        try:
            repo_obj = self.github.get_repo(repo)
            base_ref = repo_obj.get_git_ref(f"heads/{base_branch}")

            try:
                repo_obj.create_git_ref(
                    ref=f"refs/heads/{branch}", sha=base_ref.object.sha
                )
            except Exception as e:
                if "Reference already exists" in str(e):
                    # Update existing branch
                    branch_ref = repo_obj.get_git_ref(f"heads/{branch}")
                    branch_ref.edit(base_ref.object.sha, force=True)
                else:
                    raise
        except Exception as e:
            raise GitHubError(f"Failed to create branch: {e}")

    async def update_file(
        self, repo: str, path: str, content: Optional[str], message: str, branch: str
    ) -> None:
        """Update or delete a file in the repository"""
        try:
            repo_obj = self.github.get_repo(repo)

            if content is None:
                # Delete file
                try:
                    contents = repo_obj.get_contents(path, ref=branch)
                    if isinstance(contents, List):
                        raise GitHubError(f"Path '{path}' points to a directory")
                    repo_obj.delete_file(
                        path=path, message=message, sha=contents.sha, branch=branch
                    )
                except Exception as e:
                    if "Not Found" not in str(e):
                        raise
            else:
                # Update or create file
                try:
                    contents = repo_obj.get_contents(path, ref=branch)
                    if isinstance(contents, List):
                        raise GitHubError(f"Path '{path}' points to a directory")
                    repo_obj.update_file(
                        path=path,
                        message=message,
                        content=content,
                        sha=contents.sha,
                        branch=branch,
                    )
                except Exception as e:
                    if "Not Found" in str(e):
                        repo_obj.create_file(
                            path=path, message=message, content=content, branch=branch
                        )
                    else:
                        raise
        except Exception as e:
            raise GitHubError(f"Failed to update file: {e}")

    async def create_pull_request(
        self,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str,
        draft: bool = False,
    ) -> str:
        """Create a pull request"""
        try:
            repo_obj = self.github.get_repo(repo)
            pr = repo_obj.create_pull(
                title=title, body=body, head=head, base=base, draft=draft
            )
            return pr.html_url
        except Exception as e:
            raise GitHubError(f"Failed to create pull request: {e}")

    async def add_labels(self, repo: str, pr_number: int, labels: List[str]) -> None:
        """Add labels to a pull request"""
        try:
            repo_obj = self.github.get_repo(repo)
            pr = repo_obj.get_pull(pr_number)
            pr.add_to_labels(*labels)
        except Exception as e:
            raise GitHubError(f"Failed to add labels: {e}")

    async def add_reviewers(
        self, repo: str, pr_number: int, reviewers: List[str]
    ) -> None:
        """Add reviewers to a pull request"""
        try:
            repo_obj = self.github.get_repo(repo)
            pr = repo_obj.get_pull(pr_number)
            pr.create_review_request(reviewers=reviewers)
        except Exception as e:
            raise GitHubError(f"Failed to add reviewers: {e}")

    async def enable_auto_merge(
        self, repo: str, pr_number: int, merge_method: str = "squash"
    ) -> None:
        """Enable auto-merge for a pull request"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}/auto_merge"

            async with session.put(
                url, json={"merge_method": merge_method}
            ) as response:
                if response.status not in (200, 201):
                    text = await response.text()
                    raise GitHubError(f"Failed to enable auto-merge: {text}")
        except Exception as e:
            raise GitHubError(f"Failed to enable auto-merge: {e}")
