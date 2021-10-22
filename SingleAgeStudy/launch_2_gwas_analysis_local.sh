#!/bin/bash

source $WORKING_DIR/.phenosnip/bin/activate

snakemake --jobs 10 --use-singularity --singularity-args "-B $WORKING_DIR:$WORKING_DIR" --snakefile 2_gwas_execution_rules --configfile config/single_age_study_config.yaml

