"""Updating conda-meta/history.d directory."""

from datetime import datetime
from pathlib import Path

from conda.base.context import context
from conda.history import History

from conda.core.prefix_data import PrefixData
from conda.models.records import PrefixRecord
from conda.models.records import PackageRecord
from conda.gateways.disk.create import create_hard_link_or_copy, write_as_json_to_file
from conda.gateways.disk.delete import rm_rf
from conda.gateways.disk.link import symlink


HISTORY_D_STATE_PATH_TEMPLATE = "{prefix}/conda-meta/history.d/{timestamp}"
HISTORY_D_LATEST_PATH_TEMPLATE = "{prefix}/conda-meta/history.d/latest"


def update_history_d(_command: str) -> None:
    target_prefix = context.target_prefix
    history = History(prefix=target_prefix)

    states = history.construct_states()
    current_dt = datetime.fromisoformat(states[-1][0])
    timestamp = current_dt.strftime("%Y-%m-%d-%H-%M-%S")
    history_d_state_path = Path(
        HISTORY_D_STATE_PATH_TEMPLATE.format(
            prefix=target_prefix,
            timestamp=timestamp,
        )
    )
    history_d_latest_path = Path(
        HISTORY_D_LATEST_PATH_TEMPLATE.format(prefix=target_prefix)
    )
    history_d_subdir_path = history_d_state_path / context.subdir

    if history_d_subdir_path.exists():
        return

    history_d_subdir_path.mkdir(parents=True, exist_ok=True)

    prefixdata = PrefixData(prefix_path=target_prefix, pip_interop_enabled=False)
    prefix_record: PrefixRecord
    for prefix_record in prefixdata.iter_records():
        history_d_record_path = history_d_subdir_path / prefixdata._get_json_fn(
            prefix_record
        )
        extracted_package_dir = Path(prefix_record.extracted_package_dir)
        repodata_record_path = extracted_package_dir / "info" / "repodata_record.json"
        if repodata_record_path.exists():
            create_hard_link_or_copy(repodata_record_path, history_d_record_path)
        else:
            package_record = PackageRecord.from_objects(prefix_record)
            write_as_json_to_file(history_d_record_path, package_record)

    rm_rf(history_d_latest_path)
    symlink(history_d_state_path, history_d_latest_path)

    # TODO record additional metadata about state of the environment
