import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_command(command, working_directory=None):
    try:
        if working_directory:
            cwd = os.getcwd()
            os.chdir(working_directory)
            subprocess.check_call(command, shell=True)
            os.chdir(cwd)
        else:
            subprocess.check_call(command, shell=True)
        logger.info(f"Command executed: {command}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {command}")
        logger.error(f"Error: {e}")


def setup_project():
    # Load SBVA
    run_command("git clone https://github.com/hgarrereyn/SBVA.git")
    run_command("curl -L https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz -o eigen-3.4.0.tar.gz", working_directory="SBVA")
    run_command("tar xf eigen-3.4.0.tar.gz", working_directory="SBVA")
    run_command("make", working_directory="SBVA")
    logger.info("SBVA setup complete.")

    # Load Kissat
    run_command("git clone https://github.com/arminbiere/kissat.git")
    run_command("./configure && make all", working_directory="kissat")
    logger.info("Kissat setup complete.")

if __name__ == "__main__":
    setup_project()
