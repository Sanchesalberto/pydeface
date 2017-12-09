"""Utility scripts for pydeface."""

import os
import sys
import subprocess
from pkg_resources import resource_filename, Requirement


def run_shell_cmd(cmd, cwd=[]):
    """Run a command in the shell using Popen."""
    if cwd:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   cwd=cwd)
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line.strip())
    process.wait()


def usage():
    """Print the docstring and exit."""
    sys.stdout.write(__doc__)
    sys.exit(2)


def initial_checks(template=None, facemask=None):
    """Initial sanity checks."""
    if template is None:
        template = resource_filename(Requirement.parse("pydeface"),
                                     "pydeface/data/mean_reg2mean.nii.gz")
    if facemask is None:
        facemask = resource_filename(Requirement.parse("pydeface"),
                                     "pydeface/data/facemask.nii.gz")

    if not os.path.exists(template):
        raise Exception('Missing template: %s' % template)
    if not os.path.exists(facemask):
        raise Exception('Missing face mask: %s' % facemask)

    if 'FSLDIR' not in os.environ:
        raise Exception("FSL must be installed and "
                        "FSLDIR environment variable must be defined.")
        sys.exit(2)
    return template, facemask


def check_output_path(outfile, infile, force=False):
    """Determine output file name."""
    if force is None:
        force = False

    if os.path.exists(outfile) and force:
        print('Previous output will be overwritten.')
    elif os.path.exists(outfile):
        raise Exception("%s already exists. Remove it first or use '--force' "
                        "flag to overwrite." % outfile)
    else:
        outfile = infile.replace('.nii', '_defaced.nii')
    return outfile
