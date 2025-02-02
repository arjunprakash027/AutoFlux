#!/bin/bash
# spark/entrypoint.sh

# Start Spark wroker
/spark/sbin/start-worker.sh spark://spark-server:7077

# Keep container alive
tail -f /dev/null