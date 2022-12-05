#!/bin/sh
# this file is for remove all migration files in Django application #
# this file must be in root dir of django application #


for FILE in $(find ./hospital_* -type f -iname "000*.py")
do
	rm $FILE
	echo "File '" $FILE "' is removed!"
done

echo "done!"

# i'm very ...