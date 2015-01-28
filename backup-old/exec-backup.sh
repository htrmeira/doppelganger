#!/bin/bash

RSYNC_ARGS=""
DEST_DIR=""
SRC_DIR=""
LINK_DIR_NAME=""
INCREMENTAL=false
PRESERVE=false
DST_DIR_NAME=backup-$(date +%Y%m%d%H%M%S)
COMMAND="rsync --delete -r"

function print_ok {
	echo -e "$1 ............. \e[32mOK"; tput sgr0
}

function print_fail {
	echo -e "$1 ............. \e[31mFAIL"; tput sgr0
}

## Number of incremental copies should be an argument
function rotate {
	mkdir -p $DEST_DIR/$DST_DIR_NAME
}



function check_precoditions {
	STATUS=0
	echo -n "cheking screen command"
	if [ -z `which screen` ]; then
		print_fail ""
		STATUS=1
	else
		print_ok ""
	fi
	echo -n "cheking rsync command"
	if [ -z `which rsync` ]; then
		print_fail ""
		STATUS=1
	else
		print_ok ""
	fi

	for src in $*; do
		if [ $src == "check" ]; then
			continue;
		else
			echo -n "cheking if $src exists"
			if [ -e $src ]; then
				print_ok ""
			else
			        print_fail ""
				STATUS=1
			fi
		fi
	done;
	exit $STATUS
}

function configure_params {
	next_dest_dir=false;
	next_src_dir=false;
	for param in $@; do
		if [ "$param" == "-p" ]; then
			PRESERVE=true;
		elif [ "$param" == "-i" ]; then
			INCREMENTAL=true;
		elif [ "$param" == "-d" ]; then
			next_dest_dir=true;
		elif [ $next_dest_dir == true ]; then
			DEST_DIR=$param
			next_dest_dir=false;
		elif [ "$param" == "-s" ]; then
			next_src_dir=true;
		elif [ $next_src_dir == true ]; then
			SRC_DIR="$SRC_DIR $param"
		fi;

	done;
}

function last_backup {
	if [ -e $DEST_DIR ]; then
		LINK_DIR_NAME=`ls $DEST_DIR/ | sort | tail -1`;
	fi
}

function create_comand {
	if [ $PRESERVE == true ]; then
		COMMAND="$COMMAND -Hapogtl"
	fi;
	if [ $INCREMENTAL == true ]; then
		last_backup;
		COMMAND="$COMMAND --link-dest=$DEST_DIR$LINK_DIR_NAME"
	fi;

	COMMAND="$COMMAND $SRC_DIR $DEST_DIR$DST_DIR_NAME/"
}

function print_help {
	echo "USAGE: exec-backup.sh help -> to show this help"
	echo "USAGE: exec-backup.sh check -> To check dependecies and src files and directories"
	echo "USAGE: exec-backup.sh -p [preserve attributes|OPTIONAL] -i [incremental|OPTIONAL] -d [full path to destination directory] -s [source directory] [source directory] ..."
}


function exec_sync() {
	create_comand
	echo "Doing backup to $DEST_DIR$DST_DIR_NAME"
	mkdir -p $DEST_DIR/$DST_DIR_NAME
	echo $COMMAND
	$COMMAND
	STATUS=$?;
	echo -n "Backup ended"
	if [ $STATUS == 0 ]; then
		print_ok ""
	else
		print_fail ""
		echo "But, it does not mean that the backup failed, please check your backup files"
	fi
}

case $1 in
	check)
		check_precoditions $@;
		;;
	status)
		configure_params $@
		check_status;
		;;
	help)
		print_help
		;;
	"")
		print_help
		;;
         *)
		configure_params $@
		exec_sync

esac
