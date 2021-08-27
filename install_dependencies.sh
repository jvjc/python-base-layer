mkdir -p ./layer/python
rm -rf ./layer/python/*
cd ./layer/python
pip install -r ../../requirements.txt -t .
cd ../..
cp -r src/* ./layer/python
