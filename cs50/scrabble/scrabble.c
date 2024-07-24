#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }

    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }

    else
    {
        printf("Tie\n");
    }


}

int compute_score(string word)
{

    int score = 0;

    // itarating through each letter of the submitted words to calculate the score
    for (int i = 0; i < (int)strlen(word); i++)
    {
        //checking if letter is uppercase
        if (word[i] > 64 && (word[i] < 90))
        {
            int upper_count = word[i] - 65;
            score = score + POINTS[upper_count];
        }
        // checking if letter is lowercase
        else if (word[i] > 96 && (word[i] < 123))
        {
            int lower_count = word[i] - 97;
            score = score + POINTS[lower_count];
        }
        // checking if char is a letter
        else
        {
            score = score + 0;
        }
    }

    return score;
}