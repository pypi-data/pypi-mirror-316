'''
file specifies premises, conclusions, and settings.
running the file finds a model and prints the result.
'''

import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from string import Template
import argparse
import importlib.util
from threading import (
    Thread,
    Event,
)
import time
from tqdm import tqdm
# import warnings
# import cProfile
# import pstats

# didn't work
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Get the directory path of the current file
# current_dir = os.path.dirname(__file__)
# # Construct the full path to your project root
# project_root = os.path.abspath(os.path.join(current_dir, ".."))
# # project_root = project_root[:-4] # bandaid fix to remove "/src" from the root
# # Add the project root to the Python path
# sys.path.append(project_root)

### FOR TESTING ###
from __init__ import __version__
from model_structure import (
    StateSpace,
    make_model_for,
    )

# ### FOR PACKAGING ###
# from model_checker.__init__ import __version__
# from model_checker.model_structure import (
#     StateSpace,
#     make_model_for,
#     )

script_template = Template("""
'''
Model Checker: ${name}
'''
import os
parent_directory = os.path.dirname(__file__)
file_name = os.path.basename(__file__)

################################
########## SETTINGS ############
################################

# time cutoff for increasing N
max_time = 1

# find a countermodel with the smallest value of N within max_time
optimize_bool = False

# print all Z3 constraints if a model is found
print_constraints_bool = False

# print all states including impossible states
print_impossible_states_bool = False

# present option to append output to file
save_bool = False


################################
############ SYNTAX ############
################################

### SENTENCES ###

# 'A', 'B', 'C',... can be used for sentence letters

# Alternatively, 'RedBall', 'MarySings',... or 'red_ball', 'mary_sings',... can be used for sentence letters.

# 'top' is a designated sentence for the trivial truth verified by everything and falsified by nothing.


### UNARY OPERATORS ###

# Negation: 'neg', e.g., 'neg A'.
# Necessity: 'Box', e.g., 'Box A'.
# Possibility: 'Diamond', e.g., 'Diamond A'. 

# NOTE: parentheses must not be included for unary operators.


### BINARY OPERATORS ###

# Conjunction: 'wedge', e.g., '(A wedge B)'
# Disjunction: 'vee', e.g., '(A vee B)'
# Conditional: 'rightarrow', e.g., '(A rightarrow B)'
# Biconditional: 'leftrightarrow', e.g., '(A leftrightarrow B)'
# Must Counterfactual: 'boxright', e.g., '(A boxright B)'
# Might Counterfactual: 'circright', e.g., '(A circright B)'
# Ground: 'leq', e.g., '(A leq B)'
# Essece: 'sqsubseteq', e.g., '(A sqsubseteq B)'
# Propositional Identity: 'equiv', e.g., '(A equiv B)'
# Relevance: 'preceq', e.g., '(A preceq B)'

# NOTE: parentheses must always be included for binary operators.


################################
########## ARGUMENTS ###########
################################

# NOTE: Additional examples can be found at: https://github.com/benbrastmckie/ModelChecker/tree/master/Examples

### INVALID ###

premises = ['neg A','(A boxright (B vee C))']
conclusions = ['(A boxright B)','(A boxright C)']
N = 3 # number of atomic states
contingent_bool = False # make all propositions contingent
disjoint_bool = False # make all propositions have disjoint subject-matters

### VALID ###

# premises = ['((A vee B) boxright C)']
# conclusions = ['(A boxright C)']
# N = 3 # number of atomic states
# contingent_bool = False # make all propositions contingent
# disjoint_bool = False # make all propositions have disjoint subject-matters

""")

