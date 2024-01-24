from tqdm import tqdm
import wandb
from random import random
import time
from pathlib import Path
import os
import signal

existing_run_id = os.environ.get('WANDB_RUN_ID')
print('WANDB env: ', {k:v for k,v in os.environ.items() if k.startswith('WANDB')})
if existing_run_id:
    print('Existing run ID')
else:
    print('New run ID')
wandb.init(resume=existing_run_id is not None)

print('Wandb run id: ', wandb.run.id)
print('Wandb config: ', wandb.config)
print('Wandb run step: ', wandb.run.step)

ckpt_path = Path(__file__).parent / 'ckpts' / wandb.run.id
os.makedirs(ckpt_path.parent, exist_ok=True)
if ckpt_path.exists():
    print('Continuing from checkpoint')
else:
    print('New checkpoint')
    ckpt_path.touch()

def sighandler(signum, frame):
    print(f'{datetime.now().isoformat()} Caught signal {signum}, quitting')
    wandb.mark_preempting()
    sys.exit(42)
signal.signal(signal.SIGTERM, sighandler)
signal.signal(signal.SIGINT, sighandler)

max_steps = 10000
start_step = wandb.run.step or 0

for i in tqdm(range(start_step, max_steps), initial=start_step, total=max_steps):
    # Noisy version of 1/x
    metric = (1 / ((i + 1) * wandb.config.x_scaling_factor)) * random()
    wandb.log({'loss': metric})
    time.sleep(0.01)