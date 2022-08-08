#! /bin/sh

shared_fils='utils.py models.py db.py'

function create_lambda_zip_file() {
    echo "Creating lambda zip file " $1
    sleep 1
    cd package
    zip -q ../$1.zip -r .
    cd ..
    zip -q $1.zip $1.py $shared_fils
    echo "Done creating lambda zip file " $1
}
# install all the dependencies
pip install -r requirements.prod.txt --target ./package
# run in parallel
create_lambda_zip_file query &
create_lambda_zip_file booking &
create_lambda_zip_file update_db &

wait
echo "Done creating all lambda zip files"