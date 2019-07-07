import argparse

from common import defaults


def main_args():
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--mode", default=defaults.MODE, type=str, choices=["hivemind", "robot"])
    argparser.add_argument("--hivemind_ip", default=defaults.HIVEMIND_IP, type=str)

    return argparser.parse_args()