#!/usr/local/bin/python3.6

# Author: Daniel Faludi
# IPK Project 1 Web Server

# To see how threads are created and terminated set logging.DEBUG in logging.basicConfig() in __main__ function

import subprocess # For calling OS functions (such as lscpu)
import threading # For multi-threading
import logging # For logging server events (you can set logging level to CRITICAL to only see error messages)
import select # Access to select() unix function
import socket # Low-level networking interface
import signal # For processing signals such as keyboard interrupt
import time # Needed for sleep() operations
import json # For correct json formatting
import sys # For exitting and accessing arguments passed to the script
import re # Regular expressions

# Hostname
HOST = socket.gethostname() # Returns hostname of a server

class ServerThread(threading.Thread):
    """ Thread for a new client connection """

    def __init__(self, address, conn):
        """ Constructor (also initializes superclass) """

        threading.Thread.__init__(self)
        self.address = address
        self.conn = conn
        logger.debug("[+] New server thread started for client {client}".format(client=address))

    def run(self):
        """ 
        Recieve data and close connection after keep-alive timeout elapsed
        Inspired by https://theembeddedlab.com/tutorials/threaded-socket-server-python/ 
        """
        
        self.__stop = False
        while not self.__stop: # Run until timeout elapses or until keyboard interrupt has been detected
            if self.conn:
                try:
                    rdy_read, rdy_write, sock_err = select.select([self.conn,], [self.conn,], [], 5) # Monitor multiple file descriptors, wait until one or more of the file descriptors are "ready" for some I/O operation
                except:
                    logger.critical("Select() failed on socket with client {ip_add}".format(ip_add=self.address))
                    self.stop() # Set __stop to True which will break this while loop
                    return
            
                if len(rdy_read) > 0:
                    raw_data = self.conn.recv(1024) # Recieve data from client (presumably HTTP request) 

                    if len(raw_data) == 0: # If empty request was recieved (can be triggered when keep-alive timeout has elapsed)
                        self.stop()
                    else:
                        response = self._process_request(raw_data) # Process request
                        self.conn.send(response) # Send response
            else:
                logger.critical("Client not connected, can't recieve data")
                self.stop()
        self.close()

    def stop(self):
        self.__stop = True

    def close(self):
        if self.conn:
            logger.debug("Closing connection with {ip_add}".format(ip_add=self.address))
            self.conn.close() # Close the client socket (either after an error or after keep-alive timeout has elapsed)
            logger.debug("Closed the socket")

    def _process_request(self, raw_data):
        """ Decode request and return requested data """

        status_code = {
            "Not Found": 404,
            "Not Allowed": 405,
            "Not Acceptable": 406,
            "OK": 200,
        }

        data = raw_data.decode()
        parameter = None
        refresh_period = None
        resp_type = ''

        req_method = data.split(' ')[0] # Split data by space, take first string
        logger.debug("Recieved {req_m} request".format(req_m=req_method))

        if(req_method != "GET"): # If different method than GET was requested
            logger.info("Serving 405 Method Not Allowed")
            resp_message = b"405 Method Not Allowed" # Sent in plain text since Accept field has not been read at this point
            resp_header = self._generate_header(status_code["Not Allowed"], len(resp_message), refresh_period, resp_type="text/plain") # Return error response if other method than GET was requested
            return resp_header.encode() + resp_message

        req_accept = re.search(r"Accept:(.*)", str(data)) # Regex to match Accept field
        if not req_accept: # If Accept field was not in request
            resp_type = "text/plain" # Send default response content-type
        elif re.search(r"(text\/plain)", str(req_accept.group(1))) is not None: # Look for text/plain in Accept field
            resp_type = "text/plain" # If found, response content-type will be text/plain
        elif re.search(r"(application\/json)", str(req_accept.group(1))) is not None: # Look for application/json in Accept field
            resp_type = "application/json" # If found, response content-type will be application/json
        elif re.search(r"(\*\/\*)", str(req_accept.group(1))) is not None: # Look for */*
            resp_type = "text/plain" # If found, response content-type will be text/plain (*/* means accept any MIME)
        else: # Generate 406 Not Acceptable if unsupported content type was requested
            logger.info("Serving 406 Not Acceptable")
            resp_message = b"" # Sending empty response payload since requested content type is not acceptable
            resp_header = self._generate_header(status_code["Not Acceptable"], len(resp_message), refresh_period, resp_type)
            return resp_header.encode() + resp_message

        logger.debug("Processing {req_m} request".format(req_m=req_method))

        url = data.split(' ')[1] # Split data by space, take second string
        if '?' in url:
            req_page, parameter = tuple(url.split('?')) # If parameter was entered save it in a different variable
        else:
            req_page = url

        # Page directory as dictionary with callable values (works like a switch statement)
        page_dir = {
            "/hostname": self._hostname_response,
            "/cpu-name": self._cpu_name_response,
            "/load": self._load_response,
        }

        match = [k for k in page_dir if k == req_page] # Check whether requested page exists

        if parameter is not None: # Check whether parameter was entered
            name = parameter.split('=')[0]
            if name == "refresh" and req_page == "/load": # Only accept refresh parameter entered to /load page request
                try:
                    refresh_period = int(parameter.split('=')[1])
                except ValueError:
                    logging.info("Refresh argument was entered incorrectly, ignoring")
                    refresh_period = None
            else:
                logger.info("Ignoring unknwown parameter: {p}".format(p=parameter)) # Ignore any other parameter

        if not match: # If requested page was not found, send appropriate status code
            logger.info("Serving 404 Not Found")
            resp_message = self._generate_error_message(resp_type, status_code["Not Found"], status_code)
            resp_header = self._generate_header(status_code["Not Found"], len(resp_message), refresh_period, resp_type) # Return error response if requested page was not found
            return resp_header.encode() + resp_message
        else: # Server requested page
            logger.info("Serving {p}".format(p=req_page))
            resp_message = page_dir[req_page](resp_type)
            resp_header = self._generate_header(status_code["OK"], len(resp_message), refresh_period, resp_type) # Return 200 OK response if everything went correctly
            return resp_header.encode() + resp_message

    def _generate_error_message(self, resp_type, error_code, status_code):
        """ Generate error massage payload based on content-type requested """

        error = ''
        for k, v in status_code.items(): # Iterate through dictionary items
            if v == error_code: # If specified error_code matches a value in dictionary
                error = "{} {}".format(error_code, k) # Construct a corresponding error message

        # Return error as either text/plain or application/json
        if resp_type == "text/plain":
            return error.encode()
        if resp_type == "application/json":
            return json.dumps({"status": error}).encode()

    def _generate_header(self, resp_code, content_length, refresh_period, resp_type):
        """ Generate a response header """
        header = ''

        # Generate status code
        if resp_code == 406: # Not Acceptable
            header += "HTTP/1.1 406 Not Acceptable\n"
        elif resp_code == 405: # Not Allowed
            header += "HTTP/1.1 405 Method Not Allowed\n"
        elif resp_code == 404: # Not Found
            header += "HTTP/1.1 404 Not Found\n"
        else: # 200 OK
            header += "HTTP/1.1 200 OK\n"
    
        if refresh_period is not None:
            if(refresh_period >= 0):
                header += "Refresh: {rp}\n".format(rp=refresh_period)
            else:
                logging.info("Refresh parameter was entered incorrectly, ignoring")
                    
        # Generate other important parameters for HTTP 1.1
        header += "Connection: Keep-Alive\n" # Default for HTTP 1.1
        if len(resp_type) > 0: # In case of status code 406 response content-type cannot be determined
            header += "Content-Type: {r_type}\n".format(r_type=resp_type) # Content type chosen in _process_request method
        header += "Content-Length: {len}\n".format(len=content_length) # Length of response payload
        header += "Keep-Alive: timeout=10, max=20\n\n" # Wait 10 seconds for another request, close connection when no more requests recieved (maximum of 20 requests)

        return header

    def _hostname_response(self, resp_type):
        """ Content of /hostname """

        response_data = HOST

        # Return hostname as application/json or text/plain 
        if resp_type == "application/json":
            return json.dumps({"hostname": response_data}).encode()
        else:
            return response_data.encode()

    def _cpu_name_response(self, resp_type):
        """ Content of /cpu-name """

        proc = subprocess.Popen("lscpu", stdout=subprocess.PIPE) # Subprocess to invoke lscpu command
        output = proc.stdout.read()
        match = re.search(r"Model name:\s*(.+?(?=\\n))", str(output)) # Regex to match CPU name
        cpu_name = match.group(1)

        response_data = "{cpu}".format(cpu=cpu_name)

        # Return result as application/json or text/plain
        if resp_type == "application/json":
            return json.dumps({"cpu_name": response_data}).encode()
        else:
            return response_data.encode()

    def _load_response(self, resp_type):
        """ Content of /load """

        with open("/proc/stat") as f: # Open /proc/stat
            data_prev = f.readline() # Read first line
            f.seek(0) # Reset offset to beginning of the file
            time.sleep(0.1) # Sleep for 100 milliseconds
            data_curr = f.readline() # Read first line again

        # Fix formatting of the file
        data_prev = data_prev.split()[1:11]

        data_curr = data_curr.split()[1:11]

        # Convert strings in list to floats
        data_prev = list(map(float, data_prev))
        data_curr = list(map(float, data_curr))

        # Calculate CPU load
        # https://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux

        # prevIdle + prevIOWait
        prev_idle = data_prev[3] + data_prev[4]

        # Idle + IOWait
        idle = data_curr[3] + data_curr[4]

        # prevUser + prevNice + prevSystem + prevIRQ + prevSoftIRQ + prevSteal
        prev_non_idle = data_prev[0] + data_prev[1] + data_prev[2] + data_prev[5] + data_prev[6] + data_prev[7]

        # User + Nice + System + IRQ + SoftIRQ + Steal
        non_idle = data_curr[0] + data_curr[1] + data_curr[2] + data_curr[5] + data_curr[6] + data_curr[7]

        prev_total = prev_idle + prev_non_idle
        total = idle + non_idle

        totald = total - prev_total
        idled = idle - prev_idle

        cpu_percentage = ((totald - idled)/totald) * 100 # multiply by 100 to get percentage

        # Return result as percentage as application/json or text/plain
        response_data = "{cpu_usage}%".format(cpu_usage=round(cpu_percentage, 2))

        if resp_type == "application/json":
            return json.dumps({"load": response_data}).encode()
        else:
            return response_data.encode()

