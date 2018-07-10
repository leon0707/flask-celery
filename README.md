# Flask and celery

This app has two parts: client and worker

1. The Celery client. This is used to issue background jobs. When working with Flask, the client runs with the Flask application.
2. The Celery workers. These are the processes that run the background jobs. Celery supports local and remote workers, so you can start with a single worker running on the same machine as the Flask server, and later add more workers as the needs of your application grow.
3. The message broker. The client communicates with the the workers through a message queue, and Celery supports several ways to implement these queues. The most commonly used brokers are RabbitMQ and Redis.

1. broker
RabbitMQ
```
brew install rabbitmq
sudo rabbitmq-server -detached
sudo rabbitmqctl status
sudo rabbitmqctl stop # stop the rabbitmq
```
RabbitMQ has a default user guest, but a new user is needed for remote access

`sudo rabbitmqctl add_user myuser mypassword`

a virtual host and allow that user access to that virtual host

`sudo rabbitmqctl add_vhost myvhost`

`sudo rabbitmqctl set_user_tags myuser mytag`

`sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"`

add `PATH=$PATH:/usr/local/sbin` into the shell if needed

set hostname `sudo scutil --set HostName <workspace.local>`. Then add that host name to /etc/hosts
`127.0.0.1       workspace.local`


Install virtual environment and packages in the requirements file and open 2 terminals

1. worker
move into the worker dir and start the worker
`celery worker -A worker --loglevel=info`

2. client
move into the client dir
`flask run`


The client sends the name of the task and arguments to the worker via broker.

The worker receives the task and arguments, then run the task and keep updating the task record in redis

The client keep checking the record from redis every second until the task is finished.
