#!/bin/bash
# This is expected to run inside one of the agent dirs
set -e
rm -rf wandb
export WANDB_AGENT_DISABLE_FLAPPING=true
exec wandb agent guytsky/sweeps-proj/$SWEEP_ID
