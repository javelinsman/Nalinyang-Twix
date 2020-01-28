sudo docker run \
        --rm -it \
        -e PYTHONPATH=/home \
        -v $PWD:/home \
        -w /home \
        -p 8000:8000 \
        --net=host \
    main \
        $@ # all arguments