#!/bin/bash

source $WORKING_DIR/.phenosnip/bin/activate

snakemake --jobs 1 --use-singularity --singularity-args "-B $WORKING_DIR:$WORKING_DIR" --snakefile 1_lines_analysis_rules --configfile config/single_age_study_config.yaml

