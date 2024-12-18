
### python provided modules ###
import time
import os
import sys
from copy import deepcopy
import pickle
import datetime
import argparse

### extra common libraries ###
import numpy as np

### ace-reaction libraries ###
from tsflow import chem
from tsflow import mcd
from tsflow.utils import process


def parse_qc_content(f):
    qc_content = ''
    while True:
        line = f.readline()
        if line == '\n':
            break
        qc_content = qc_content + line
    return qc_content


def parse_reactant(f):
    state_info = f.readline().strip().split(' ')
    chg,multiplicity = int(state_info[0]), int(state_info[1])
    atom_list = []
    atom_info = f.readline()
    while atom_info.strip() != '':
        atom_info = atom_info.strip().split()
        #print (atom_info)
        atom_type = atom_info[0]
        x = float(atom_info[1])
        y = float(atom_info[2])
        z = float(atom_info[3])
        atom = chem.Atom(atom_type)
        atom.x = x
        atom.y = y
        atom.z = z
        atom_list.append(atom)
        try:
            atom_info = f.readline()
            if atom_info.strip() == '':
                break
        except:
            break 
    reactant = chem.Molecule()
    reactant.atom_list = atom_list
    reactant.chg = chg
    reactant.multiplicity = multiplicity
    return reactant
   

def parse_coordinate(f):
    constraints = dict()
    num_steps = dict()
    while True:
        line = f.readline()
        if line == '\n':
            break
        info = line.strip().split()
        try:
            constraint = tuple([int(idx) - 1 for idx in info[:-2]])
            target_value = float(info[-2])
        except:
            print ('Wrong coordinate found! Check coordinate file again !!!')
            print (f'Current line: {line.strip()}')
            print ('Input should be given as: [Coordinate] [target value] [num_step]')
            exit()
        if len(constraint)  < 2:
            print ('Wrong coordinate found! Check coordinate file again !!!')
            print (f'Current line: {line.strip()}')
            print ('Input should be given as: [Coordinate] [target value] [num_step]')
            exit()
        if len(constraint) > 2:
            target_value *= np.pi/180
        constraints[constraint] = target_value
        try:
            num_steps[constraint] = int(info[-1])
        except:
            print ('Num steps are not given! Check coordinate file again !!!')
            print ('Input should be given as: [Coordinate] [target value] [num_step]')
            exit()     
    return constraints, num_steps


def parse_option(f):
    option = make_default_option()
    is_good = True
    wrong_attributes = []
    while True:
        correct = True
        line = f.readline()
        try:
            words = line.strip().split('=')
            attribute = words[0]
            value = words[1]
        except:
            break
        if line == '\n':
            break
        if attribute == 'num_relaxation':
            try:
                value = int(value)
                if value <= 0:
                    print (f'Wrong num_relaxation (={value}) is given! Check the option file !!!')
                    print (f'The value must be positive integer !!!\n')
                    correct = False
            except:
                print (f'Wrong num_relaxation (={value}) is given! Check the option file !!!')
                print (f'The value must be positive integer !!!\n')
                correct = False
        elif attribute == 'step_size':
            try:
                value = float(value)
                if value <= 0.0:
                    print (f'Wrong step_size (={value}) is given! Check the option file !!!')
                    print (f'The value must be positive !!!\n')
                    correct = False
            except:
                print (f'Wrong step_size (={value}) is given! Check the option file !!!')
                print (f'The value must be positive !!!\n')
                correct = False
        elif attribute == 'unit':
            if not value in ['eV','Hartree','kcal']:
                print (f'Wrong unit (={value}) is given! Check the option file !!!')
                print ('Only eV, Hartree, kcal are allowed options !!!\n')
                correct = False
        elif attribute == 'use_hessian':
            try:
                value = int(value)
                if not value in [0,1]:
                    print (f'Wrong use_hessian (={value}) is given! Check the option file !!!')
                    print ('Only 0 or 1 are possible. If the value is zero, hessian is not used. Otherwise, hessian is used ... Default value is 0 \n')
                    correct = False
            except:
                print (f'Wrong use_hessian (={value}) is given! Check the option file !!!')
                print ('Only 0 or 1 are possible. If the value is zero, hessian is not used. Otherwise, hessian is used ... Default value is 0 \n')
                correct = False

        elif attribute == 'hessian_update':
            if not str.lower(value) in ['exact','bofill']:
                print (f'Wrong hessian_update (={value}) is given! Check the option file !!!')
                print ('Only bofill and exact are possible options !!! Default method is bofill\n')
                correct = False

        elif attribute == 'reoptimize':
            try:
                value = int(value)
                if not value in [0,1]:
                    print (f'Wrong reoptimize (={value}) is given! Check the option file !!!')
                    print ('Only 0 or 1 are possible. If the value is zero, given geometry is directly undergone MCD, otherwise, the molecule is reoptimized !!! Default value is 1\n')
                    correct = False
            except:
                print (f'Wrong reoptimize (={value}) is given! Check the option file !!!')
                print ('Only 0 or 1 are possible. If the value is zero, given geometry is directly undergone MCD, otherwise, the molecule is reoptimized !!! Default value is 1\n')
                correct = False
        else:
            wrong_attributes.append(attribute)
            correct = False
        
        if correct:
            option[attribute] = value

        if not correct:
            is_good = False

    if len(wrong_attributes) > 0:
        content = ','.join(wrong_attributes)
        print (f'Wrong attribute(s) (={content}) is given! Check the option file !!!')
        print ('Possible attributes are \'working_directory\', \'num_relaxation\',\'step_size\',\'unit\',\'calculator\',\'command\',\'use_hessian\',\'hessian_update\',\'reoptimize\'')


    else:
        print ('option directory is not found! Default parameters are used!!!')

    return option, is_good