class BuildModule:
    """load module and store values as a class"""
    def __init__(self, module_name, module_path):
        self.module_name = module_name
        self.module_path = module_path
        self.default_values = {
            "N": 3,
            "premises": [],
            "conclusions": [],
            "max_time": 1,
            "contingent_bool": False,
            "disjoint_bool": False,
            "optimize_bool": False,
            "print_constraints_bool": False,
            "print_impossible_states_bool": False,
            "save_bool": False,
        }
        self.parent_file = None
        self.parent_directory = None
        self.N = self.default_values["N"]
        self.premises = self.default_values["premises"]
        self.conclusions = self.default_values["conclusions"]
        self.max_time = self.default_values["max_time"]
        self.contingent_bool = self.default_values["contingent_bool"]
        self.disjoint_bool = self.default_values["disjoint_bool"]
        self.optimize_bool = self.default_values["optimize_bool"]
        self.print_constraints_bool = self.default_values["print_constraints_bool"]
        self.print_impossible_states_bool = self.default_values["print_impossible_states_bool"]
        self.save_bool = self.default_values["save_bool"]
        self.module = self.load_module()
        self.initialize_attributes()
        self.validate_attributes()

    def load_module(self):
        """prepares a test file, raising a error if unsuccessful."""
        try:
            spec = importlib.util.spec_from_file_location(self.module_name, self.module_path)
            if spec is None or spec.loader is None:
                raise ImportError("Module spec could not be loaded.")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            raise ImportError(f"Failed to load the module '{self.module_name}': {e}") from e

    def initialize_attributes(self):
        """stores all user settings included in a test file."""
        self.parent_file = getattr(self.module, "file_name", True)
        self.parent_directory = getattr(self.module, "parent_directory", True)
        self.N = getattr(self.module, "N", self.default_values["N"])
        self.premises = getattr(self.module, "premises", self.default_values["premises"])
        self.conclusions = getattr(self.module, "conclusions", self.default_values["conclusions"])
        self.max_time = float(getattr(self.module, "max_time", self.default_values["max_time"]))
        self.contingent_bool = getattr(
            self.module,
            "contingent_bool",
            self.default_values["contingent_bool"]
        )
        self.disjoint_bool = getattr(
            self.module,
            "disjoint_bool",
            self.default_values["disjoint_bool"]
        )
        self.optimize_bool = getattr(
            self.module,
            "optimize_bool",
            self.default_values["optimize_bool"]
        )
        self.print_constraints_bool = getattr(
            self.module,
            "print_constraints_bool",
            self.default_values["print_constraints_bool"]
        )
        self.print_impossible_states_bool = getattr(
            self.module,
            "print_impossible_states_bool",
            False
        )
        self.save_bool = getattr(self.module, "save_bool", True)
        # self.all_constraints = getattr(self.module, "all_constraints", [])

    def update_max_time(self, new_max_time):
        self.max_time = new_max_time

    def validate_attributes(self):
        for attr, default_value in self.default_values.items():
            if not hasattr(self.module, attr):
                print(f"The value of '{attr}' is absent and has been set to {default_value}.")
                # raise ImportError(f"The value of '{attr}' is absent")

def parse_file_and_flags():
    """returns the name and path for the current script"""
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        prog='model-checker',
        usage='%(prog)s [options] input',
        description="""
        Running '%(prog)s' without options or an input will prompt the user
        to generate a new test file. To run a test on an existing file, include
        the path to that file as the input.""",
        epilog="""
        More information can be found at:
        https://github.com/benbrastmckie/ModelChecker/""",
    )
    parser.add_argument(
        "file_path",
        nargs='?',
        default=None,
        type=str,
        help="Specifies the path to a Python.",
    )
    parser.add_argument(
        '--contingent',
        '-c',
        action='store_true',
        help='Overrides to make all propositions contingent.'
    )
    parser.add_argument(
        '--disjoint',
        '-d',
        action='store_true',
        help='Overrides to make all propositions have disjoint subject-matters.'
    )
    parser.add_argument(
        '--print',
        '-p',
        action='store_true',
        help='Overrides to print the Z3 constraints or else the unsat_core constraints if there is no model.'
    )
    parser.add_argument(
        '--save',
        '-s',
        action='store_true',
        help='Overrides to prompt user to save output.'
    )
    parser.add_argument(
        '--impossible',
        '-i',
        action='store_true',
        help='Overrides to print impossible states.'
    )
    parser.add_argument(
        '--version',
        '-v',
        action='version',
        version=f"%(prog)s:  {__version__}",
        help='Prints the version number.'
    )
    parser.add_argument(
        '--optimize',
        '-o',
        action='store_true',
        help='finds the minimum value for N that is satisfiable before reaching max_time.'
    )
    parser.add_argument(
        '--upgrade',
        '-u',
        action='store_true',
        help='Upgrade the package.'
    )
    # parse the command-line argument to get the module path
    args = parser.parse_args()
    package_name = parser.prog  # Get the package name from the parser
    return args, package_name

