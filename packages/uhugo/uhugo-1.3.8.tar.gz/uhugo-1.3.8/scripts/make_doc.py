import os
import shutil

if "scripts" in os.getcwd():
    os.chdir("../_docs")
else:
    os.chdir("_docs")


def make_doc():
    """Run Sphinx to build the doc."""
    try:
        # removing previous build
        print("removing previous build")
        cmd = "make clean"
        os.system(cmd)
        shutil.rmtree("../docs/", ignore_errors=True)

        # new build
        cmd = "make html"
        os.system(cmd)

        # copy files - windows cmd here
        print("copy files")
        shutil.copytree("_build/html/", "../docs")
    except Exception as error:
        print(error)
        exit(1)


if __name__ == "__main__":
    make_doc()
