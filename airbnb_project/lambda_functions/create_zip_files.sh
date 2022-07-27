#! /bin/sh

shared_fils='utils.py models.py db.py'
should_install_packages=$1
function create_lambda_zip_file() {
    echo "Creating lambda zip file " $1
    zip -q $1.zip $1.py $shared_fils
    echo "Done creating lambda zip file " $1
}
# install all the dependencies if should_install_packages
if [ "$should_install_packages" = "--install" ]; then
    pip install -U pip
    pip install -r requirements.prod.txt --target ./package/python
    cd package
    zip -q -r ../package.zip .
    cd ..
fi

# run in parallel
create_lambda_zip_file query &
create_lambda_zip_file booking &
create_lambda_zip_file update_db &

wait
echo "Done creating all lambda zip files"
