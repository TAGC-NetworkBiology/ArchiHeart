# ArchiOldHeart : Genetic architecture of natural variation of cardiac performance in flies 

## Article information

**Title:** Genetic architecture of natural variation of cardiac performance in flies 

**Authors:**
Saswati Saha 1,†, Lionel Spinelli 1,†, Jaime A Castro-Mondragon 2, Anaïs Kervadec 3, Laurent Kremmer 1,5, Laurence Roder 1, Krifa Sallouha 1, Magali Torres 1, Christine Brun 1,4, Georg Vogler 3, Rolf Bodmer 3, Alexandre R. Colas 3*, Karen Ocorr 3*, Laurent Perrin 1,4*

(†) Equal contribution
(1) Aix Marseille Univ, INSERM, TAGC, UMR_S_1090, Turing Centre for Living systems, 13288 Marseille, France
(2) Centre for Molecular Medicine Norway (NCMM), P.O. Box 1137 Blindern, 0318 Oslo, Norway
(3) Development, Aging and Regeneration Program, Sanford Burnham Prebys Medical Discovery Institute, 10901 North Torrey Pines Road, La Jolla, CA, 92037, USA
(4) CNRS, 13288 Marseille, France
(5) Present address: INRAE, Institut Sophia Agrobiotech, Université Côte d’Azur, CNRS, 06903 Sophia Antipolis, France

(*) Authors for correspondence (acolas@sbpdiscovery.org, kocorr@sbpdiscovery.org; laurent.perrin@univ-amu.fr) -  Laurent Perrin, TAGC UMR 1090, Campus de Luminy, Case 928, 13288 Marseille Cedex 9, France. Tel : +33 4 91828727

**Abstract:** Deciphering the genetic architecture of human cardiac disorders is of fundamental importance but their underlying complexity is a major hurdle. We investigated the natural variation of cardiac performance in the sequenced inbred lines of the Drosophila Genetic Reference Panel (DGRP)1. Genome Wide Associations Studies (GWAS) identified genetic networks associated with natural variation of cardiac traits which were extensively validated with in vivo cardiac-specific gene manipulation. Specifically, non-coding variants that we identified were used to map potential regulatory non-coding regions, which in turn were employed to predict Transcription Factors (TFs) binding sites. Cognate TFs, many of which themselves bear polymorphisms associated with variations of cardiac performance, were also validated by heart specific knockdown. Although rarely studied, the genetic control of phenotypic variability is of primary importance, with both medical and fundamental implications. We showed that the natural variations associated with variability in cardiac performance affect a set of genes overlapping with those associated with average traits but through different variants in the same genes. Furthermore, we showed that phenotypic variability is also associated with gene regulatory network deviations. More importantly, we documented correlations between genes associated with cardiac phenotypes in both flies and humans, which supports a conserved genetic architecture regulating adult cardiac function from arthropods to mammals. Specifically, roles for PAX9 and EGR2 in the regulation of the cardiac rhythm were established in both models, illustrating that the characteristics of natural variations in cardiac function identified in Drosophila can accelerate discovery in humans.

---
---

## Goal of the github

This github project contains the instructions and material to reproduce the analyses reported in the article (and more). Source code are available in the github repository. Required data and built Singularity images are available on download. Instructions to reproduce the analyses are provided below.

To reproduce the analysis, you have to first, prepare the environments (see "Prepare the Environments" section below), then execute the analysis step by step (see "Run the analysis" section below).

## Description of the dataset

The dataset contains the cardiac phenotype data of 1 week old dropsophila. The data are stored in a SQlite database available on Zenodo (see below).

---
---

## Prepare the environments

In order to prepare the environment for analysis execution, it is required to:

* Clone the github repository and set the WORKING_DIR environment variable
* Download the pre-processed data
* Install Singularity
* Download the Singularity images

Below you will find detailed instruction for each of these steps.

---

### Clone the github repository

Use you favorite method to clone this repository in a chosen folder. This will create a folder **ArchiOldHeart** with all the source code. The following folder and file stucture will be created:

```
ArchiOldHeart
├── LICENSE
├── README.md
└── SingleAgeStudy
    ├── config
    ├── input
    ├── script
    ├── src
    ├── 1_lines_analysis_rules
    ├── 2_gwas_execution_rules
    ├── 3_epistasis_execution_rules
    ├── launch_1_lines_analysis_local.sh
    ├── launch_1_lines_analysis_slurm.sh
    ├── launch_2_gwas_analysis_local.sh
    ├── launch_2_gwas_analysis_slurm.sh
    ├── launch_3_epistasis_analysis_local.sh
    └── launch_3_epistasis_analysis_slurm.sh
```

