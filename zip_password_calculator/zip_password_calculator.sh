#!/bin/bash

ELEMENTS="ro.product.model ro.product.brand ro.product.name ro.product.device ro.product.board ro.product.cpu.abi ro.product.cpu.abi2 ro.product.manufacturer ro.product.locale.language ro.product.locale.region"


HELP() {
	echo -e "Usage: $0 FILENAME\n\nFILENAME should be a 'build.prop' file containing the following elements:" 
	for x in $ELEMENTS; do echo -e "\t$x"; done

}

if [ $# -ne 1 ]; then
	HELP
	exit 1
fi

if [ ! -f $1 ]; then
	HELP
	exit 2
fi


INFILE="$1"

for element in $ELEMENTS; do PROPS="$PROPS`grep ${element}= $INFILE`"; done

HASH1=`echo -n $PROPS | sha512sum | tr a-z A-Z | awk '{print $1}'`

HASH2=`echo -n $HASH1 | sha512sum | tr a-z A-Z | awk '{print $1}'`

echo $HASH2 | cut -c 11-38

