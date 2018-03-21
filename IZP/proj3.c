/**
 * Kostra programu pro 3. projekt IZP 2017/18
 *
 * Jednoducha shlukova analyza
 * Unweighted pair-group average
 * https://is.muni.cz/th/172767/fi_b/5739129/web/web/usrov.html
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h> // sqrtf
#include <limits.h> // INT_MAX

/*****************************************************************
 * Ladici makra. Vypnout jejich efekt lze definici makra
 * NDEBUG, napr.:
 *   a) pri prekladu argumentem prekladaci -DNDEBUG
 *   b) v souboru (na radek pred #include <assert.h>
 *      #define NDEBUG
 */
#ifdef NDEBUG
#define debug(s)
#define dfmt(s, ...)
#define dint(i)
#define dfloat(f)
#else

// vypise ladici retezec
#define debug(s) printf("- %s\n", s)

// vypise formatovany ladici vystup - pouziti podobne jako printf
#define dfmt(s, ...) printf(" - "__FILE__":%u: "s"\n",__LINE__,__VA_ARGS__)

// vypise ladici informaci o promenne - pouziti dint(identifikator_promenne)
#define dint(i) printf(" - " __FILE__ ":%u: " #i " = %d\n", __LINE__, i)

// vypise ladici informaci o promenne typu float - pouziti
// dfloat(identifikator_promenne)
#define dfloat(f) printf(" - " __FILE__ ":%u: " #f " = %g\n", __LINE__, f)

#endif

/*****************************************************************
 * Deklarace potrebnych datovych typu:
 *
 * TYTO DEKLARACE NEMENTE
 *
 *   struct obj_t - struktura objektu: identifikator a souradnice
 *   struct cluster_t - shluk objektu:
 *      pocet objektu ve shluku,
 *      kapacita shluku (pocet objektu, pro ktere je rezervovano
 *          misto v poli),
 *      ukazatel na pole shluku.
 */

struct obj_t {
    int id;
    float x;
    float y;
};

struct cluster_t {
    int size;
    int capacity;
    struct obj_t *obj;
};

/*****************************************************************
 * Deklarace potrebnych funkci.
 *
 * PROTOTYPY FUNKCI NEMENTE
 *
 * IMPLEMENTUJTE POUZE FUNKCE NA MISTECH OZNACENYCH 'TODO'
 *
 */

/*
 Inicializace shluku 'c'. Alokuje pamet pro cap objektu (kapacitu).
 Ukazatel NULL u pole objektu znamena kapacitu 0.
*/
void init_cluster(struct cluster_t *c, int cap)
{
    assert(c != NULL);
    assert(cap >= 0);

    // TODO
    c->size = 0;
    c->obj = malloc(sizeof(struct obj_t) * cap);
    if (c->obj != NULL)
    {
        c->capacity = cap;
    }
    else
    {
        c->capacity = 0;
    }
}

/*
 Odstraneni vsech objektu shluku a inicializace na prazdny shluk.
 */
void clear_cluster(struct cluster_t *c)
{
    // TODO
    free(c->obj);
    c->obj = NULL;
    c->size = 0;
    c->capacity = 0;
}

/// Chunk of cluster objects. Value recommended for reallocation.
const int CLUSTER_CHUNK = 10;

/*
 Zmena kapacity shluku 'c' na kapacitu 'new_cap'.
 */
struct cluster_t *resize_cluster(struct cluster_t *c, int new_cap)
{
    // TUTO FUNKCI NEMENTE
    assert(c);
    assert(c->capacity >= 0);
    assert(new_cap >= 0);

    if (c->capacity >= new_cap)
        return c;

    size_t size = sizeof(struct obj_t) * new_cap;

    void *arr = realloc(c->obj, size);
    if (arr == NULL)
        return NULL;

    c->obj = (struct obj_t*)arr;
    c->capacity = new_cap;
    return c;
}

/*
 Prida objekt 'obj' na konec shluku 'c'. Rozsiri shluk, pokud se do nej objekt
 nevejde.
 */
void append_cluster(struct cluster_t *c, struct obj_t obj)
{
    // TODO
    if (c->capacity <= c->size)
    {
        c = resize_cluster(c, c->capacity + CLUSTER_CHUNK);
    }
    c->obj[c->size] = obj;
    c->size++;
}

/*
 Seradi objekty ve shluku 'c' vzestupne podle jejich identifikacniho cisla.
 */
void sort_cluster(struct cluster_t *c);

/*
 Do shluku 'c1' prida objekty 'c2'. Shluk 'c1' bude v pripade nutnosti rozsiren.
 Objekty ve shluku 'c1' budou serazeny vzestupne podle identifikacniho cisla.
 Shluk 'c2' bude nezmenen.
 */
void merge_clusters(struct cluster_t *c1, struct cluster_t *c2)
{
    assert(c1 != NULL);
    assert(c2 != NULL);

    // TODO
    for (int i = 0; i < c2->size;i++)
    {
        append_cluster(c1, c2->obj[i]);
    }
    sort_cluster(c1);
}

