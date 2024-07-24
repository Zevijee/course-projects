#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // checking for argv1
    if (argc != 2)
    {
        printf("Error: this program requires exactly 2 command line arguments.\n");
        return 1;
    }

    // checking if argv1 is a digit
    else
    {
        for (int x = 0; x < (int)strlen(argv[1]); x++)
        {
            if (isdigit(argv[1][x]) == 0)
            {
                printf("the second must be an int\n");
                return 1;
            }
        }
    }

    // variables
    char key = atoi(argv[1]);
    string plain_text = get_string("plaintext: ");
    printf("ciphertext: ");

    // adding the key the letter
    for (int i = 0; i < (int)strlen(plain_text); i++)
    {
        // checking if lower case
        char current_letter = plain_text[i];
        if (islower(current_letter))
        {
            current_letter = current_letter - 97;
            current_letter = ((current_letter + key) % 26) + 97;
            printf("%c", current_letter);
        }
        
        // cheking if upper case
        else if (isupper(current_letter))
        {
            current_letter = current_letter - 65;
            current_letter = ((current_letter + key) % 26) + 65;
            printf("%c", current_letter);
        }
        else
        {
            printf("%c", current_letter);
        }
    }
    printf("\n");
}
