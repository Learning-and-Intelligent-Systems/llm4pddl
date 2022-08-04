"""Script for killing all active openstack experiments.

WARNING: any other python3.8 processes running on the machine will also be
killed (but there typically shouldn't be any).

See launch.py for information about the format of machines.txt.

Usage example:
    python scripts/kill_openstack.py --machines machines.txt \
        --sshkey ~/.ssh/cloud.key
"""

import argparse
import os

from cluster_utils import run_cmds_on_machine


def _main() -> None:
    # Set up argparse.
    parser = argparse.ArgumentParser()
    parser.add_argument("--machines", required=True, type=str)
    parser.add_argument("--sshkey", required=True, type=str)
    args = parser.parse_args()
    with open(args.machines, "r", encoding="utf-8") as f:
        machines = f.read().splitlines()
    # Make sure that the ssh key exists.
    assert os.path.exists(args.sshkey)
    # Loop through each machine and kill the python3.8 process.
    kill_cmd = "pkill -9 python3.8"
    for machine in machines:
        print(f"Killing machine {machine}")
        # Allow return code 1, meaning that no process was found to kill.
        run_cmds_on_machine([kill_cmd],
                            "ubuntu",
                            machine,
                            ssh_key=args.sshkey,
                            allowed_return_codes=(0, 1))


if __name__ == "__main__":
    _main()
