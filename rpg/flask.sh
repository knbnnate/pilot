COMMAND=${1:-start}
shift
APP_NAME=${1:-hello}
shift
BIND_ADDR=${1:-0.0.0.0}
shift
BIND_PORT=${1:-5000}
shift
FLASK_APP=${APP_NAME}.py
ID=${APP_NAME}_${BIND_ADDR}_${BIND_PORT}
if [ ! -d var ] ; then
  mkdir var
fi
PIDFILE=var/flask_${ID}.pid
ERR=var/flask_${ID}.err
OUT=var/flask_${ID}.out
for f in ${PIDFILE} ${ERR} ${OUT} ; do
  if [ ! -f ${f} ] ; then
    touch ${f}
  fi
done
if [ "${COMMAND}" == start ] ; then
  if [ -z "$(cat ${PIDFILE})" ] ; then
    FLASK_APP=${FLASK_APP} flask run --host=${BIND_ADDR} --port=${BIND_PORT} > ${OUT} 2> ${ERR} &
    FLASK_PID=${!}
    echo Started ${FLASK_APP} as pid ${FLASK_PID}
    echo ${FLASK_PID} > ${PIDFILE}
  else
    echo ${PIDFILE} contains $(cat ${PIDFILE}) - flask already running?
  fi
elif [ "${COMMAND}" == stop ] ; then
  if [ -n "$(cat ${PIDFILE})" ] ; then
    kill -9 $(cat ${PIDFILE})
    cp /dev/null ${PIDFILE}
  else
    echo ${PIDFILE} empty - flask not running?
  fi
elif [ "${COMMAND}" == status ] ; then
  if [ -n "$(cat ${PIDFILE})" ] ; then
    tail ${ERR}
    lsof -p $(cat ${PIDFILE}) | head -n1
    if [ "${BIND_ADDR}" == 0.0.0.0 ] ; then
      lsof -iTCP -sTCP:LISTEN | grep flask | grep "*:${BIND_PORT}"
    elif [ "${BIND_ADDR}" == 127.0.0.1 ] ; then
      lsof -iTCP -sTCP:LISTEN | grep flask | grep "localhost:${BIND_PORT}"
    else
      lsof -iTCP -sTCP:LISTEN | grep flask | grep "${BIND_ADDR}:${BIND_PORT}"
    fi
  else
    echo ${PIDFILE} empty - flask not running?
  fi
elif [ "${COMMAND}" == wipe ] ; then
  for f in ${PIDFILE} ${ERR} ${OUT} ; do
    if [ -f ${f} ] ; then
      rm -fv ${f}
    fi
  done
fi
