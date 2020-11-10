#/bin/bash
OIFS="$IFS"
IFS=$'\n'

if [ -f "dataset_ddr/index.txt" ]; then
	rm dataset_ddr/index.txt
fi

touch index.txt

for f in $(find ./dataset_ddr/ -name *.pkl); do
	STR=${f:14}
	echo ${STR%.*} >> dataset_ddr/index.txt
done

IFS="$OIFS"
