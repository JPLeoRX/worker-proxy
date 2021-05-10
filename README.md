


# Basic workflow

So this is how our proxy works:

* Proxy server app is exposed. It gets called by someone from the web, intercepts the request, pushes it into RabbitMQ and waits to receive a response.

* Your worker app is run without any exposure into the web (meaning that it's run from your internal network, from your local machine etc). And your proxy client app is launched alongside the worker. Proxy client must be able to make HTTP requests to the worker. But they both can remain private, run from your local machine. 

* Proxy client app listens to new incoming requests, forwards them to the worker, and then pushes the result into RabbitMQ.

* After which proxy server receives the response, and returns it back to the caller. 



We support running multiple workers & clients to better distribute the load. You can find one example that illustrates this.



# Examples

To let you quickly experience and test the example cases for yourself we implemented them with docker-compose.

### Cases:
1. `example_1_basic` Basic example that spins up RabbitMQ, Proxy Server, Proxy Client and the Worker. Then you can access the worker's REST API through the proxy server.

2. `example_2_multiple_workers` Same idea as the previous one, but now with multiple workers/clients.

### How to run examples:

You should build the worker's dockerfile first `docker build -t worker-proxy-sample-service .`

Then just go into the example you want and run `docker-compose up -d`, and when done don't forget to shut down by `docker-compose down`



 
# DockerHub
[Server part DockerHub](https://hub.docker.com/repository/docker/jpleorx/worker-proxy-server)

[Client part DockerHub](https://hub.docker.com/repository/docker/jpleorx/worker-proxy-client) 