def generate_test(name):
    """check if a script name was provided"""
    template_data = {
        'name': name
    }
    script_content = script_template.substitute(template_data)
    output_file_path = f'{name}.py'
    with open(output_file_path, 'w', encoding="utf-8") as f:
        f.write(script_content)
    print(f"\nThe {name}.py file has been created.")
    print("You can run this file with the command:\n")
    print(f"model-checker {name}.py\n")

def ask_generate_test():
    """prompt user to create a test file"""
    result = input("Would you like to generate a new test file? (y/n): ")
    if result in {'Yes', 'yes', 'y', 'Y'}:
        test_name = input("Enter the name of your test using snake_case: ")
        generate_test(test_name)
        return
    print("You can run a test.py file that already exists with the command:\n")
    print("model-checker test.py\n")

def ask_save():
    """print the model and prompt user to store the output"""
    result = input("Would you like to save the output? (y/n):\n")
    if not result in ['Yes', 'yes', 'y']:
        return None, None
    cons_input = input("\nWould you like to include the Z3 constraints? (y/n):\n")
    print_cons = bool(cons_input in ['Yes', 'yes', 'y'])
    file_name = input(
        "\nEnter the file name in snake_case without an extension.\n"
        "Leave the file name blank to append the output to the project file.\n"
        "\nFile name:\n"
    )
    return file_name, print_cons

def ask_time(runtime, max_time):
    """prompt the user to increase the max_time"""
    output = input(f"Enter a value for max_time > {max_time} or leave blank to exit.\n\nmax_time = ")
    if output.strip() == "":
        return None
    try:
        new_max_time = float(output)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return ask_time(runtime, max_time)
    if not new_max_time > max_time:
        print("Invalid input. Please enter a valid number.")
        return ask_time(runtime, max_time)
    return new_max_time


def no_model_save_or_append(module, model_structure, file_name):
    """option to save or append if no model is found"""
    if len(file_name) == 0:
        with open(f"{module.module_path}", 'a', encoding="utf-8") as f:
            print('\n"""', file=f)
            model_structure.no_model_print(module.print_cons, f)
            print('"""', file=f)
        return
    with open(f"{module.parent_directory}/{file_name}.py", 'w', encoding="utf-8") as n:
        print(f'# TITLE: {file_name}.py generated from {module.parent_file}\n"""', file=n)
        model_structure.no_model_save(module.print_constraints_bool, n)
    print()

def save_or_append(module, model_setup, file_name, print_cons, print_imposs):
    """option to save or append if a model is found"""
    if len(file_name) == 0:
        with open(f"{module.module_path}", 'a', encoding="utf-8") as f:
            print('\n"""', file=f)
            model_setup.print_to(print_cons, print_imposs, f)
            print('"""', file=f)
        return
    with open(f"{module.parent_directory}/{file_name}.py", 'w', encoding="utf-8") as n:
        print(f'# TITLE: {file_name}.py generated from {module.parent_file}\n"""', file=n)
        model_setup.save_to(print_cons, print_imposs, n)
    print()

def adjust(module, offset):
    """Redefines module and model_setup after adjusting N by the offset."""
    module.N += offset
    model_setup = make_model_for(
        module.N,
        module.premises,
        module.conclusions,
        module.max_time,
        module.contingent_bool,
        module.disjoint_bool,
    )
    return module, model_setup

def optimize_N(module, model_setup, past_module, past_model_setup, sat=False):
    """Finds the min value of N for which there is a model up to a timeout limit."""
    if model_setup.model_status: # finds a model
        new_sat = True
        new_module, new_model_setup = adjust(module, -1)
        min_module, min_model_setup = optimize_N(
            new_module,
            new_model_setup,
            module,
            model_setup,
            new_sat
        )
        return min_module, min_model_setup
    if sat: # does not find a model but has before (hence sat = True)
        return past_module, past_model_setup
    if model_setup.model_runtime < model_setup.max_time: # hasn't found a model yet
        new_module, new_model_setup = adjust(module, 1)
        max_module, max_model_setup = optimize_N(
            new_module,
            new_model_setup,
            module,
            model_setup,
            sat
        )
        return max_module, max_model_setup
    handle_timeout(module, model_setup)
    return run_optimization_with_progress(module)


def create_model_setup(module):
    """Creates a model setup based on module attributes."""
    return make_model_for(
        module.N,
        module.premises,
        module.conclusions,
        module.max_time,
        module.contingent_bool,
        module.disjoint_bool,
    )