/**********************************************************************/
/* Prace s polem shluku */

/*
 Odstrani shluk z pole shluku 'carr'. Pole shluku obsahuje 'narr' polozek
 (shluku). Shluk pro odstraneni se nachazi na indexu 'idx'. Funkce vraci novy
 pocet shluku v poli.
*/
int remove_cluster(struct cluster_t *carr, int narr, int idx)
{
    assert(idx < narr);
    assert(narr > 0);

    // TODO
    int newVal = narr - 1, i;

    clear_cluster(&carr[idx]);

    for (i = idx; i < newVal;i++)
    {
        carr[i] = carr[i + 1];
    }

    return newVal;
}

/*
 Pocita Euklidovskou vzdalenost mezi dvema objekty.
 */
float obj_distance(struct obj_t *o1, struct obj_t *o2)
{
    assert(o1 != NULL);
    assert(o2 != NULL);

    // TODO
    float res = sqrtf(powf(o1->x - o2->x, 2.0) + powf(o1->y - o2->y, 2.0));
    return res;
}

/*
 Pocita vzdalenost dvou shluku.
*/

/* 
Globalna premenna pre nastavenie metody zhlokovania
(defaultna metoda je --avg)
*/

static int premium_case = 1;

float cluster_distance(struct cluster_t *c1, struct cluster_t *c2)
{
    assert(c1 != NULL);
    assert(c1->size > 0);
    assert(c2 != NULL);
    assert(c2->size > 0);

    // TODO
    int i, j;

    // Unweighted pair-group average
    if (premium_case == 1)
    {
        float total = 0.0;

        for (i = 0;i < c1->size;i++)
        {
            for (j = 0;j < c2->size;j++)
            {
                total += obj_distance(&c1->obj[i], &c2->obj[j]);
            }
        }
        return total / (i * j);                
    }

    // Complete-linkage
    if (premium_case == 2)
    {
        float maxDistance = 0.0;
        float tmp;

        for (i = 0;i < c1->size;i++)
        {
            for (j = 0;j < c2->size;j++)
            {
                tmp = obj_distance(&c1->obj[i], &c2->obj[j]);
                if (tmp > maxDistance)
                {
                    maxDistance = tmp;
                }
            }
        }
        return maxDistance;               
    }

    // Single-linkage
    if (premium_case == 3)
    {
        float minDistance = INFINITY;
        float tmp;

        for (i = 0;i < c1->size;i++)
        {
            for (j = 0;j < c2->size;j++)
            {
                tmp = obj_distance(&c1->obj[i], &c2->obj[j]);
                if (tmp < minDistance)
                {
                    minDistance = tmp;
                }
            }
        }
        return minDistance;               
    }
    
    return 0;
}

/*
 Funkce najde dva nejblizsi shluky. V poli shluku 'carr' o velikosti 'narr'
 hleda dva nejblizsi shluky. Nalezene shluky identifikuje jejich indexy v poli
 'carr'. Funkce nalezene shluky (indexy do pole 'carr') uklada do pameti na
 adresu 'c1' resp. 'c2'.
*/
void find_neighbours(struct cluster_t *carr, int narr, int *c1, int *c2)
{
    assert(narr > 0);

    // TODO
    float minimum = INFINITY, distance;
    int i, j;

    for (i = 0;i < narr;i++)
    {
        for (j = i + 1;j < narr; j++)
        {
            distance = cluster_distance(&carr[i], &carr[j]);
            if (distance < minimum)
            {
                minimum = distance;
                *c1 = i;
                *c2 = j;
            }
        }
    }
}

// pomocna funkce pro razeni shluku
static int obj_sort_compar(const void *a, const void *b)
{
    // TUTO FUNKCI NEMENTE
    const struct obj_t *o1 = (const struct obj_t *)a;
    const struct obj_t *o2 = (const struct obj_t *)b;
    if (o1->id < o2->id) return -1;
    if (o1->id > o2->id) return 1;
    return 0;
}

/*
 Razeni objektu ve shluku vzestupne podle jejich identifikatoru.
*/
void sort_cluster(struct cluster_t *c)
{
    // TUTO FUNKCI NEMENTE
    qsort(c->obj, c->size, sizeof(struct obj_t), &obj_sort_compar);
}

/*
 Tisk shluku 'c' na stdout.
*/
void print_cluster(struct cluster_t *c)
{
    // TUTO FUNKCI NEMENTE
    for (int i = 0; i < c->size; i++)
    {
        if (i) putchar(' ');
        printf("%d[%g,%g]", c->obj[i].id, c->obj[i].x, c->obj[i].y);
    }
    putchar('\n');
}


/*
 Testuje ci sa subor zatvoril.
*/
int test_closed(FILE *f)
{
    if (fclose(f) != 0)
    {
        fprintf(stderr, "Error: file failed to close\n");
        return -1;
    }
    else
    {
        return 0;
    }
}