class Server(object):
    """ Basic web server for handling multi-client connections """

    def __init__(self, port):
        """ Server constructor """
        self.port = port
        self.host = HOST
        print("To shutdown server use CTRL+C")

    def start_server(self):
        """ 
        Binds host and port to created socket, supports both IPv4 and IPv6
        as per : https://docs.python.org/3/library/socket.html#example
        """

        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socket.SOCK_STREAM) # Create a new socket, socket family is chosen by getaddrinfo output, the socket type is hardcoded (TCP)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) # Enable sending of keep-alive messages on connection-oriented sockets
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of local addresses
            except OSError: # If creating a socket fails try again with different settings
                self.sock = None
                continue
            try:
                self.sock.bind(sa) # Bind the socket to address (obtained from getaddrinfo)
            except OSError:
                self.sock.close() # Close the socket if an error occurs
                self.sock = None
                continue
            break
        if self.sock is None: # If creating or binding a socket was not successful terminate the script with return value 1
            logger.critical("Could not open socket")
            sys.exit(1)

        self._listen() # call to _listen method

    def _listen(self):
        """ Accept incoming connection, create new subthread to handle communication """

        logging.info("WAITING FOR CONNECTIONS")

        while True:
            self.sock.listen(5) # Mark the socket as a passive socket (a socket that will be used to accept incoming connection)
            self.sock.settimeout(1) # Set 1 second timeout on blocking socket operations
            try:
                (conn, address) = self.sock.accept() # Accepts connection, return new socket (conn) and address (split to ip and port)
            except socket.timeout:
                conn = None
            
            if(conn):
                new_thread = ServerThread(address, conn) # Once a connection was accepted a communication can start on a new subthread
                new_thread.start() # Start a new server thread

    def shutdown_server(self):
        """ Shutdown server on CTRL+C """

        subthread_count = threading.active_count() - 1 # subtract 1 because active_count will count main thread too which is not a subthread
        logging.debug("Terminating with {t_count} active subthread(s)".format(t_count=subthread_count))
        for t in threading.enumerate(): # threading.enumerate() contains only active threads
            if t is threading.main_thread(): # Skip main thread
                continue
            logger.debug("[-] Terminating {t}".format(t=t.name))
            t.stop() # Call stop method of ServerThread class
            t.join() # Join thread with main thread

        try:
            logging.info("SHUTTING DOWN SERVER")
            self.sock.shutdown(socket.SHUT_RDWR) # Shutdown socket
            self.sock.close() # Close socket
            self.sock = None
        except OSError:
            logger.critical("Couldn't shutdown the server")
            sys.exit(1) # Exit with return value 1 if server is unable to shutdown

if __name__ == "__main__":
    """ Main function """

    FORMAT = '%(levelname)s - %(asctime)s %(threadName)s --> %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%H:%M:%S') # Configure the logging module (to see how threads are managed change logging.INFO to logging.DEBUG)
    logger = logging.getLogger(__name__) # Initialize logger

    if len(sys.argv) != 2:
        logger.critical("Missing or too many arguments")
        sys.exit(1)
    else:
        try:
            port = int(sys.argv[1])
        except ValueError as msg:
            logging.critical("Invalid port argument entered")
            sys.exit(1)
        if(port not in range(0,65536)): # Must be an existing port number
            logging.critical("Specified argument is not a valid port number")
            sys.exit(1)

    def shutdown(sig, unused):
        server.shutdown_server() # Call to shutdown_server method of Server class
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown) # Shutdown server on CTRL+C
    server = Server(port) # Create new Server object with specified port number
    server.start_server() # Start server
