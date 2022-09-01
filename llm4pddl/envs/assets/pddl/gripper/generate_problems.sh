#!/usr/bin/env bash

# See https://github.com/AI-Planning/pddl-generators
PATH_TO_PDDL_GEN="${HOME}/phd/pddl-generators"
GRIPPER_GEN=${PATH_TO_PDDL_GEN}/gripper/gripper
OUT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TRAIN_MULTIPLIER=4
EVAL_MULTIPLIER=4

# Train problems
for i in {1..1};
do
N=$(($i*$TRAIN_MULTIPLIER))
$GRIPPER_GEN -n $N > "${OUT_DIR}/task${i}.pddl"
done

# Eval problems
for i in {2..20};
do
N=$(($i*$EVAL_MULTIPLIER))
$GRIPPER_GEN -n $N > "${OUT_DIR}/task${i}.pddl"
done