The **input** folder contains the input data. Some are already present at repository clone, other will be downloaded from Zenodo (see below).

The **script** folder contains the code used to execute the varios analysis steps.

The **src** code contain python OOP code used during the analysis to manage the data coming from the SQlite database.

The **config** folder contains the snakemake config file, the json config file to run snakemake on Slurm and the python requirement file to create the python virtual environment for snakemake.

The files named with **_rules** are the snakemake rule definition files (snakefiles) of the various analysis workflows.

The files with **.sh** extension are bash files used to launch the analysis workflows. The file with the **_local** name are used to launch the workflows on a workstation while the files with the **slurm** name are used to launch the workflow on a SLURM cluster.

---

### Set the WORKING_DIR variable

Then, you must set an environment variable called **WORKING_DIR** with a value set to the path to this folder.

For instance, if you have chosen to clone the Git repository in "/home/spinellil/workspace", then the **WORKING_DIR** variable will be set to "/home/spinellil/workspace/ArchiOldHeart"

On linux:

```
    export WORKING_DIR=/home/spinellil/workspace/moFluMemB
```

---

### Download the data

Data are available on Zenodo **TODO: Add the Data DOI**. You have to download:

* The SQlite database containing the phenotype value and metadata value for each individual drosophila and the variant information from GDRP2 consortium
* The genotype data from the DGRP2 consortium (BED, BIM and FAM files)

Use the following command on Linux:

```
   cd $WORKING_DIR/SingleAgeStudy

   wget **TODO : add the link to the SQLite file** -O Phenosnip.sqlite.tar.gz
    tar zxvf Phenosnip.sqlite.tar.gz

   wget **TODO : add the link to the DGRP2 file** -O dgrp2.tar.gz
    tar zxvf dgrp2.tar.gz
```

Once done, the **input** folder will look like:

```
ArchiOldHeart
└── SingleAgeStudy
    └──	input
	├── cov_wolbachia_inversions.txt
	├── cov_wolbachia.txt
	├── dgrp2.bed
	├── dgrp2.bim
	├── dgrp2.fam
	└── Phenosnip.201612.sqlite
```

---

### Install Singularity and Docker

You need to install Singularity v2.6 on your system to run the complete analysis. Follow the instructions here : https://sylabs.io/guides/2.6/admin-guide/

---

### Install Snakemake

You need to install Snakemake to run the complete analysis workflow. You can use your preferred solution : https://snakemake.readthedocs.io/en/stable/getting_started/installation.html

In the **config** folder, you will find a **python_virtualenv_freeze.txt** file that contains the package list used during our analysis to create a python virtual environment. You can easily reproduce the same virtual environment using this file.
See https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ for more details.

The following scripts use a virtual environment called **.phenosnip** and stored in the **WORKING_DIR**.

---

### Download the Singularity images

Singularity images files are stored on Zenodo **TODO: Add the Singularity containers DOI**. Execute the following commands to download the images:

On linux:

```
    cd $WORKING_DIR
    wget **TODO: Add the container phenosnip_singleageanalysis.img URL** -O phenosnip_singleageanalysis.img
    wget **TODO: Add the container phenosnip_singleageepistasis.img URL** -O phenosnip_singleageepistasis.img
    wget **TODO: Add the container phenosnip_singleagegwas.img URL** -O phenosnip_singleagegwas.img
```

One done, the folder will look like:

```
ArchiOldHeart
├── LICENSE
├── README.md
└── SingleAgeStudy
    ├── config
    ├── input
    ├── script
    ├── src
    ├── 1_lines_analysis_rules
    ├── 2_gwas_execution_rules
    ├── 3_epistasis_execution_rules
    ├── launch_1_lines_analysis_local.sh
    ├── launch_1_lines_analysis_slurm.sh
    ├── launch_2_gwas_analysis_local.sh
    ├── launch_2_gwas_analysis_slurm.sh
    ├── launch_3_epistasis_analysis_local.sh
    ├── launch_3_epistasis_analysis_slurm.sh
    ├── phenosnip_singleageanalysis.img
    ├── phenosnip_singleageepistasis.img
    └── phenosnip_singleagegwas.img
```

---
---

## Run the analysis

To run the complete analysis, you have to run the three workflow in the following order:

```
    cd $WORKING_DIR
    ./launch_1_lines_analysis_local.sh
    ./launch_2_gwas_analysis_local.sh
    ./launch_3_epistasis_analysis_local.sh
```

**IMPORTANT NOTES:**

* The previous command launch the analysis on a local computer. To run them in a SLURM cluster, use the **_slurm** files.
* The GWAS and Epistasis are computationally intensive. Prefer to run them on a powerfull workstation or on a HPC.










