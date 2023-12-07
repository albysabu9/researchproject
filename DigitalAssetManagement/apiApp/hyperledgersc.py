import subprocess
import uuid

def create_ledger(from_owner, to_owner, amt=None, productname=None, action=None):
    # Define the arguments you want to pass to the shell script
    arg1 = str(uuid.uuid4())
    arg2 = from_owner
    arg3 = to_owner
    arg4 = action


    # Path to your shell script
    shell_script_path = "/home/albysabu/Desktop/Project/code/DigitalAssetManagement/apiApp/createledger.sh"

    # Construct the command with arguments
    command = [
        "bash",
        shell_script_path,
        arg1,
        arg2,
        arg3,
        arg4
    ]

    # Run the shell script with subprocess
    subprocess.run(command)
    return {
        "from_owner":from_owner,
        "to_owner":to_owner,
        "amt":amt,
        "productname":productname,
        "action":action
    }