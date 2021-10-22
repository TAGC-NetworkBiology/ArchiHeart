# -*- coding: utf-8 -*-

import os, re
import logging


# ########################################
#  GENERAL CONSTANTS
# ########################################

BOOLEAN_TYPE_STRING = "boolean"
BOOLEAN_FALSE_STRING = "false"
BOOLEAN_TRUE_STRING = "true"
BOOLEAN_VALUES_STRING = [ BOOLEAN_FALSE_STRING, BOOLEAN_TRUE_STRING]


STRING_TYPE_STRING = "true"


# ########################################
#   KEYWORDS
# ########################################
MEAN_KEYWORD = 'MEAN'
IQR_KEYWORD = 'IQR'
IQR_15_KEYWORD = '1.5IQR'
MEDIAN_KEYWORD = 'MEDIAN'
METHODS_LIST = [MEAN_KEYWORD, IQR_KEYWORD, IQR_15_KEYWORD, MEDIAN_KEYWORD]
FALSE_KEYWORDS = ['False', 'FALSE', 'F', 'false', 'f']


###############################################################################
# STRATEGIES
###############################################################################
STRATEGIES = ['Insertion', 'PhenotypeStatistics', 'Processing', 'Analysis', 'PopulationAnalysis', 'InteractiveQuery', 'RareVariant', 'Epistasis']
OPTIONS_GIVEN = """###############################################################################
# OPTIONS GIVEN
###############################################################################\n"""

# ########################################
#  # Extensions files tag
# ########################################
EXTENSION_ODS_TAG = 'ODS'
EXTENSION_XLS_TAG = 'XLS'
EXTENSION_XLSX_TAG = 'XLSX'
EXTENSION_TXT_TAG = 'TXT'
EXTENSION_CSV_TAG = 'CSV'
EXTENSION_LIST = [EXTENSION_ODS_TAG, EXTENSION_XLS_TAG,
                  EXTENSION_XLSX_TAG, EXTENSION_TXT_TAG, EXTENSION_CSV_TAG]


# ########################################
# Constants about DGRP input Files
#  and data file
# tag, regex
# ########################################
# Constants for header name in data file
INDIVIDUAL_TAG = 'Filename'
SCALE_FACTOR_TAG = 'Scale_Factor'
GENOTYPE_TAG = 'Genotype'
ID_TAG = 'ID'
DATE_CONTROL_TAG = 'Date_Control'
AGE_TAG = 'Age'
SEX_TAG = 'Sex'
SOFTWARE_USER_TAG = 'Software_user'
COMMENTS_TAG = 'Comments'

DATE_CONTROL_REGEX = '^[0123]{1}[0-9]{1}[01]{1}[0-9]{1}[0-9]{2}$'
SEX_REGEX = '^[fFmM]{1}$'


DGRP_REGEX_BASE = 'Constants.DGRP_ENTRY_'
DGRP_REGEX_FINAL = '_REGEX'

# Tag for different mutation
DGRP_LIST_MUTATION = ["SNP", "INS", "DEL", "MNP"]
DGRP_ENTRY_SNP_TAG = "SNP"
DGRP_ENTRY_MNP_TAG = "MNP"
DGRP_ENTRY_INSERTION_TAG = "INS"
DGRP_ENTRY_DELETION_TAG = "DEL"

# Pattern for SNP, INS, DEL, MNP
PATTERN_SNP = re.compile(DGRP_ENTRY_SNP_TAG)
PATTERN_INS = re.compile(DGRP_ENTRY_INSERTION_TAG)
PATTERN_DEL = re.compile(DGRP_ENTRY_DELETION_TAG)
PATTERN_MNP = re.compile(DGRP_ENTRY_MNP_TAG)

# REGEX for column
DGRP_ENTRY_CHROMOSOM_REGEX = '^.*(2R|2L|3R|3L|4|X).*$'
DGRP_ENTRY_POSITION_REGEX = '^[0-9]+$'
DGRP_ENTRY_IDENTIFIER_REGEX = '^(2R|2L|3R|3L|4|X)_\d+_(SNP|MNP|INS|DEL)$'
DGRP_ENTRY_IDENTIFIER_PATTERN = re.compile( DGRP_ENTRY_IDENTIFIER_REGEX )
DGRP_ENTRY_QUALITY_REGEX = "^999$"
DGRP_ENTRY_FORMAT_REGEX = "^GT$"
DGRP_ENTRY_FILTER_REGEX = "^PASS$"

