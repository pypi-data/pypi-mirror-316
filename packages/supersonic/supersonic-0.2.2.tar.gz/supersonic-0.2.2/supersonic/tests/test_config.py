import pytest
from pydantic import ValidationError
from supersonic.core.config import SupersonicConfig, PRConfig, MergeStrategy


def test_pr_config_defaults():
    """Test PRConfig with default values"""
    config = PRConfig(title="Test PR")

    assert config.title == "Test PR"
    assert config.description is None
    assert config.base_branch == "main"
    assert config.draft is False
    assert config.labels == []
    assert config.reviewers == []
    assert config.team_reviewers == []
    assert config.merge_strategy == MergeStrategy.SQUASH
    assert config.delete_branch_on_merge is True
    assert config.auto_merge is False


def test_pr_config_custom():
    """Test PRConfig with custom values"""
    config = PRConfig(
        title="Custom PR",
        description="Test description",
        base_branch="develop",
        draft=True,
        labels=["bug", "feature"],
        reviewers=["user1", "user2"],
        team_reviewers=["team1"],
        merge_strategy=MergeStrategy.REBASE,
        delete_branch_on_merge=False,
        auto_merge=True,
    )

    assert config.title == "Custom PR"
    assert config.description == "Test description"
    assert config.base_branch == "develop"
    assert config.draft is True
    assert config.labels == ["bug", "feature"]
    assert config.reviewers == ["user1", "user2"]
    assert config.team_reviewers == ["team1"]
    assert config.merge_strategy == MergeStrategy.REBASE
    assert config.delete_branch_on_merge is False
    assert config.auto_merge is True


def test_pr_config_merge_strategy_validation():
    """Test merge strategy validation"""
    # Valid strategies
    PRConfig(title="Test", merge_strategy=MergeStrategy.MERGE)
    PRConfig(title="Test", merge_strategy=MergeStrategy.SQUASH)
    PRConfig(title="Test", merge_strategy=MergeStrategy.REBASE)

    # Invalid strategy
    with pytest.raises(ValidationError):
        PRConfig(title="Test", merge_strategy="invalid")


def test_supersonic_config_minimal():
    """Test SupersonicConfig with minimal required values"""
    config = SupersonicConfig(github_token="test-token")

    assert config.github_token == "test-token"
    assert config.base_url == "https://api.github.com"
    assert config.app_name is None
    assert isinstance(config.default_pr_config, PRConfig)


def test_supersonic_config_full():
    """Test SupersonicConfig with all values"""
    config = SupersonicConfig(
        github_token="test-token",
        base_url="https://github.example.com",
        app_name="test-app",
        default_pr_config=PRConfig(title="Default PR", base_branch="develop"),
    )

    assert config.github_token == "test-token"
    assert config.base_url == "https://github.example.com"
    assert config.app_name == "test-app"
    assert config.default_pr_config.title == "Default PR"
    assert config.default_pr_config.base_branch == "develop"


def test_supersonic_config_dict_initialization():
    """Test SupersonicConfig initialization from dict"""
    config_dict = {
        "github_token": "test-token",
        "app_name": "test-app",
        "default_pr_config": {"title": "Default PR", "labels": ["auto"]},
    }

    config = SupersonicConfig(**config_dict)
    assert config.github_token == "test-token"
    assert config.app_name == "test-app"
    assert config.default_pr_config.title == "Default PR"
    assert config.default_pr_config.labels == ["auto"]


def test_config_validation():
    """Test configuration validation"""
    # Missing required github_token
    with pytest.raises(ValidationError, match="github_token"):
        SupersonicConfig.model_validate({})


def test_pr_config_mutation():
    """Test that PR config lists are independent"""
    config1 = PRConfig(title="Test1")
    config2 = PRConfig(title="Test2")

    config1.labels.append("bug")
    assert config2.labels == []

    config1.reviewers.append("user1")
    assert config2.reviewers == []

    config1.team_reviewers.append("team1")
    assert config2.team_reviewers == []


def test_default_pr_config():
    """Test default PR configuration"""
    config = PRConfig()
    assert config.title == "Automated changes"
    assert config.base_branch == "main"
    assert config.draft is False
    assert config.labels == []
    assert config.reviewers == []
    assert config.team_reviewers == []
    assert config.merge_strategy == MergeStrategy.SQUASH
    assert config.delete_branch_on_merge is True
    assert config.auto_merge is False


def test_custom_pr_config():
    """Test custom PR configuration"""
    config = PRConfig(
        title="Test PR",
        description="Test description",
        base_branch="develop",
        draft=True,
        labels=["test"],
        reviewers=["user1"],
        team_reviewers=["team1"],
        merge_strategy=MergeStrategy.REBASE,
        delete_branch_on_merge=False,
        auto_merge=True,
    )
    assert config.title == "Test PR"
    assert config.description == "Test description"
    assert config.base_branch == "develop"
    assert config.draft is True
    assert config.labels == ["test"]
    assert config.reviewers == ["user1"]
    assert config.team_reviewers == ["team1"]
    assert config.merge_strategy == MergeStrategy.REBASE
    assert config.delete_branch_on_merge is False
    assert config.auto_merge is True


def test_supersonic_config_from_token():
    """Test creating config from token string"""
    config = SupersonicConfig(github_token="test-token")
    assert config.github_token == "test-token"
    assert config.base_url == "https://api.github.com"
    assert config.app_name is None
    assert isinstance(config.default_pr_config, PRConfig)


def test_supersonic_config_from_dict():
    """Test creating config from dictionary"""
    config = SupersonicConfig(
        github_token="test-token",
        base_url="https://github.enterprise.com/api/v3",
        app_name="test-app",
        default_pr_config={"title": "Custom Default", "draft": True},
    )
    assert config.github_token == "test-token"
    assert config.base_url == "https://github.enterprise.com/api/v3"
    assert config.app_name == "test-app"
    assert config.default_pr_config.title == "Custom Default"
    assert config.default_pr_config.draft is True
