# Aiohttp + Taskiq example

This example uses postgresql as a database, AioHTTP as a framework to serve requests.
We provide docker-compose file to easily start the application.

We use nats as a main queue and redis for result backend for redis.

To run the application, type:

```bash
docker-compose up --build
```

After the startup, head to http://localhost:8080/swagger, try different endpoints and check logs to see that everything works
as expected.