# Tag for count reference and alternative allele
REFCOUNT_TAG = 'REFCOUNT'
ALTCOUNT_TAG = 'ALTCOUNT'

# Regex for mutations
# One unique letter among A,T,C or G for SNP for reference\
# and alternative allele
DGRP_ENTRY_REFERENCE_ALLELE_SNP_REGEX = '^(A|T|G|C){1}$'
DGRP_ENTRY_ALTERNATIVE_ALLELE_SNP_REGEX = '^(A|T|G|C){1}$'

# One letter for insertion reference allele
DGRP_ENTRY_REFERENCE_ALLELE_INS_REGEX = '^(A|T|G|C){1,}$'
# More of one letter for insertion alternative allele
DGRP_ENTRY_ALTERNATIVE_ALLELE_INS_REGEX = '^[ATGC]{2,}$'

# More of one letter for deletion reference allele
DGRP_ENTRY_REFERENCE_ALLELE_DEL_REGEX = '^[ATGC]{2,}$'
# One letter for deletion alternative allele
DGRP_ENTRY_ALTERNATIVE_ALLELE_DEL_REGEX = '^(A|T|G|C){1,}$'

# More of one letter for mnp reference and alternative allele
DGRP_ENTRY_REFERENCE_ALLELE_MNP_REGEX = '^[ATGC]{2,}$'
DGRP_ENTRY_ALTERNATIVE_ALLELE_MNP_REGEX = '^[ATGC]{2,}$'

DGRP_ENTRY_ANNOTATION_REGEX = '.*(ANNOTATION=[a-zA-Z0-9]*\|.*\|[A-Z_]*\|[0-9]*);.*'
DGRP_ENTRY_ANNOTATION_UNDEFINED_GENE_ID = 'UNDEFINED_GENE_ID'
DGRP_ENTRY_ANNOTATION_UNDEFINED_GENE_SYMBOL = 'UNDEFINED_GENE_SYMBOL'
DGRP_ENTRY_ANNOTATION_UNDEFINED_EFFECT_TYPE = 'UNDEFINED_EFFECT_TYPE'
DGRP_ENTRY_ANNOTATION_UNDEFINED_EFFECT_POSITION = -1


DGRP_ENTRY_IDENTIFIER_TYPE = 'IDENTIFIER'
DGRP_ENTRY_CHROMOSOM_TYPE = 'CHROMOSOM'
DGRP_ENTRY_QUALITY_TYPE = 'QUALITY'
DGRP_ENTRY_FORMAT_TYPE = 'FORMAT'
DGRP_ENTRY_FILTER_TYPE = 'FILTER'
DGRP_ENTRY_POSITION_TYPE = 'POSITION'
DGRP_ENTRY_REFERENCE_ALLELE_SNP = 'REFERENCE_ALLELE_SNP'
DGRP_ENTRY_ALTERNATIVE_ALLELE_SNP = 'ALTERNATIVE_ALLELE_SNP'
DGRP_ENTRY_REFERENCE_ALLELE_INS = 'REFERENCE_ALLELE_INS'
DGRP_ENTRY_ALTERNATIVE_ALLELE_INS = 'ALTERNATIVE_ALLELE_INS'
DGRP_ENTRY_REFERENCE_ALLELE_DEL = 'REFERENCE_ALLELE_DEL'
DGRP_ENTRY_ALTERNATIVE_ALLELE_DEL = 'ALTERNATIVE_ALLELE_DEL'
DGRP_ENTRY_REFERENCE_ALLELE_MNP = 'REFERENCE_ALLELE_MNP'
DGRP_ENTRY_ALTERNATIVE_ALLELE_MNP = 'ALTERNATIVE_ALLELE_MNP'
DGRP_REFERENCE_ALLELE_BASE = 'Constants.DGRP_ENTRY_REFERENCE_ALLELE_'
DGRP_ALTERNATIVE_ALLELE_BASE = 'Constants.DGRP_ENTRY_ALTERNATIVE_ALLELE_'

