#!/bin/bash

module load userspace/all
module load python3/3.6.3
source $WORKING_DIR/.phenosnip/bin/activate

snakemake --jobs 10 --use-singularity --singularity-args "-B $WORKING_DIR:$WORKING_DIR" --snakefile 3_epistasis_execution_rules --configfile config/single_age_study_config.yaml --cluster-config config/single_age_study_cluster.json --cluster 'sbatch --job-name {cluster.job-name} -A {cluster.project} -N {cluster.nodes-number} -n {cluster.cores-number} --ntasks {cluster.ntasks} --cpus-per-task {threads} --mem-per-cpu {cluster.mem-per-cpu} --partition {cluster.partition} --time {cluster.time} --mail-user {cluster.mail-user} --mail-type {cluster.mail-type} --error {cluster.error} --output {cluster.output}'

