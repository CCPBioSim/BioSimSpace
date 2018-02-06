import __main__ as main

# Determine whether we're being imported from a Jupyter notebook.
def _is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

# Interactive tools.
if _is_notebook():
    import BioSimSpace.Notebook

import BioSimSpace.Process
import BioSimSpace.Protocol

import Sire.IO
import Sire.Base
import Sire.System

import Sire.Mol

from Sire.Mol import AtomMCSMatcher as MCSMatcher

def readMolecules( files ):
    return Sire.IO.MoleculeParser.read( files )

def readMolecule( files ):
    return Sire.IO.MoleculeParser.read( files )[Sire.Mol.MolIdx(0)].molecule()

def saveMolecules(filebase, system, fileformat):
    return Sire.IO.MoleculeParser.save(system, filebase, \
                      {"fileformat":Sire.Base.wrap(fileformat)})

def saveMolecule(filebase, molecule):
    s = Sire.System.System("BioSimSpace molecule")
    m = Sire.Mol.MoleculeGroup("all")
    m.add(molecule)
    s._old_add(m)
    f1 = saveMolecules(filebase, s, "PRM7")
    f2 = saveMolecules(filebase, s, "RST7")
    return f1+f2

def _system_add(system, molecule):
    system._old_add(molecule, Sire.Mol.MGIdx(0))

def _system_fileformat(system):
    return system.property("fileformat").value()

def _system_take(system, molid):
    molecule = system[ molid ]
    system.remove(molecule.number())
    return molecule

Sire.System.System._old_add = Sire.System.System.add
Sire.System.System.add = _system_add
Sire.System.System.fileFormat = _system_fileformat
Sire.System.System.take = _system_take

class MolWithResName(Sire.Mol.MolWithResID):
    def __init__(self, resname):
        super().__init__( Sire.Mol.ResName(resname) )