# ########################################
#  Constants for logging
# ########################################
PATH_LOG = os.path.expanduser('~') + '/Phenosnip/' + 'execution.log'

MODE_DEBUG = logging.DEBUG
MODE_INFO = logging.INFO
MODE_WARNING = logging.WARNING
MODE_ERROR = logging.ERROR
MODE_CRITICAL = logging.CRITICAL

LOG_MODE_DEBUG = ['d', 'debug']
LOG_MODE_INFO = ['i', 'info']
LOG_MODE_WARNING = ['w', 'warning']
LOG_MODE_ERROR = ['e', 'error']
LOG_MODE_CRITICAL = ['c', 'critical']

LOG_APPEND = 'a'
LOG_NO_APPEND = 'w'

# ########################################
# Constants used to associate reference/alternate genotype
#  to mutation
# ########################################
# Constants defining methods used for the association to mutation
ADD_REF_LINE = 'mutation.add_ref_line_mutation(line_mutation)'
ADD_ALT_LINE = 'mutation.add_alt_line_mutation(line_mutation)'
ADD_UNKNOWN_LINE = 'mutation.add_unknown_line_mutation(line_mutation)'

# List of genotype type
DGRP_GENOTYPE_LIST = ['0/0', '1/1', './.']
DGRP_REF_GENOTYPE = '0/0'
DGRP_ALT_GENOTYPE = '1/1'
DGRP_UNKNOWN_GENOTYPE = './.'

# Association genotype type to method
MUTATION_GENOTYPE_ASSOCIATION = {DGRP_REF_GENOTYPE: ADD_REF_LINE,
                                 DGRP_ALT_GENOTYPE:  ADD_ALT_LINE,
                                 DGRP_UNKNOWN_GENOTYPE: ADD_UNKNOWN_LINE}

MUTATION_AFFECTING_PROTEIN = ['NON_SYNONYMOUS_START', 'EXON_DELETED', 'NON_SYNONYMOUS_CODING', 'START_GAINED', 'STOP_GAINED', 'START_LOST', 'STOP_LOST', 'CODON_DELETION', 'FRAME_SHIFT', 'CODON_INSERTION', 'CODON_CHANGE_PLUS_CODON_INSERTION', 'CODON_CHANGE_PLUS_CODON_DELETION'] 
MUTATION_INSIDE_GENE = ['CODON_CHANGE', 'EXON', 'SYNONYMOUS_STOP', 'UTR_3_PRIME', 'INTRON', 'SYNONYMOUS_CODING', 'UTR_5_PRIME']
MUTATION_OUTSIDE_GENE = ['DOWNSTREAM', 'UPSTREAM'] 
MUTATION_UNDEFINED = [ DGRP_ENTRY_ANNOTATION_UNDEFINED_EFFECT_TYPE]

MUTATION_WANTED = MUTATION_AFFECTING_PROTEIN + MUTATION_INSIDE_GENE + MUTATION_OUTSIDE_GENE + MUTATION_UNDEFINED
MUTATION_NOT_WANTED = []

# ########################################
# Constants used to manage sql database
# ########################################
# Path for sql files created by parser DGRP files.
PATH_SQL_BASE = 'sqlite:///'

PATH_SQL_TEST_FILE = '/tmp/TestSQL.sqlite'

PATH_SQL_DGRP_FILE = '/home/mathieu/DGRP2.sqlite'
PATH_SQL_DGRP_TEST_FILE = '/tmp/Test_DGRP.sqlite'

PATH_SQL_DATA_TEST_FILE = '/tmp/Test_Data_SQL.sqlite'
PATH_SQL_DATA_FILE = '/tmp/Data.sqlite'

# Path for tests files.
# TODO : change paths
PATH_DATA_TEST_FILE = os.path.expanduser('~') + '/workspace/tagc-snpnet2/phase6/test/testdata.csv'
PATH_DGRP_TEST_FILE = os.path.expanduser('~') + '/workspace/tagc-snpnet2/phase6/test/test_DGRP_file.txt'

BULK_SIZE = 10000

