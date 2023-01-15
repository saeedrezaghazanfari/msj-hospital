#!/bin/bash
# creator: Peaka
# this file is for remove all migration files in Django application #
# this file must be in root dir of django application #


echo "\nEnter your Selection:"
echo "# 1 => remove all migrations files"
echo "# 2 => remove all pycache files"
read -p "Enter your Selection: " FLAG


# delete all of 00*.py files of migrations dir
if [ $FLAG = 1 ]; then
	
	read -p "Your selection is 'Remove Migration Files', Are you Sure? [n/Y] " SUREMENT

	if [ $SUREMENT = 'Y' ]; then

		for FILE in $(find ./hospital_*/migrations/ -type f -iname "00*.py")
		do
			# rm $FILE
			echo "File '" $FILE "' is removed!"
		done
		echo "done!"

	else
		echo "Exited!"
	fi


# delete all of *.pyc files in this dir
elif [ $FLAG = 2 ]; then

	read -p "Your selection is 'Remove PyCache Files', Are you Sure? [n/Y] " SUREMENT

	if [ $SUREMENT = 'Y' ]; then

		for FILE in $(find ./hospital_*/*/__pycache__/ -type f -iname "*.pyc")
		do
			# rm $FILE
			echo "File '" $FILE "' is removed!"
		done
		echo "done!"

	else
		echo "Exited!"
	fi


else
	echo "Your input is invalid!"
fi
