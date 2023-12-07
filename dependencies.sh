#!bin/sh
# Recommended to run in a virtual environment Python3.12

echo "Update pip "
pip3 install --upgrade pip   &

wait

echo "Installing necessary dependencies"
pip3 install flask marshmallow pymongo flask_cors flask_swagger_ui

echo "Done!, now you can run the API on your respective port with command:"
echo "flask run --port 5001"