from collections.abc import Iterable

from conda import plugins

from .history_d import update_history_d


@plugins.hookimpl
def conda_post_commands() -> Iterable[plugins.CondaPostCommand]:
    """Plugin that records a details history for all environments in conda-meta/history.d"""
    yield plugins.CondaPostCommand(
        name="conda-history-d",
        action=update_history_d,
        run_for={
            "create",
            "install",
            "remove",
            "uninstall",
            "update",
            "upgrade",
            "env_create",
            "env_remove",
            "env_update",
        },
    )