def make_default_option():
    option = dict()
    option['num_relaxation'] = 5
    option['step_size'] = 0.0
    option['unit'] = 'Hartree'
    option['use_hessian'] = 0
    option['reoptimize'] = 1
    option['restart'] = 0
    option['hessian_update'] = 'bofill'    
    return option


def read_bond_info(directory):
    constraints = dict()
    num_steps = dict()
    formed_bonds = []
    broken_bonds = []
    try:
        f =  open(os.path.join(directory,'coordinates'))
    except:
        print ('Cannot find \'coordinates\' file! Recheck your input !!!')
        exit()
    for line in f:
        info = line.strip().split() #0: start, 1: end, 2: target length, 3: Num steps
        if len(info) > 0:
            try:
                constraint = tuple([int(idx) - 1 for idx in info[:-2]])
                target_value = float(info[-2])
            except:
                print ('Wrong coordinate found! Check coordinate file again !!!')
                print (f'Current line: {line.strip()}')
                print ('Input should be given as: [Coordinate] [target value] [num_step]')
                exit()
            if len(constraint)  < 2:
                print ('Wrong coordinate found! Check coordinate file again !!!')
                print (f'Current line: {line.strip()}')
                print ('Input should be given as: [Coordinate] [target value] [num_step]')
                exit()
            if len(constraint) > 2:
                target_value *= np.pi/180
            constraints[constraint] = target_value
            try:
                num_steps[constraint] = int(info[-1])
            except:
                print ('Num steps are not given! Check coordinate file again !!!')
                print ('Input should be given as: [Coordinate] [target value] [num_step]')
                exit()
    return constraints, num_steps


def change_option(args):
    correct = True
    try:
        option_directory = os.path.join(args.input_directory,'option')
    except:
        print ('Default option is used !!!')
        return
    if os.path.exists(option_directory):
        wrong_attributes = []
        with open(option_directory) as f:
            for line in f:
                words = line.strip().split('=')
                attribute = words[0]
                value = words[1]
                if attribute == 'working_directory':
                    args.working_directory = value
                elif attribute == 'num_relaxation':
                    try:
                        value = int(value)
                        if value <= 0:
                            print (f'Wrong num_relaxation (={value}) is given! Check the option file !!!')
                            print (f'The value must be positive integer !!!\n')
                            correct = False
                        else:
                            args.num_relaxation = value
                    except:
                        print (f'Wrong num_relaxation (={value}) is given! Check the option file !!!')
                        print (f'The value must be positive integer !!!\n')
                        correct = False
                elif attribute == 'step_size':
                    try:
                        value = float(value)
                        if value <= 0.0:
                            print (f'Wrong step_size (={value}) is given! Check the option file !!!')
                            print (f'The value must be positive !!!\n')
                            correct = False
                        else:
                            args.step_size = value
                    except:
                        print (f'Wrong step_size (={value}) is given! Check the option file !!!')
                        print (f'The value must be positive !!!\n')
                        correct = False
                elif attribute == 'unit':
                    if not value in ['eV','Hartree','kcal']:
                        print (f'Wrong unit (={value}) is given! Check the option file !!!')
                        print ('Only eV, Hartree, kcal are allowed options !!!\n')
                        correct = False
                    else:
                        args.unit = value
                elif attribute == 'calculator':
                   args.calculator = value
                elif attribute == 'command':
                    args.command = value
                elif attribute == 'use_hessian':
                    try:
                        value = int(value)
                        if not value in [0,1]:
                            print (f'Wrong use_hessian (={value}) is given! Check the option file !!!')
                            print ('Only 0 or 1 are possible. If the value is zero, hessian is not used. Otherwise, hessian is used ... Default value is 0 \n')
                            correct = False
                        else:
                            args.use_hessian = value
                    except:
                        print (f'Wrong use_hessian (={value}) is given! Check the option file !!!')
                        print ('Only 0 or 1 are possible. If the value is zero, hessian is not used. Otherwise, hessian is used ... Default value is 0 \n')
                        correct = False

                elif attribute == 'hessian_update':
                    if not str.lower(value) in ['exact','bofill']:
                        print (f'Wrong hessian_update (={value}) is given! Check the option file !!!')
                        print ('Only bofill and exact are possible options !!! Default method is bofill\n')
                        correct = False
                    else:
                        args.hessian_update = value

                elif attribute == 'reoptimize':
                    try:
                        value = int(value)
                        if not value in [0,1]:
                            print (f'Wrong reoptimize (={value}) is given! Check the option file !!!')
                            print ('Only 0 or 1 are possible. If the value is zero, given geometry is directly undergone MCD, otherwise, the molecule is reoptimized !!! Default value is 1\n')
                            correct = False
                        else:
                            args.reoptimize = value
                    except:
                        print (f'Wrong reoptimize (={value}) is given! Check the option file !!!')
                        print ('Only 0 or 1 are possible. If the value is zero, given geometry is directly undergone MCD, otherwise, the molecule is reoptimized !!! Default value is 1\n')
                        correct = False
                else:
                    wrong_attributes.append(attribute)
                    correct = False

            if len(wrong_attributes) > 0:
                content = ','.join(wrong_attributes)
                print (f'Wrong attribute(s) (={content}) is given! Check the option file !!!')
                print ('Possible attributes are \'working_directory\', \'num_relaxation\',\'step_size\',\'unit\',\'calculator\',\'command\',\'use_hessian\',\'hessian_update\',\'reoptimize\'')


    else:
        print ('option directory is not found! Default parameters are used!!!')

    return correct

