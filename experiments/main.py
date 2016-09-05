#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import random, itertools
from hfo import *
from cmac import CMAC
from sarsa import SARSA

import argparse

def str2bool(v):
    """ Helps to avoid confusion for truth values. """
    return v.lower() in ("yes", "true", "t", "1")

def parse_args(args):
    """ Parse command line parameters.

    Args:
        args (tuple[str]): All settings either default or set via command line arguments.

    Returns:
        args (argparse.Namespace): All settings either default or set via command line arguments.

    """
    parser = argparse.ArgumentParser(
            description="Realising learning with Half Field Offense.")

    exparg = parser.add_argument_group('Experiment')
    exparg.add_argument("--exp_type", default="AtariExp", help="Choose experiment implementation.")
    exparg.add_argument("--env_type", default="AtariEnv", help="Choose environment implementation.")
    exparg.add_argument("--agent_type", default="AtariAgent", help="Choose agent implementation.")

def run():
    print('New agent online!')
    print('..... Initializing learning algorithm: SARSA')
    ACTIONS = [MOVE, SHOOT, PASS_CLOSE, PASS_FAR, DRIBBLE]
    SARSA = SARSA(ACTIONS)
    print('..... Initializing discretization with CMAC')
    CMAC = CMAC(1,0.5,0.1)
    print('..... Loading HFO environment')
    hfo = HFOEnvironment()
    print('..... Connecting to HFO server')
    hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                      'bin/teams/base/config/formations-dt', 6000,
                      'localhost', 'base_left', False)
    print('..... Start training')
    for episode in itertools.count():
        print('..... Starting episode %d' % episode)
        status = IN_GAME
        step = 0
        while status == IN_GAME:
            step += 1
            old_status = status
            # Get the vector of state features for the current state
            features = hfo.getState()
            state = transformFeatures(features)
            print('State: %s' % str(state))

            action = select_action(state)
            hfo.act(action)
            #print('Action: %s' % str(action))
            # Advance the environment and get the game status
            status = hfo.step()
            #print('Status: %s' % str(status))
            print('.......... Step %d: %s - %s - %s' % (step, str(old_status), str(action), str(status)))
        # Check the outcome of the episode
        print('..... Episode ended with %s'% hfo.statusToString(status))
        # Quit if the server goes down
        if status == SERVER_DOWN:
            hfo.act(QUIT)
            break


if __name__ == '__main__':
    run()
