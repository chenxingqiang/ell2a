import os
import subprocess
import shutil
import toml
import sys

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, check=True)
    return result


def npm_install():
    print("Running npm install")
    run_command("npm install", cwd="ell2a-studio")


def npm_build():
    print("Running npm build")
    run_command("npm run build", cwd="ell2a-studio")
    print("Copying static files")
    source_dir = os.path.join("ell2a-studio", "build")
    target_dir = os.path.join("src", "ell2a", "studio", "static")
    shutil.rmtree(target_dir, ignore_errors=True)
    shutil.copytree(source_dir, target_dir)
    print(f"Copied static files from {source_dir} to {target_dir}")


def get_ell2a_version():
    pyproject_path = "pyproject.toml"
    pyproject_data = toml.load(pyproject_path)
    return pyproject_data["tool"]["poetry"]["version"]


def run_pytest():
    print("Running pytest")
    try:
        run_command("pytest", cwd="tests")
    except subprocess.CalledProcessError:
        print("Pytest failed. Aborting build.")
        sys.exit(1)


def run_all_examples():
    print("Running all examples")
    try:
        run_command("python run_all_examples.py -w 16", cwd="tests")
    except subprocess.CalledProcessError:
        print("Some examples failed. Please review the output above.")
        user_input = input("Do you want to continue with the build? (y/n): ").lower()
        if user_input != 'y':
            print("Aborting build.")
            sys.exit(1)


def main():
    ell2a_version = get_ell2a_version()
    os.environ['REACT_APP_ELL2A_VERSION'] = ell2a_version
    npm_install()
    npm_build()
    run_pytest()
    run_all_examples()
    print("Build completed successfully.")


if __name__ == "__main__":
    main()
