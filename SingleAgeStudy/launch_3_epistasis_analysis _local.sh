#!/bin/bash

module load userspace/all
module load python3/3.6.3
source $WORKING_DIR/.phenosnip/bin/activate

snakemake --jobs 10 --use-singularity --singularity-args "-B $WORKING_DIR:$WORKING_DIR" --snakefile 3_epistasis_execution_rules --configfile config/single_age_study_config.yaml

