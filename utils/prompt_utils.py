import importlib.resources

import os
import sys

# Find the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Add the root directory to sys.path if it's not already there
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


def load_prompt(prompt):
    system_prompts_dir = os.path.join(root_dir, "hackbot", "system_prompts")
    os.makedirs(system_prompts_dir, exist_ok=True)

    full_path = os.path.join(system_prompts_dir, f"{prompt}.txt")

    try:
        file_path = str(full_path)
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")
        with open(file_path, "r") as fp:
            return fp.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {full_path}")


def obs_dict_of_last_event(events, obs_descriptor):
    obs_dict = {}
    for key, description, state_type in obs_descriptor:
        value = events[-1][1][key]
        obs_dict[key] = f"{description}{value}\n\n"
    return obs_dict
