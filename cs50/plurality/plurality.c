#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
         if (!vote(name))
         {
            printf("invalid name\n");
         }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    bool b = false;
    for (int i = 0; i < candidate_count; i++)
    {
        int result = strcmp(name, candidates[i].name);
        if (result == 0)
        {
            b = true;
            candidates[i].votes++;
        }
    }
    return b;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    string C[candidate_count];
    int V = candidates[0].votes;
    C[0] = candidates[0].name;
    int J = 0;
    for (int i = 0; i < candidate_count - 1; i++)
    {
        if (candidates[i].votes < candidates[i + 1].votes)
        {
            for (int x = 0; x < J; x++)
            {
                C[x] = "\0";
            }
            V = candidates[i + 1].votes;
            C[0] = candidates[i + 1].name;
            J = 0;
        }
        else if (V == candidates[i + 1].votes)
        {
            C[J] = candidates[i].name;
            C[J + 1] = candidates[i + 1].name;
            J++;
        }
    }
    for (int i = 0; i < J + 1; i++)
    {
        printf("%s\n", C[i]);
    }
}