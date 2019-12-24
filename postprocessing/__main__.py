'''
todo
'''

import argparse
import json
import os

import postprocessing

#-----------------------------------------------------------------------------#
# constants

class Constants():
    class __Paths():
        def __init__(self):
            self._root = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
            self._build = os.path.join(self._root, '..', 'build')
            self._risk_output = os.path.join(self._build, 'risk.json')

        @property
        def root(self):
            return self._root

        @property
        def build(self):
            return self._build

        @property
        def risk_output(self):
            return self._risk_output

    def __init__(self):
        self._paths = Constants.__Paths()

    @property
    def paths(self):
        return self._paths

CONSTANTS = Constants()

#-----------------------------------------------------------------------------#
# config

class Config():
    def __init__(self):
        self._input_path = None

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, new_path):
        self._input_path = new_path

#-----------------------------------------------------------------------------#
# risk

def postprocess_risk(result):
    cfg = result['config']
    data = result['data']

    n = cfg['max-fight-rounds']

    # print README-result in markdown-syntax
    print('| winner (%) | defenders  |   both   | attackers  |')
    print('|:----------:|:----------:|:--------:|:----------:|')

    for key_att, dict_def in data.items():
        # get number of attackers
        a = key_att[-1]
        for key_def, counts in dict_def.items():
            # get number of defenders
            d = key_def[-1]
            # calculate percentages from counts
            defended = counts['defended'] / n * 100
            draw = counts['draw'] / n * 100
            defeated = counts['defeated'] / n * 100
            # prepare print and find winner
            defended = f'{defended:2.0f}'
            draw = f'{draw:2.0f}'
            defeated = f'{defeated:2.0f}'
            if draw > defended:
                if defeated > draw:
                    defeated += '*'
                    draw += ' '
                    defended += ' '
                else:
                    defeated += ' '
                    draw += '*'
                    defended += ' '
            else:
                if defeated > defended:
                    defeated += '*'
                    draw += ' '
                    defended += ' '
                else:
                    defeated += ' '
                    draw += ' '
                    defended += '*'
            print(f'|  `{a}>` `({d}` |     {defended}    |    {draw}   |     {defeated}    |')

#-----------------------------------------------------------------------------#
# cmdline-parsing

def parse_cmdline():
    '''
    Parse cmdline-args and print help-msg if specified.
    '''

    #-------------------------------------------------------------------------#
    # define args and parse them

    description  = 'This tool takes simulation-results and processes it, '
    description += 'e.g. for visualization.'
    parser = argparse.ArgumentParser(description=description)

    # input-path
    help_msg = 'Defines the input-path of the simulation-file.'
    parser.add_argument('-i', '--input',
        metavar=('PATH'),
        dest='input_path',
        action='store',
        type=str,
        required=True,
        help=help_msg
    )

    args = parser.parse_args()

    #-------------------------------------------------------------------------#
    # finalize and return

    cfg = Config()

    cfg.input_path = args.input_path

    return cfg

#-----------------------------------------------------------------------------#
# main

if __name__ == '__main__':
    # extract params
    cfg = parse_cmdline()

    if not os.path.exists(cfg.input_path):
        print(f'ERROR: File of input-path {cfg.input_path} does not exist.')
        exit(1)

    result = None
    with open(cfg.input_path) as json_file:
        result = json.load(json_file)

    boardgame = result['boardgame']
    if boardgame == 'Risk':
        postprocess_risk(result)
    else:
        print(f'Unsupported boardgame {boardgame}')
