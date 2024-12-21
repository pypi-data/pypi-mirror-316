# ============================================================================================================
# Communication.py
# lheywang on 19/12/2024
#
# Base file for the Communication class
#
# ============================================================================================================


class SiglentCommunication:
    def __init__(self, instr, baseclass):
        self.__instr__ = instr
        self.__baseclass__ = baseclass
