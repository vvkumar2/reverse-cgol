import subprocess

def run_command(command):
    """Run shell commands in the specified working directory."""
    try:
        subprocess.check_call(command, shell=True)
        print(f"Executed: {command}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def main():
    # Clone the SBVA repository
    run_command("git clone https://github.com/hgarrereyn/SBVA.git")
    run_command("cd SBVA && curl -L https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz -o eigen-3.4.0.tar.gz")
    run_command("cd SBVA && tar xf eigen-3.4.0.tar.gz")
    run_command("cd SBVA && make")

    # Clone the Kissat SAT solver
    run_command("git clone https://github.com/arminbiere/kissat.git")
    run_command("cd kissat && ./configure && make all")

if __name__ == "__main__":
    main()
