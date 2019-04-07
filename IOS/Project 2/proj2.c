// --IOS Proj2 1.5.2018--

// Author: Daniel Faludi
// Login: xfalud00

#include "proj2.h"

int main(int argc, char **argv)
{
    setbuf(stdout, NULL);

    if(set_resources() == false)
    {
        free_resources();
        exit(EXIT_FAILURE);
    }

    if(argparse(argc, argv) == false)
    {
        free_resources();
        exit(EXIT_FAILURE);
    }

    setbuf(f_ptr, NULL);

    pid_t process_pid = fork();

    if(process_pid == 0)
    {
        rider_gen();
    }
    else if(process_pid > 0)
    {
        simulate_bus();
    }
    else
    {
        perror("fork error");
        free_resources();
        exit(EXIT_FAILURE);
    }

    free_resources();

    return EXIT_SUCCESS;
}

long parse_check(const char *str)
{
    char *end_ptr;

    long val = strtol(str, &end_ptr, 10);
    if(*end_ptr != '\0')
    {
        fprintf(stderr, "strtol error\n");
        return -1;
    }
    else
    {
        return val;
    }
}

bool argparse(int argc, char **argv)
{
    if(argc != 5)
    {
        fprintf(stderr, "wrong arguments format\n");
        return false;
    }
    
    int val_array[4];
    for(int i = 0;i < 4;i++)
    {
        val_array[i] = parse_check(argv[i + 1]);
    }
    
    int total_arg = val_array[0];
    int cap = val_array[1];
    int delay = val_array[2];
    int ride = val_array[3];

    if(total_arg <= 0 || cap <= 0 || delay < 0 || delay >= 1000 || ride < 0 || ride >= 1000)
    {
        fprintf(stderr, "wrong argument entered\n");
        return false;
    }

    *bus_p = (struct bus_struct)
    {
        .capacity = cap,
        .ride_time = ride
    };

    *riders = (struct riders_struct)
    {
        .total = total_arg,
        .gen_delay = delay,
        .waiting = 0
    };

    return true;
}

bool set_resources()
{
    f_ptr = fopen("proj2.out", "w");

    if((action_counter_id = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
        perror("shmget error");
        return false;
    }

    if((action_counter = shmat(action_counter_id, NULL, 0)) == NULL)
    {
        perror("shmat error");
        return false;
    }
    else
    {
        *action_counter = 1;
    }

    riders = mmap(NULL, sizeof(*(riders)), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    
    bus_p = mmap(NULL, sizeof(*(bus_p)), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    if((mutex = sem_open(MUTEX_SEM, O_CREAT | O_EXCL, 0666, UNLOCKED)) == SEM_FAILED)
    {
        perror("sem_open error (\"mutex\" sem)");
        return false;
    }

    if((bus = sem_open(BUS_SEM, O_CREAT | O_EXCL, 0666, LOCKED)) == SEM_FAILED)
    {
        perror("sem_open error (\"bus\" sem)");
        return false;
    }

    if((boarding = sem_open(BOARDING_SEM, O_CREAT | O_EXCL, 0666, LOCKED)) == SEM_FAILED)
    {
        perror("sem_open error (\"boarding\" sem)");
        return false;
    }

    if((finish = sem_open(FINISH_SEM, O_CREAT | O_EXCL, 0666, LOCKED)) == SEM_FAILED)
    {
        perror("sem_open error (\"finish\" sem)");
        return false;
    }

    if((done = sem_open(DONE_SEM, O_CREAT | O_EXCL, 0666, LOCKED)) == SEM_FAILED)
    {
        perror("sem_open error (\"done\" sem)");
        return false;
    }

    if((output = sem_open(OUTPUT_SEM, O_CREAT | O_EXCL, 0666, UNLOCKED)) == SEM_FAILED)
    {
        perror("sem_open error (\"done\" sem)");
        return false;
    }

    return true;
}

// Semaphores inspired by "The Little Book of Semaphores" by Allen B. Downey
// Excessive usage of output semaphore to ensure correct line numbering
void simulate_bus()
{
    sem_wait(output);
    LOG_BUS("BUS", "start");
    sem_post(output);

    while(riders->total > 0)
    {
        sem_wait(output);
        LOG_BUS("BUS", "arrival");
        sem_post(output);

        sem_wait(mutex);

        if(riders->waiting > 0)
        {
            sem_wait(output);
            LOG_BUS_BOARD("BUS", "start boarding", riders->waiting);
            sem_post(output);

            int n = MIN(riders->waiting, bus_p->capacity);
            for(int i = 0;i < n;i++)
            {
                sem_post(bus);
                sem_wait(boarding);
            }
            riders->waiting = MAX((riders->waiting - bus_p->capacity), 0);

            sem_wait(output);
            LOG_BUS_BOARD("BUS", "end boarding", riders->waiting);
            sem_post(output);

            sem_wait(output);
            LOG_BUS("BUS", "depart");
            sem_post(output);

            sem_post(mutex);         
            SLEEP(bus_p->ride_time);

            sem_wait(output);
            LOG_BUS("BUS", "end");
            sem_post(output);

            for(int i = 0;i < n;i++)
            {
                sem_post(done);
                sem_wait(finish);
            }
        }
        else
        {
            sem_wait(output);
            LOG_BUS("BUS", "depart");
            sem_post(output);

            sem_post(mutex);
            SLEEP(bus_p->ride_time);
            
            sem_wait(output);
            LOG_BUS("BUS", "end");
            sem_post(output);
        }
    }

    sem_wait(output);
    LOG_BUS("BUS", "finish");
    sem_post(output);
}

void rider(int id)
{
    sem_wait(output);
    LOG_RID("RID", id, "start");
    sem_post(output);

    sem_wait(mutex);
        ++(riders->waiting);
        sem_wait(output);
        LOG_RID_ENTER("RID", id, "enter", riders->waiting);
        sem_post(output);
    sem_post(mutex);

    sem_wait(bus);
        sem_wait(output);
        LOG_RID("RID", id, "boarding");
        sem_post(output);
    sem_post(boarding);

    sem_wait(done);
        sem_wait(output);
        LOG_RID("RID", id, "finish");
        sem_post(output);
        --(riders->total);
    sem_post(finish);

    exit(EXIT_SUCCESS);
}

void rider_gen()
{
    pid_t rider_process;
    int total = riders->total;

    for(int id = 1;id <= total;id++)
    {
        rider_process = fork();
        if(rider_process == 0)
        {
            rider(id);
        }
        if(rider_process < 0)
        {
            perror("fork error");
            exit(EXIT_FAILURE);
        }
        SLEEP(riders->gen_delay);
    }
}

void free_resources()
{
    if (f_ptr != NULL)
    {
        fclose(f_ptr);
    }

    shmctl(action_counter_id, IPC_RMID, NULL);
    munmap((riders), sizeof(riders));
    munmap((bus_p), sizeof(bus_p));

    sem_close(mutex);
    sem_close(bus);
    sem_close(boarding);
    sem_close(finish);
    sem_close(done);
    sem_close(output);

    sem_unlink(MUTEX_SEM);
    sem_unlink(BUS_SEM);
    sem_unlink(BOARDING_SEM);
    sem_unlink(FINISH_SEM);
    sem_unlink(DONE_SEM);
    sem_unlink(OUTPUT_SEM);
}
