"""Launch script for openstack experiments.

Requires a file that contains a list of IP addresses for instances that are:
    - Turned on
    - Accessible via ssh for the user of this file
    - Configured with the llm4pddl image
    - Sufficient in number to run all of the experiments in the config file

Usage example:
    python scripts/launch_openstack.py --config scripts/configs/example.yaml \
        --machines machines.txt --sshkey ~/.ssh/cloud.key

The default branch can be overridden with the --branch flag.

To run all commands on one machine, in sequence, rather than across multiple
machines in parallel, use --single_machine. The first machine in machines.txt
will be used.
"""

import argparse
import os

from cluster_utils import DEFAULT_BRANCH, SingleSeedRunConfig, \
    config_to_cmd_flags, config_to_logfile, generate_run_configs, \
    get_cmds_to_prep_repo, run_cmds_on_machine


def _main() -> None:
    # Set up argparse.
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=str)
    parser.add_argument("--machines", required=True, type=str)
    parser.add_argument("--sshkey", required=True, type=str)
    parser.add_argument("--branch", type=str, default=DEFAULT_BRANCH)
    parser.add_argument("--single_machine", action="store_true")
    args = parser.parse_args()
    # Load the machine IPs.
    with open(args.machines, "r", encoding="utf-8") as f:
        machines = f.read().splitlines()
    # Make sure that the ssh key exists.
    assert os.path.exists(args.sshkey)
    # Generate all of the run configs and make sure that we have enough
    # machines to run them all.
    run_configs = list(generate_run_configs(args.config))
    num_machines = len(machines)
    if not args.single_machine:
        assert num_machines >= len(run_configs)
    else:
        assert num_machines >= 1
    # Prepare the commands.
    cmds = ["cd ~/llm4pddl"] + get_cmds_to_prep_repo(args.branch)
    main_cmds = []
    for cfg in run_configs:
        assert isinstance(cfg, SingleSeedRunConfig)
        logfile = os.path.join("logs", config_to_logfile(cfg))
        cmd_flags = config_to_cmd_flags(cfg)
        cmd = f"python3.8 llm4pddl/main.py {cmd_flags} &> {logfile}"
        main_cmds.append(cmd)
    # Launch across multiple machines.
    if not args.single_machine:
        for machine, machine_main_cmd in zip(machines, main_cmds):
            print(f"Launching on machine {machine}: {machine_main_cmd}")
            background_cmd = machine_main_cmd + " &"
            machine_cmds = cmds + [background_cmd]
            run_cmds_on_machine(machine_cmds,
                                "ubuntu",
                                machine,
                                ssh_key=args.sshkey)
    # Launch sequentially on one machine.
    else:
        machine = machines[0]
        sequential_cmd = "{ " + ("; ".join(main_cmds)) + "; } &"
        print(f"Launching on machine {machine}: {sequential_cmd}")
        machine_cmds = cmds + [sequential_cmd]
        run_cmds_on_machine(machine_cmds,
                            "ubuntu",
                            machine,
                            ssh_key=args.sshkey)


if __name__ == "__main__":
    _main()
