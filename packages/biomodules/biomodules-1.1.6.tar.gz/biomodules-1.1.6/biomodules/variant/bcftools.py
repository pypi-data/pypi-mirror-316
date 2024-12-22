# -*- coding: utf-8 -*-
from okmodule import Option, Argument, Command


class BcftoolsIndex(Command):
    """bcftools index.

    bcftools (https://github.com/samtools/bcftools) need to be installed.

    Args:
        threads: Use multithreading with INT worker threads
        vcf: The VCF file.
    """
    threads = Option('--threads')
    vcf = Argument()



class BcftoolsConsensus(Command):
    """bcftools consensus.

    bcftools (https://github.com/samtools/bcftools) need to be installed.

    Args:
        fasta_ref: Reference sequence in fasta format
        output: Write output to a file
        vcf: The VCF file.
    """
    fasta_ref = Option('-f')
    output = Option('-o')
    vcf = Argument()