# ##############################################
# Constants for analyzes result
# ##############################################
DIR_RESULT_NAME = 'Phenosnip'
DIR_RESULTS = os.path.expanduser('~') + '/' + DIR_RESULT_NAME + '/'
PATH_RESULTS = DIR_RESULTS + 'results/'
IMAGES_RESULTS = PATH_RESULTS + 'images/'
IMAGES_RESULTS_TEST = IMAGES_RESULTS + 'TEST/'
PATH_REPORTS = PATH_RESULTS + 'reports/'
PATH_REPORTS_TEST = PATH_REPORTS + 'TEST/'

###############################################################################
# Constants for report images path
###############################################################################
IMAGE_VARIANT_STATS_1_PATH = IMAGES_RESULTS + 'variant_stats_1.png'
IMAGE_VARIANT_STATS_1_TEST_PATH = IMAGES_RESULTS_TEST + 'variant_stats_1_TEST.png'

IMAGE_VARIANT_STATS_2_PATH = IMAGES_RESULTS + 'variant_stats_2.png'
IMAGE_VARIANT_STATS_2_TEST_PATH = IMAGES_RESULTS_TEST + 'variant_stats_2_TEST.png'

# ########################################
# Constants relative to usage of QuickGO
# ########################################
QUICKGO_COLUMN = 'proteinSymbol, proteinID, goID, goName, aspect, evidence, proteinTaxonName'


DEFAULT_EXTRAS = ['fenced-code-blocks', 'footnotes', 'metadata', 'pyshell', 'smarty-pants', 'tag-friendly', 'wiki-tables']

# ########################################
# Constants relative to CSS
# ########################################

DEFAULT_CSS = """
html {
    font-family: Helvetica;
    font-size: 10px;
    font-weight: normal;
    color: #000000;
    background-color: transparent;
    margin: 0;
    padding: 0;
    line-height: 150%;
    border: 1px none;
    display: inline;
    width: auto;
    height: auto;
    white-space: normal;
}

div.breakafter {
  page-break-after: always;
}

b,
strong {
    font-weight: bold;
}

i,
em {
    font-style: italic;
}

u {
    text-decoration: underline;
}

s,
strike {
    text-decoration: line-through;
}

a {
    text-decoration: underline;
    color: blue;
}

ins {
    color: green;
    text-decoration: underline;
}
del {
    color: red;
    text-decoration: line-through;
}

pre,
code,
kbd,
samp,
tt {
    font-family: "Courier New";
}

h1,
h2,
h3,
h4,
h5,
h6 {font-weight:bold;
    color: #1E90FF; 
    -pdf-outline: true;
    -pdf-outline-open: false;
}

h1 {
    /*18px via YUI Fonts CSS foundation*/
    text-align: center;
    font-size:138.5%;
    -pdf-outline-level: 0;
}

h2 {
    /*16px via YUI Fonts CSS foundation*/
    font-size:123.1%;
    -pdf-outline-level: 1;
}

h3 {
    /*14px via YUI Fonts CSS foundation*/
    font-size:108%;
    -pdf-outline-level: 2;
}

h4 {
    -pdf-outline-level: 3;
}

h5 {
    -pdf-outline-level: 4;
}

h6 {
    -pdf-outline-level: 5;
}

h1,
h2,
h3,
h4,
h5,
h6,
p,
pre,
hr {
    margin:1em 0;
}

address,
blockquote,
body,
center,
dl,
dir,
div,
fieldset,
form,
h1,
h2,
h3,
h4,
h5,
h6,
hr,
isindex,
menu,
noframes,
noscript,
ol,
p,
pre,
table,
th,
tr,
td,
ul,
li,
dd,
dt,
pdftoc {
    display: block;
}

table {
}

tr,
th,
td {

    vertical-align: middle;
    width: auto;
}

th {
    text-align: center;
    font-weight: bold;
}

center {
    text-align: center;
}

big {
    font-size: 125%;
}

small {
    font-size: 75%;
}


ul {
    margin-left: 1.5em;
    list-style-type: disc;
}

ul ul {
    list-style-type: circle;
}

ul ul ul {
    list-style-type: square;
}

ol {
    list-style-type: decimal;
    margin-left: 1.5em;
}

pre {
    white-space: pre;
}

blockquote {
    margin-left: 1.5em;
    margin-right: 1.5em;
}

noscript {
    display: none;
}

.image4{
    height: 500px;
    width: 500px;
}

.image1{
    height: 300px;
    width: 300px;
}

"""
