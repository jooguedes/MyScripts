#!/bin/bash
# Usage: ./extrair_estrutura.sh input.sql
input_file=$1
echo "" > estrutura.sql
sed -n '/-- Table structure for table/,/-- Dumping data for table/p' $input_file > estrutura.sql