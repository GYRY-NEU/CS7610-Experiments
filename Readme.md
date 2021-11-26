# Getting Started
```bash

git clone `project-experimentation`

cd `project-experimentation`
python3 -m venv env
source env/bin/activate
pip install setuptools-rust
pip install --upgrade pip
pip install fabric

```


# Project Structure
```bash
.
|
|
|__________main.py
|__________Experiments
          |
          |____experiment_1.py
          |____experiment_2.py
          |____...

```
# Run a experiment

```bash
# Warning your password stored in env variable.
# I dont have ways to access it, it will be deleted after you close the session
# But I suggest to change your password after or before to dummy password.
# Sorry for inconvience but it is required to simulated many machines in automated fashion.

    export MYKHOURYPASS=`yourkhourpass`

```
```bash
    python main.py `experiment_num`

```

# Experiment Info
## Experiment1 
- It simulates the basic case: 1 coordinator, 1 developer, 1 worker, 1 client
