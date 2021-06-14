#!/bin/sh

year=2018

# must be 1 or 5
horizon=1

url="https://www2.census.gov/programs-surveys/acs/data/pums/${year}/${horizon}-Year/"

download_dir="${year}/${horizon}-Year/"

states="
ak
al
ar
az
ca
co
ct
dc
de
fl
ga
hi
ia
id
il
in
ks
ky
la
ma
md
me
mi
mn
mo
ms
mt
nc
nd
ne
nh
nj
nm
nv
ny
oh
ok
or
pa
pr
ri
sc
sd
tn
tx
ut
va
vt
wa
wi
wv
wy
"

# Download state files

download_states_data()
{
  for state in $states
  do
    wget "${url}csv_h${state}.zip" -P $download_dir
    unzip -o "${download_dir}csv_h${state}.zip" -d $download_dir
    wget "${url}csv_p${state}.zip" -P $download_dir
    unzip -o "${download_dir}csv_p${state}.zip" -d $download_dir
  done
}

# Download US wide files

download_us_data()
{
  wget "${url}csv_pus.zip" -P $download_dir
  wget "${url}csv_hus.zip" -P $download_dir
}

mkdir -p $download_dir
download_states_data
download_us_data
