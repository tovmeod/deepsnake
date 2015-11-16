# -*- coding: utf-8 -*-
import sys
import os
from evaluationinfo import EvaluationInfo
from deepagent import Agent
import ctypes
from ctypes import *
from ctypes import POINTER
from ctypes import c_int
from ctypes import py_object
from ctypes.util import find_library
if sys.platform == 'linux2':
    ##########################################
    # find_library on Linux could only be used if your libAmiCoPyJava.so is
    # on system search path or path to the library is added in to LD_LIBRARY_PATH
    #
    # name =  'AmiCoPyJava'
    # loadName = find_library(name)
    ##########################################
    loadName = './libAmiCoPyJava.so'
    libamico = ctypes.CDLL(loadName)
    print libamico
else:  # else if OS is a Mac OS X (libAmiCo.dylib is searched for) or Windows (AmiCo.dll)
    name = 'AmiCoPyJava'
    loadName = find_library(name)
    print loadName
    libamico = ctypes.CDLL(loadName)
    print libamico

# import numpy
# os.environ['LD_LIBRARY_PATH'] = '/usr/lib/jvm/java-8-oracle/jre/lib/amd64:/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server'  # noqa


class ListPOINTER(object):
    """Just like a POINTER but accept a list of ctype as an argument"""
    def __init__(self, etype):
        self.etype = etype

    def from_param(self, param):
        if isinstance(param, (list, tuple)):
            # print "Py: IS INSTANCE"
            return (self.etype * len(param))(*param)
        else:
            # print "Py: NOT INSTANCE"
            return param


class ListByRef(object):
    """An argument that converts a list/tuple of ctype elements into a
    pointer to an array of pointers to the elements"""
    def __init__(self, etype):
        self.etype = etype
        self.etype_p = POINTER(etype)

    def from_param(self, param):
        if isinstance(param, (list, tuple)):
            val = (self.etype_p * len(param))()
            for i, v in enumerate(param):
                if isinstance(v, self.etype):
                    val[i] = self.etype_p(v)
                else:
                    val[i] = v
            return val
        else:
            return param


def from_param(self, param):
    if isinstance(param, (list, tuple)):
        return (self.etype * len(param))(*param)
    else:
        return param


def cfunc(name, dll, result, * args):
    """build and apply a ctypes prototype complete with parameter flags"""
    atypes = []
    aflags = []
    for arg in args:
        atypes.append(arg[1])
        aflags.append((arg[2], arg[0]) + arg[3:])
    return CFUNCTYPE(result, * atypes)((name, dll), tuple(aflags))

java_class = "ch/idsia/benchmark/mario/environments/MarioEnvironment"
libamico.amicoInitialize(1, "-Djava.class.path=." + os.pathsep + ":jdom.jar")
libamico.createMarioEnvironment(java_class)

reset = cfunc('reset', libamico, None, ('list', ListPOINTER(c_int), 1))
get_entire_observation = cfunc('getEntireObservation', libamico, py_object, ('list', c_int, 1), ('zEnemies', c_int, 1))
performAction = cfunc('performAction', libamico, None, ('list', ListPOINTER(c_int), 1))
getEvaluationInfo = cfunc('getEvaluationInfo', libamico, py_object)
getObservationDetails = cfunc('getObservationDetails', libamico, py_object)


def amico_simulator():
    """simple AmiCo env interaction"""
    print "Py: AmiCo Simulation Started:"
    print "library found: "
    print "Platform: ", sys.platform

    agent = Agent()

    options = ""
    if len(sys.argv) > 1:
        options = sys.argv[1]

    if options.startswith('"') and options.endswith('"'):
        options = options[1:-1]

    k = 1
    seed = 0
    print("Py: ======Evaluation STARTED======")
    total_iterations = 0
    # for i in range(k, k+10000):
    for i in range(k, k+1):
        options1 = options + " -ls " + str(seed)
        print("options: ", options1)
        reset(options1)
        obs_details = getObservationDetails()
        print(obs_details)
        agent.setObservationDetails(obs_details[0], obs_details[1], obs_details[2], obs_details[3])
        while not libamico.isLevelFinished():
            total_iterations += 1
            libamico.tick()
            obs = get_entire_observation(1, 0)
            # print '~=~=~' * 100
            # print obs
            # for o in obs:
            #     print len(o)
            # print '~=~=~' * 100
            agent.integrateObservation(obs[0], obs[1], obs[2], obs[3], obs[4])
            action = agent.getAction()
            # print "action: ", action
            performAction(action)
        print("Py: TOTAL ITERATIONS: ", total_iterations)
        evaluationInfo = getEvaluationInfo()
        print("evaluationInfo = \n", EvaluationInfo(evaluationInfo))
        seed += 1

if __name__ == "__main__":
    amico_simulator()
