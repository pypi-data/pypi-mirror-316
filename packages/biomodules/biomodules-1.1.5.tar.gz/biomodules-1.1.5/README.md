# biomodules: 生物信息模块

## 通用模块

1. `MergeDir`，给定一个输入文件夹和一个输出文件，把该文件夹下的所有文件合并到该文件中；

## 序列相关（seq）

1. `Fastq2Fasta`，fastq转fasta；

## 预处理模块（preprocessing）

1. `Fastqc`，使用fastqc进行质量控制；
2. `Filtlong`，使用Filtlong过滤reads；

## 序列比对（align）

1. `blastn`，使用blastn进行序列比对；
2. `minimap2`，使用minimap2进行序列比对；
3. `samtools`，使用samtools处理比对结果；

## 变异检测（variant）

1. `bgzip`，bgzip压缩；
2. `bcftools`，bcftools相关功能；

## Oxford Nanopore（ont）

注意，使用该功能需要安装额外的包：

```shell
pip install biomodules[ont]
```

1. `medaka`，使用medaka call突变；