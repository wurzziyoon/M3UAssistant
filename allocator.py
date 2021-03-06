"""
Allocator is responsible of:
1. concatenating .ts file fragments into one, and
2. converting .ts file to .mp4
"""


import logging
import os
import subprocess as sp
import sys
from typing import List


class Allocator:

    def __init__(self, alc_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned and create place holders for tools
        :param alc_logger: the logger assigned
        """
        self._logger = alc_logger
        self.cov_tool = None
        self.cat_tool = None

    def check_tool(self, conversion_tool: str, concatenation_tool: str) -> None:
        """
        Checking if the tools are available
        :param conversion_tool: the tool assigned for conversion
        :param concatenation_tool: the tool assigned for concatenation
        """
        if sp.call(['which', conversion_tool], stdout=sp.DEVNULL):
            self._logger.error(
                "abort: Cannot access conversion tool {}".format(conversion_tool))
            exit(2)

        if sp.call(['which', concatenation_tool], stdout=sp.DEVNULL):
            self._logger.error(
                "abort: Cannot access concatenation_tool tool {}".format(concatenation_tool))
            exit(2)

        self.cov_tool = conversion_tool
        self.cat_tool = concatenation_tool

    def concatenate(self, input_files: List[str], concatenated_name: str) -> None:
        """
        Concatenating the input files to one
        :param input_files: a list of files to concatenate
        :param concatenated_name: the name of the concatenated file
        """
        input_files = [file for file in input_files if file[-3:] == '.ts']
        if len(input_files) <= 1:
            return
        input_files.sort(key=len)
        cat_command = [self.cat_tool] + input_files + ['>', concatenated_name]
        os.system(" ".join(cat_command))

    def convert(self, in_ts: str, out_mp4: str) -> None:
        """
        Converting .ts file to .mp4
        :param in_ts: the .ts file to convert
        :param out_mp4: the name of the converted file
        """
        cov_command = '{tool} -i {in_ts} -codec {codec} {out_mp4} ' \
            .format(tool=self.cov_tool, in_ts=in_ts, codec='copy', out_mp4=out_mp4)

        sp.call(cov_command.split(), stdout=sp.DEVNULL, stderr=sp.DEVNULL)


# Demo
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    minion = Allocator(logger)
    minion.concatenate(input_files=['01.ts', '02.ts', '03.ts'], concatenated_name="out.ts")
    minion.convert(in_ts="out.ts", out_mp4="out.mp4")
