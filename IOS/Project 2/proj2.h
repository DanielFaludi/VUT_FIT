// --IOS Proj2 1.5.2018--

// Author: Daniel Faludi
// Login: xfalud00

#define _GNU_SOURCE
// access to lots of nonstandard GNU/Linux extension functions
// https://stackoverflow.com/questions/5582211/what-does-define-gnu-source-imply

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <signal.h>
#include <sys/mman.h>
#include <stdbool.h>

#ifdef NDEBUG
#define LOG_BUS(process_name, action) {printf("%d: %s: %s\n", (*action_counter)++, (process_name), (action));}
#define LOG_BUS_BOARD(process_name, action, waiting) {printf("%d: %s: %s: %d\n", (*action_counter)++, (process_name), (action), (waiting));}
#define LOG_RID(process_name, id, action) {printf("%d: %s %d: %s\n", (*action_counter)++, (process_name), (id), (action));}
#define LOG_RID_ENTER(process_name, id, action, waiting) {printf("%d: %s %d: %s: %d\n", (*action_counter)++, (process_name), (id), (action), (waiting));}
#else
#define LOG_BUS(process_name, action) {fprintf(f_ptr, "%d: %s: %s\n", (*action_counter)++, (process_name), (action));}
#define LOG_BUS_BOARD(process_name, action, waiting) {fprintf(f_ptr, "%d: %s: %s: %d\n", (*action_counter)++, (process_name), (action), (waiting));}
#define LOG_RID(process_name, id, action) {fprintf(f_ptr, "%d: %s %d: %s\n", (*action_counter)++, (process_name), (id), (action));}
#define LOG_RID_ENTER(process_name, id, action, waiting) {fprintf(f_ptr, "%d: %s %d: %s: %d\n", (*action_counter)++, (process_name), (id), (action), (waiting));}
#endif

// Defines for semaphores
#define MUTEX_SEM "/xfalud00_mutex"
#define BUS_SEM "/xfalud00_bus"
#define BOARDING_SEM "/xfalud00_boarding"
#define FINISH_SEM "/xfalud00_finish"
#define DONE_SEM "/xfalud00_done"
#define OUTPUT_SEM "/xfalud00_output"
#define LOCKED 0
#define UNLOCKED 1

// Global variables
sem_t *mutex, *bus, *boarding, *finish, *done, *output;
FILE *f_ptr;
int action_counter_id = 0;
int *action_counter = NULL;

// Macros
#define SLEEP(max) {usleep(max == 0 ? 0 : (rand() % max) * 1000);}
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

// Struct for riders
struct riders_struct
{
    int total;
    int waiting;
    int gen_delay;
} *riders;

// Struct for bus
struct bus_struct
{
    int capacity;
    int ride_time;
} *bus_p;

// Simulates bus (target for bus process)
void simulate_bus();

// Deallocates shared memory and semaphores
void free_resources();

// Allocates shared memory and semaphores
bool set_resources();

// Generates rider proceses
void rider_gen();

// Simulates rider (target for rider process)
void rider(int id);

// Checks if parsed argument is valid
long parse_check(const char *str);

// Parses arguments
bool argparse(int argc, char **argv);