def handle_timeout(module, model_setup):
    """Handles timeout scenarios by asking the user for a new time limit."""
    previous_N = model_setup.N - 1
    print(f"There are no {previous_N}-models.")
    print(f"No {model_setup.N}-models were found within {model_setup.model_runtime} seconds.")
    new_max_time = ask_time(model_setup.model_runtime, model_setup.max_time)
    if new_max_time is None:
        print("Process terminated.")
        print(f"Consider increasing max_time to be > {model_setup.max_time} seconds.\n")
        model_setup.N = previous_N
        model_setup.no_model_print(module.print_constraints_bool)
        os._exit(1)
    module.update_max_time(new_max_time)

def optimize_model_setup(module):
    """Runs make_model_for on the values provided by the module and user, optimizing if required."""
    max_time = module.max_time
    model_setup = create_model_setup(module)
    run_time = model_setup.model_runtime
    if run_time > max_time:
        handle_timeout(module, model_setup)
        module, model_setup = run_optimization_with_progress(module)
    if module.optimize_bool:
        module, model_setup = optimize_N(module, model_setup, module, model_setup)
    return module, model_setup

def show_progress_bar(max_time, optimize_future):
    """Show progress bar for how much of max_time has elapsed."""
    padding = 0 # setting this to 5 makes for strange results
    step_time = (max_time + padding) / 100
    with tqdm(
        desc=f"Searching for {max_time} seconds: ",
        total=100,
        unit="step",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    ) as pbar:
        for _ in range(100):
            if optimize_future.done():
                # pbar.update(100 - pbar.n) # makes the progress bar complete
                break
            time.sleep(step_time)
            pbar.update(1)

def run_optimization_with_progress(module):
    """Main function: Creates, optimizes (if needed), and manages model setup process."""
    with ThreadPoolExecutor() as executor:
        optimize_future = executor.submit(optimize_model_setup, module)
        # optimize_progress = executor.submit(show_progress_bar, module.max_time, optimize_future)
        show_progress_bar(module.max_time, optimize_future)
        try:
            module, model_setup = optimize_future.result()
        except Exception as e:
            print(f"Error during optimization: {e}")
            raise
    return module, model_setup

### BEGIN ALTERNATIVES ###

# def progress_bar(optimize_future, max_time):
#     """Simulate a progress bar that runs until future is done."""
#     start_time = time.time()
#     step_time = max_time / 100
#     while optimize_future.running():
#         elapsed_time = time.time() - start_time
#         print(f"Progress: {elapsed_time:.2f}/{max_time:.2f} seconds", end='\r')
#         time.sleep(step_time)  # Update progress every 0.1 second
#         # if elapsed_time >= max_time:
#         if optimize_future.done():
#             break
#     # print("\nProgress bar stopped.")

# def progress_bar(max_time, stop_event):
#     """Show progress bar for how much of max_time has elapsed."""
#     padding = 0
#     step_time = (max_time + padding) / 100
#     step_num = 0
#     with tqdm(
#         desc=f"Searching for {max_time} seconds: ",
#         total=100,
#         unit="step",
#         bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
#     ) as pbar:
#         while not stop_event.is_set() and pbar.n < 100:
#             step_num =+ 1
#             if pbar.n < 50:
#                 time.sleep(step_time) # NOTE: gives bad result if multiplied by 4
#                 pbar.update(1)
#             if pbar.n < 70:
#                 time.sleep((step_time * 100) / (100 - step_num)) # NOTE: gives bad result if multiplied by 4
#                 pbar.update(1)
#             time.sleep((step_time * 200) / (100 - step_num)) # NOTE: gives bad result if multiplied by 4
#             pbar.update(1)

# def progress_bar(max_time, stop_event):
#     """Simulate a progress bar that runs until stop_event is set."""
#     start_time = time.time()
#     step_time = max_time / 100
#     while not stop_event.is_set():
#         elapsed_time = time.time() - start_time
#         print(f"Progress: {elapsed_time:.2f}/{max_time:.2f} seconds", end='\r')
#         time.sleep(step_time)  # Update progress every 0.1 second
#         if elapsed_time >= max_time:
#             break
#     # print("\nProgress bar stopped.")

