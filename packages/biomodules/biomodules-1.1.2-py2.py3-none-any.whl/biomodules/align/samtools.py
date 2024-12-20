# -*- coding: utf-8 -*-
from okmodule import Flag, Option, Argument, Command


class SamtoolsView(Command):
    """使用samtools view处理sam/bam文件。

    Args:
        bam: Output BAM
        min_mq: Only include in output reads that have mapping quality >= INT
        threads: Number of additional threads to use
        output: Write output to file
        input: Input bam or sam file
    """
    bam = Flag('-b')
    min_mq = Option('-q')
    threads = Option('-@')
    output = Option('-o')
    input = Argument()
