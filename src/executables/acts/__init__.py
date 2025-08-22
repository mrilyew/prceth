from executables.Executable import Executable
from executables.Documentable import Documentable
from executables.Runnable import Runnable
from executables.Saveable import Saveable
from executables.RecursiveDeclarable import RecursiveDeclarable

class Act(Executable):
    self_name = "Act"

class BaseAct(Runnable, Documentable, Saveable, RecursiveDeclarable):
    self_name = "Act"
