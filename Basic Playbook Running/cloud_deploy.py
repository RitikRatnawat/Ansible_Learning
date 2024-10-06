import os
from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader 
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

def run_ansible_playbook(playbook_path, inventory_path, extra_vars=None):

    # Creating Dataloader, Inventory Manager and Variable Manager
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[inventory_path])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # Adding CLI Arguments
    options = {
        'connection': 'ssh',
        'module_path': None,
        'forks': 100,
        'syntax': False,
        'become': False,
        'become_method': 'sudo',
        'become_user': 'root',
        'check': False,
        'diff': False,
        'start_at_task': "Create a EC2 Instance",
    }

    # Set context
    context.CLIARGS = ImmutableDict(options)

    # Creating Playbook Executor
    playbook = PlaybookExecutor(
        playbooks=[playbook_path],
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords={},
    )

    if extra_vars:
        playbook.extra_vars = extra_vars

    # Running Playbook
    results = playbook.run()

    if results == 0:
        print("Playbook execution completed successfully.")
    elif results == 1:
        print("Playbook execution failed.")
    else:
        print("Unexpected failure during playbook execution.")



if __name__ == "__main__":

    # Paths to Ansible playbook and inventory file
    ansible_playbook_path = os.path.abspath("cloud_deploy.yml")
    ansible_inventory_path = os.path.abspath("inventory.ini")

    # Extra variables needed in Playbook
    extra_vars = { 'become': True }

    run_ansible_playbook(ansible_playbook_path, ansible_inventory_path, extra_vars)