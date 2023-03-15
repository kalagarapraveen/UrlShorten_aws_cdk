rm -rf ./bit_layer
mkdir ./bit_layer
mkdir ./bit_layer/python
Echo 'Installing dependencies for bit layer'
python3 -m pip install --force-reinstall -t ./bit_layer/python -r requirements-bit.txt