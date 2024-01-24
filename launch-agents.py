from datetime import datetime
import time
import subprocess
import sys
import os
from random import randint
import signal
from pathlib import Path
import shutil

shutil.rmtree('agents', ignore_errors=True)

def now():
    return datetime.now().isoformat()

num_agents = 4
outputs = []
for i in range(num_agents):
    os.makedirs(f'agents/agent_{i}', exist_ok=True)
    outputs.append(open(f'agents/agent_{i}/out.log', 'a'))

agents = [None] * num_agents
def launch_agent(i):
    proc = subprocess.Popen(
        [(Path(__file__).parent / 'wandb-agent.sh').absolute()],
        cwd = f'{os.getcwd()}/agents/agent_{i}',
        stdout = outputs[i],
        stderr = outputs[i],
    )
    agents[i] = proc
    print(f'{now()} Created agent {i} PID {proc.pid}')
    return proc

for i in range(num_agents):
    launch_agent(i)

stopped = False
def sighandler(signum, frame):
    print(f'{now()} Caught signal {signum}, stopping agents')
    stopped=True
    for proc in agents:
        proc.send_signal(signum)

signal.signal(signal.SIGTERM, sighandler)
signal.signal(signal.SIGINT, sighandler)

time.sleep(1)
while True:
    if stopped:
        [proc.wait() for proc in agents]
    
    if all([proc.poll() is not None for proc in agents]):
        print(f'{now()} All agents stopped: ', {p.pid: p.poll() for p in agents})
        break

    # Choose a random agent to preempt
    i = randint(0, len(agents) - 1)
    proc = agents[i]
    print(f'{now()} Interrupting agent {i} PID {proc.pid}')
    proc.send_signal(signal.SIGTERM)
    proc.wait()
    launch_agent(i)

    time.sleep(randint(20,40))