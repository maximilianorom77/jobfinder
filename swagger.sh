PROJECT=jobfinder
CONTAINER_NAME=swagger-ui-$PROJECT

function swagger_run() {
    docker run \
           -p 80:8080 \
           -e SWAGGER_JSON=/src/openapi.yaml \
           -v $PWD:/src \
           --name $CONTAINER_NAME \
           --network host \
           swaggerapi/swagger-ui
}

function swagger_rm() {
    docker rm $CONTAINER_NAME
}

function swagger_stop() {
    docker stop $CONTAINER_NAME
}

function swagger_shell() {
    docker exec -it $CONTAINER_NAME sh
}

case "$1" in
    run)
        swagger_run
        ;;
    stop)
        swagger_stop
        ;;
    rm)
        swagger_rm
        ;;
    shell)
        swagger_shell
        ;;
    *)
        echo "commands: run|stop|shell"
esac
