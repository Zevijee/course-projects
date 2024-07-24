// Implements a dictionary's functionality
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"


// Declare the global variable
extern int globalVar;
int globalVar = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 75;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash the word
    int index = hash(word);

    // create the cursor variable to traverse the linked list
    node *cursor = table[index];

    // access the linked list at the index number
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int a = toupper(word[0]) - 'A';
    if (toupper(word[1]) - 'A' > 0)
    {
        int b = toupper(word[1]) - 'A';
        if (toupper(word[2]) - 'A' > 0)
        {
            int c = toupper(word[2]) - 'A';
            return a + b + c;
        }
        return a + b;
    }
    return a;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open file
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        return false;
    }

    // malloc memory for word
    char *word = malloc(sizeof(char) * LENGTH + 1);
    if (word == NULL)
    {
        return false;
    }

    // loop through file and get each word
    while (fscanf(input, "%s", word) != EOF)
    {
        // create node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // put current word in curretn node
        strcpy(n->word, word);

        // hash each word for indexing in the table[]
        int index = hash(word);

        // point the current node to the first index in the link list according to the hash number then point the hash index of the node to the new node
        n->next = table[index];
        table[index] = n;

        n = NULL;
        free(n);

        globalVar++;
    }
    fclose(input);
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return globalVar;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // loop through the table array
    for (int i = 0; i < N; i++)
    {
        // check if table[i] = NULL
        if (table[i] != NULL)
        {
            node *cursor = table[i];
            while (cursor != NULL)
            {
                node *tmp = cursor->next;
                free(cursor);
                cursor = tmp;
            }
        }
    }

    return true;
}
