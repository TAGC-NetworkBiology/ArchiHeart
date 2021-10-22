#!/bin/bash

module load userspace/all
module load python3/3.6.3
source $WORKING_DIR/.phenosnip/bin/activate

snakemake --jobs 1 --use-singularity --singularity-args "-B $WORKING_DIR:$WORKING_DIR" --snakefile 1_lines_analysis_rules --configfile config/single_age_study_config.yaml --cluster-config config/single_age_study_cluster.json --cluster 'sbatch -A {cluster.project} --job-name {cluster.job-name} --ntasks {cluster.ntasks} --cpus-per-task {threads} --mem-per-cpu {cluster.mem-per-cpu} --partition {cluster.partition} --time {cluster.time} --mail-user {cluster.mail-user} --mail-type {cluster.mail-type} --error {cluster.error} --output {cluster.output}'