/*
 Ze souboru 'filename' nacte objekty. Pro kazdy objekt vytvori shluk a ulozi
 jej do pole shluku. Alokuje prostor pro pole vsech shluku a ukazatel na prvni
 polozku pole (ukalazatel na prvni shluk v alokovanem poli) ulozi do pameti,
 kam se odkazuje parametr 'arr'. Funkce vraci pocet nactenych objektu (shluku).
 V pripade nejake chyby uklada do pameti, kam se odkazuje 'arr', hodnotu NULL.
*/
int load_clusters(char *filename, struct cluster_t **arr)
{
    assert(arr != NULL);

    // TODO
    int objCount, id, x, y, i, j;
    FILE *f;
    f = fopen(filename, "r");

    if (f == NULL)
    {
        fprintf(stderr, "Error: File failed to open\n");
        *arr = NULL;
        return -1;
    }

    if (fscanf(f, "count=%d\n", &objCount) == 1)
    {
        *arr = malloc(sizeof(struct cluster_t) * objCount);
        if (*arr == NULL)
        {
            fprintf(stderr, "Error: memory allocation was unsuccessful\n");
            test_closed(f);
            return -1;
        }
    }
    else
    {
        fprintf(stderr, "Error: no 'count=value' in the first line\n");
        test_closed(f);
        return -1;
    }

    for (i = 0;i < objCount;i++)
    {
        if (fscanf(f, "%d %d %d", &id, &x, &y ) == 3)
        {
            struct obj_t newObject;
            
            newObject.id = id;
            newObject.x = x;
            newObject.y = y;

            init_cluster(&(*arr)[i], 1);
            append_cluster(&(*arr)[i], newObject);
        } 
        else 
        {
            fprintf(stderr, "Error: wrong file format\n");
            for(j = i - 1;j >= 0;j--)
            {
                clear_cluster(&(*arr)[j]);
            }
            free(*arr);
            *arr = NULL;
            test_closed(f);
            return -1;
        }
    }

    if (test_closed(f) != 0)
    {
        fprintf(stderr, "Error: file failed to close\n");
        for (i = 0;i < objCount;i++)
        {
            clear_cluster(&(*arr)[i]);
        }
        free(*arr);
        *arr = NULL;
        return -1;
    }

    return objCount;
}

/*
 Tisk pole shluku. Parametr 'carr' je ukazatel na prvni polozku (shluk).
 Tiskne se prvnich 'narr' shluku.
*/
void print_clusters(struct cluster_t *carr, int narr)
{
    printf("Clusters:\n");
    for (int i = 0; i < narr; i++)
    {
        printf("cluster %d: ", i);
        print_cluster(&carr[i]);
    }
}

int main(int argc, char *argv[])
{
    struct cluster_t *clusters;

    // TODO
    int numOfClusters, clusterCount, idx1, idx2, i;
    long val;
    char *end_ptr;
 
    if (argc == 2)
    {
        numOfClusters = 1;
    }
    else if (argc == 3 || argc == 4)
    {  
        val = strtol(argv[2], &end_ptr, 10);
        if (*end_ptr != '\0')
        {
            fprintf(stderr, "Error: strtol conversion was not successful\n");
            return -1;
        }
        if (val <= 0)
        {
            fprintf(stderr, "Error: wrong value entered\n");
            return -1;
        }

        numOfClusters = val;

        if (argc == 4)
        {
            if (strcmp(argv[3], "--avg") == 0)
            {
                premium_case = 1;
            }
            else if (strcmp(argv[3], "--max") == 0)
            {
                premium_case = 2;
            }
            else if (strcmp(argv[3], "--min") == 0)
            {
                premium_case = 3;
            }
            else
            {
                fprintf(stderr, "Error: wrong method argument entered\n");
                return -1;
            }
        }
    }
    else
    {
        fprintf(stderr, "Error: wrong argument format\n");
        return -1;
    }

    if ((clusterCount = load_clusters(argv[1], &clusters)) < 0)
    {
        fprintf(stderr, "Error: clusters didn't load properly\n");
        return -1;
    }
    
    if (clusterCount < numOfClusters)
    {
        fprintf(stderr, "Error: more clusters than loaded objects\n");

        for (i = 0;i < clusterCount;i++)
        {
            clear_cluster(&clusters[i]);
        }

        free(clusters);
        return -1;
    }

    while (clusterCount > numOfClusters)
    {
        find_neighbours(clusters, clusterCount, &idx1, &idx2);
        merge_clusters(&clusters[idx1], &clusters[idx2]);
        clusterCount = remove_cluster(clusters, clusterCount, idx2);
    }

    print_clusters(clusters, clusterCount);
    for (i = 0;i < numOfClusters;i++)
    {
        clear_cluster(&clusters[i]);
    }
    free(clusters);
    return 0;
}