# def run_optimization_with_progress(module):
#     """Run the optimization process and progress bar in parallel."""
#     stop_event = Event()
#     progress_thread = Thread(target=progress_bar, args=(module.max_time, stop_event))
#     progress_thread.start()
#
#     # Run optimize_model_setup in the main thread
#     module, model_setup = optimize_model_setup(module)
#
#     stop_event.set()  # Signal the progress bar to stop
#     progress_thread.join()  # Wait for the progress bar thread to finish
#     return module, model_setup

# def show_progress_bar(thread, max_time):
#     with tqdm(total=100, desc="Optimizing model setup") as pbar:
#         while thread.is_alive():
#             pbar.update(1)
#             time.sleep(0.05)
#         pbar.update(pbar.total - pbar.n)  # Ensure the progress bar completes

# def run_optimization_with_progress(module):
#     """Run the optimization process and progress bar in parallel."""
#     optimize_thread = Thread(target=optimize_model_setup, args=(module,))
#     optimize_thread.start()
#     # Show the progress bar until the optimization is complete
#     show_progress_bar(optimize_thread, module.max_time)
#     return optimize_thread

# ### still has delay; consider timing how long the total search process takes
# # def optimize_if_needed(module, model_setup, optimize_model):
# #     """Optimizes the model setup if optimization is enabled."""
# #     if optimize_model:
# #         return optimize_N(module, model_setup, module, model_setup)
# #     return module, model_setup
#
# def create_and_optimize(module, optimize_model, print_cons):
#     """Runs make_model_for on the values provided by the module and user, optimizing if required."""
#
#     max_time = module.max_time
#     model_setup = create_model_setup(module)
#     run_time = model_setup.model_runtime
#
#     if run_time > max_time:
#         handle_timeout(module, model_setup, print_cons)
#         return new_optimize_model_setup(module, optimize_model, print_cons)
#
#     if optimize_model:
#         module, model_setup = optimize_N(module, model_setup, module, model_setup, print_cons)
#     return module, model_setup
#
# def show_progress(max_time, stop_event):
#     """Displays a progress bar for the specified duration."""
#     progress_thread = Thread(target=progress_bar, args=(max_time, stop_event))
#     progress_thread.start()

### END ALTERNATIVES ###


def load_module(args):
    """Returns a module from the arguments provided from the specified file.
    Updates the model to reflect the user specified flags."""
    module_path = args.file_path
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    module = BuildModule(module_name, module_path)
    module.contingent_bool = module.contingent_bool or args.contingent
    module.disjoint_bool = module.disjoint_bool or args.disjoint
    module.optimize_bool = module.optimize_bool or args.optimize
    module.print_constraints_bool = module.print_constraints_bool or args.print
    module.print_impossible_states_bool = module.print_impossible_states_bool or args.impossible
    module.save_bool = module.save_bool or args.save
    return module

def print_result(module, model_setup):
    """Prints resulting model or no model if none is found."""
    if model_setup.model_status:
        states_print = StateSpace(model_setup)
        states_print.print_to(module.print_constraints_bool, module.print_impossible_states_bool)
        if module.save_bool:
            file_name, print_cons = ask_save()
            save_or_append(module, states_print, file_name, print_cons, module.print_imposs)
        return
    model_setup.no_model_print(module.print_constraints_bool)
    if module.save_bool:
        file_name, print_cons = ask_save()
        no_model_save_or_append(module, model_setup, file_name)


def main():
    """load a test or generate a test when run without input"""
    if len(sys.argv) < 2:
        ask_generate_test()
        return
    args, package_name = parse_file_and_flags()
    if args.upgrade:
        try:
            subprocess.run(['pip', 'install', '--upgrade', package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to upgrade {package_name}: {e}")
        return

    module = load_module(args)

    # NOTE: seems to delay after progress bar completes
    # shows progress for finding z3 models
    module, model_setup = run_optimization_with_progress(module)
    # module, model_setup = optimize_model_setup(module)
    # NOTE: attempted the following to replace the above but now luck
    # module, model_setup = new_optimize_model_setup(module, optimize_model, print_cons)

    print_result(module, model_setup)

if __name__ == "__main__":
    main()
    # cProfile.run('main()')
    # cProfile.run('main()', 'profile_results')


# # Load the profiling data
# with open('profile_results', 'r') as f:
#     # profiler = pstats.Stats(f)
#     filename = 'profile_results'
#     profiler = pstats.Stats(filename)
#
# # Sort and print the profiling data by time
# profiler.sort_stats('time').print_stats()
