# standard library modules, , ,
import os
import logging

# Component, , represents an installed component, internal
from lib import component
# CMakeGen, , generate build files, internal
from lib import cmakegen


def addOptions(parser):
    pass


def execCommand(args):
    cwd = os.getcwd()
    c = component.Component(cwd)
    if not c:
        logging.debug(str(c.error))
        logging.error('The current directory does not contain a valid component.')
        return 1
    builddir = os.path.join(cwd, 'build')

    target, errors = c.satisfyTarget(args.target)
    if errors:
        for error in errors:
            logging.error(error)
        return 1

    all_components = c.getDependenciesRecursive(target=target)
    logging.info('all dependencies: (target=%s)' % target)
    for d in all_components.values():
        logging.info('    %s@%s: %s' % (d.getName(), d.getVersion(), os.path.relpath(d.path)))

    generator = cmakegen.CMakeGen(builddir, target)
    for error in generator.generateRecursive(c, all_components, builddir):
        logging.error(error)