# Documentation of the IPK Project 1 (1. Variant: Server)

This is a simple web server providing system information using HTTP, written in Python 3.6.6 using socket (a low level networking interface). To run this script use `make run port=[port_number]` (make sure Python 3 is installed). This server supports both IPv4 and IPv6, however it is not a dual-stack server, meaning, it does not support IPv4 and IPv6 simultanously.


# Server class

Server and all it's operations are implemented as a class and it's methods. It is initialized by passing port number to it's constructor

## `Server.start_server()`

Method that is called first in order to run the server. First a `socket.getaddrinfo()` method is called from a socket module to choose an address family (IPv4 or IPv6). The first available address family will be chosen. If IPv6 is chosen, a server will not accept IPv4 traffic and vice versa. After an address family is chosen, the server will attempt to bind a host address and port (also obtained from `socket.getaddrinfo()`) to the created socket. 

If binding was successful server will start to listen for incoming connections.

> Two socket options are set, *SO_KEEPALIVE* and *SO_REUSEADDR*

## `Server._listen()`

This method marks a socket created in `Server.start_server()` as a passive socket, meaning a socket that will be used to accept an incoming connection. When a client attempts to connect to the server, a new thread
will be created in which the client will be handled.

## `Server.shutdown_server()`

Invoked by `CTRL+C`, this method terminates the server (by closing it's socket) and it's running threads. To identify which threads are currently active `threading.enumerate()` is used, which returns all currently active threads (including main thread). Each active thread is then stopped and joined with the main thread.

# ServerThread class

A class that extends `threading.Thread` class, and is created each time a new client is connected.

## `ServerThread.run()`

Main method of `ServerThread` class, implemented by an infinte loop which checks for client requests. When a client sends a request, it is received by a `socket.recv()` function and then passed to `ServerThread._process_request()` method.

## `ServerThread.stop()`

This is a method which is called on keyboard interrupt or after a Keep-Alive timeout has elapsed and is used to set `__stop` flag to True, which then terminates the infinite loop in `ServerThread.run()`.

## `ServerThread._process_request()`

Method to process HTTP request, decodes data received in `ServerThrad.run()` and determines a response based on requested URL and HTTP header. Known URLs are saved in a dictionary as keys with callables as their values, meaning every time a certain key is accessed inside a dictionary, a corresponding method is called, which then generates a response payload. After processing is done, encoded response is returned back to `ServerThread.run()` where it is sent to client.

## `ServerThread._generate_error_message()`

This method generates a response payload with an error message specified by error code and requested content type

## `ServerThread._generate_header()`

Each time a response type is determined by `ServerThread._process_request()`, this method is called to generate a corresponding HTTP response header. It takes 4 arguments: status code, content length, refresh period (_None_ if refresh parameter wasn't entered) and content type. Returns HTTP response header

## `ServerThread._hostname_response()`

This method is called when _/hostname_ URL was requested and it returns a response payload (a hostname of the server), based on a content type requested

## `ServerThread._cpu_name_response()`

Called when */cpu-name* URL was requested, invokes `lscpu` command on servers operating system and extracts a Model Name portion of the string using a regular expression. Returns response payload based on requested content type.

## `ServerThread._load_response()`

Called when */load* URL was requested (also support a refresh parameter *?refresh=x*), opens `/proc/stat` file and reads it twice (with a delay of 1 nanosecond). Then performs a calculation to obtain cpu load as a percentage. returns CPU load as a percentage in requested content type

### Sources

[Official Python 3 Documentation](https://docs.python.org/3/library/socket.html#example)
[Threaded Socket Server Tutorial](https://theembeddedlab.com/tutorials/threaded-socket-server-python/)
[CPU Load Calculation](https://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux)
