#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

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

    // Populate array of candidates
    candidate_count =  atoi(argv[1]);

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 3];
        candidates[i].votes = 0;
    }

    int voter_count = atoi(argv[2]);

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = argv[i + 3 + candidate_count];

        // Check for invalid vote
        if (!vote(name))
        {
            printf("");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcasecmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int winner = candidates[0].votes;
//Determines what the largest number of votes is
    for (int i = 0; i < candidate_count; i++)
    {
        if (winner < candidates[i + 1].votes)
        {
            winner = candidates[i + 1].votes;
        }
    }
//Checks who's name holds the largest number of votes
    for (int i = 0; i < candidate_count; i++)
    {
        if (winner == candidates[i].votes)
        {
            printf("%s ", candidates[i].name);
        }
    }
    return;
}

