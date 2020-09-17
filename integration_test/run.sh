# start server
cd ../server && sh run.sh

# start node maastro
cd ../maastro && sh run.sh

# start node MUMC
cd ../mumc && sh run.sh

# back to integration test
cd ../integration_test

python3 -m venv ./env
env/bin/pip install -r requirements.txt
env/bin/python test.py -v

exitCode=$?

# stop server
cd ../server && sh teardown.sh

# stop maastro node
cd ../maastro && sh stop.sh

# stop MUMC node
cd ../mumc && sh stop.sh

# back to integration test
cd ../integration_test

cat testResult.txt
exit $exitCode