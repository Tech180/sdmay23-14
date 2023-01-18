#! /bin/sh

# prepare to kill the background processes after we ^c out of gateway
# (if we don't, then a "zombie" controls process will continue to
# flood its canbus with traffic)
catch_ctrlc() {

  ps -ef | grep icsim    | grep -v grep | awk '{print $2}' | xargs kill
  ps -ef | grep controls | grep -v grep | awk '{print $2}' | xargs kill
  echo ""
  echo "simulator background tasks have been halted"

}

trap catch_ctrlc INT

# launch the background processes
echo
echo "setting up MITM0: IC      on vcan0"
echo "                  control on vcan1"
echo "                  gateway on both"
echo

./icsim vcan0 &
./controls -X vcan1 &
python3 gw.py &

echo "launched all process for simulator"

sleep infinity