def get_calculator(args):
    calculator_name = args.calculator.lower()
    if calculator_name == 'gaussian':
        from tsflow.Calculator import gaussian
        calculator = gaussian.Gaussian(args.command)
    elif calculator_name == 'orca':
        from tsflow.Calculator import orca
        calculator = orca.Orca(args.command)
    else:
        print (f'Wrong calculator (={calculator_name}) is given! Check the option file !!!')
        calculator = None
        return calculator
    return calculator


def generate_path():
    import datetime
    parser = argparse.ArgumentParser()
    #parser.add_argument('--input_directory','-id',type=str,help='directory of inputs')
    parser.add_argument('--output_directory','-od',type=str,help='directory for saving outputs',default=None)
    parser.add_argument('--calculator','-c',type=str,help='Name of Quantum Calculation software',default='gaussian')
    parser.add_argument('--command',type=str,help='command for running qc package',default='g09')
    parser.add_argument('--basis_directory','-bd',type=str,help='directory for the basis set file',default=None)

    print (sys.argv)

    if len(sys.argv) > 2:
        args = parser.parse_args(sys.argv[2:])
    else:
        args = parser.parse_args([])

    #input_directory = args.input_directory
    input_directory = sys.argv[1]
    output_directory = args.output_directory
    if output_directory is None:
        output_directory = os.path.dirname(input_directory)
        print (output_directory)
        if output_directory=='':
            output_directory = os.getcwd()
    # If problem with input, output directory, automatically exit
    if not os.path.exists(input_directory):
        print ('Cannot find the input directory !!!')
        exit()
    elif not os.path.exists(output_directory):
        print ('Given output directory is not found !!!')
        exit()

    print (f'\ninput directory: {input_directory}')
    print (f'output directory: {output_directory}\n')

    if not os.path.exists(input_directory):
        print ('Input not found !!!')
        return
    
    f = open(input_directory)
    qc_content = parse_qc_content(f)
    reactant = parse_reactant(f)
    constraints, num_steps = parse_coordinate(f)
    option,is_good = parse_option(f)  
    f.close()

    calculator = get_calculator(args)
    calculator.qc_content = qc_content
    # Find basis file, if exists ...
    basis_directory = args.basis_directory
    if basis_directory is not None and os.path.exists(basis_directory):
        print ('New basis file found !!! Loading new basis set ...')
        calculator.load_basis(basis_directory)

    print (option)
    print (is_good)

    scanner = mcd.MCD(num_relaxation = option['num_relaxation'],calculator=calculator)
    scanner.use_hessian = option['use_hessian']
    scanner.hessian_update = option['hessian_update']
    scanner.step_size = option['step_size']
    scanner.log_directory = output_directory
    try:
        working_directory = os.environ['MCD_SCRDIR']
    except:
        working_directory = output_directory
    
    if not os.path.exists(working_directory):
        print ('working directory does not exist!!! Using output directory as default ...')
        working_directory = output_directory
    
    scanner.change_working_directory(working_directory)
    print (f'working directory: {working_directory}\n')

    scanner.change_energy_unit(option['unit'])
    num_scan = sum(num_steps.values())

    print ('\n=======================================================')
    print ('================= PYMCD RUNNING !!! ===================')
    print ('=======================================================\n')

    pathway = scanner.scan(reactant,constraints,num_steps,chg = reactant.chg, multiplicity = reactant.multiplicity)
    return pathway

def main():
    pathway = generate_path()     
    if len(pathway) > 0:
        print ('MCD well terminated ...')
    else:
        print ('MCD did not run properly !!!')

if __name__ == '__main__':
    
    main()
