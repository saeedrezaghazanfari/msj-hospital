#!/bin/bash
# creator: Peaka
# this file is for remove all migration files in Django application #
# this file must be in root dir of django application #


echo 
echo "# 1 => run server"
echo "# 2 => git add and commit"
echo "# 3 => make migrations and migrate db"
echo "# 4 => remove all migrations files"
echo "# 5 => remove all pycache files"
echo "# 6 => exit from manager.sh"
echo
read -p "Enter your Selection: " FLAG
echo


# run django server on port 8000
if [ $FLAG = 1 ]; then
	
	. venv/bin/activate
	python3 manage.py runserver 8000


# git add . and git commit -m "$"
elif [ $FLAG = 2 ]; then
	
	echo "Enter your comment of this Commit:"
	read COMMENT

	git add .
	echo
	git commit -m "$COMMENT"


# makemigrations and migrate db
elif [ $FLAG = 3 ]; then
	
	read -p "Your selection is 'Make Migrations & Migrate', Are you Sure? [n/Y] " SUREMENT

	if [ $SUREMENT = 'Y' ]; then

		. venv/bin/activate
		python3 manage.py makemigrations
		echo
		python3 manage.py migrate

	else
		echo "Exited!"
	fi


# delete all of 00*.py files of migrations dir
elif [ $FLAG = 4 ]; then
	
	read -p "Your selection is 'Remove Migration Files', Are you Sure? [n/Y] " SUREMENT

	if [ $SUREMENT = 'Y' ]; then

		for FILE in $(find ./hospital_*/migrations/ -type f -iname "00*.py")
		do
			rm $FILE
			echo "File '" $FILE "' is removed!"
		done

		rm -f ./db.sqlite3
		echo "File ' db.sqlite3 ' is removed!"

		echo "done!"

	else
		echo "Exited!"
	fi


# delete all of *.pyc files in this dir
elif [ $FLAG = 5 ]; then

	read -p "Your selection is 'Remove PyCache Files', Are you Sure? [n/Y] " SUREMENT

	if [ $SUREMENT = 'Y' ]; then

		for FILE in $(find ./hospital_*/__pycache__/)
		do
			rm -rf $FILE
			echo "Dir '" $FILE "' is removed!"
		done

		for FILE in $(find ./hospital_*/*/__pycache__/)
		do
			rm -rf $FILE
			echo "Dir '" $FILE "' is removed!"
		done

		rm -rf ./extentions/__pycache__/
		echo "Dir ' ./extentions/__pycache__/ ' is removed!"

		echo "done!"

	else
		echo "Exited!"
	fi

# exit from manager.sh
elif [ $FLAG = 6 ]; then

	echo "have good time!"

else
	echo "Your input is invalid!"
fi
