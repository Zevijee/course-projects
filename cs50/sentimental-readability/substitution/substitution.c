#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // creating a sting to compare the alphabet to
    string alphabet = "abcdefghijklmnopqrstuvwxyz";

    // checking if there is more or less than 2 command line args
    if (argc != 2)
    {
        printf("this program takes exactly 2 command line arguments\n");
        return 1;
    }

    // checking if argv[1] == 26
    if ((int)strlen(argv[1]) != 26)
    {
        printf("the key must be 26 chars long\n");
        return 1;
    }

    // creating nessacerry variables
    int size = 0;
    int validation_counter = 0;
    int arr[26];

    // looping though to see if there is any unknown chars or doubles
    for (int i = 0; i < (int)strlen(argv[1]); i++)
    {
        for (int j = 0; j < (int)strlen(alphabet); j++)
        {
            if (argv[1][i] == alphabet[j])
            {
                validation_counter++;
                for (int x = 0; x < size; x++)
                {
                    if (argv[1][i] == arr[x])
                    {
                        printf("cant use double chars in key\n");
                        return 1;
                    }
                }
                arr[i] = argv[1][i];
                size++;
            }
            if (argv[1][i] == toupper(alphabet[j]))
            {
                validation_counter++;
                for (int x = 0; x < size; x++)
                {
                    if (argv[1][i] == toupper(arr[x]))
                    {
                        printf("cant use double chars in key\n");
                        return 1;
                    }
                }
                arr[i] = toupper(argv[1][i]);
                size++;
            }
        }
        if (validation_counter == 0)
        {
            printf("invalid key entry\n");
            return 1;
        }
        validation_counter = 0;
    }


    // creating neccacerry varriables
    string key = argv[1];
    string input = get_string("plaintext: ");
    printf("ciphertext: ");

    // looping through and encrypting
    for (int i = 0; i < (int)strlen(input); i++)
    {
        for (int j = 0; j < (int)strlen(alphabet); j++)
        {
            if (isupper(input[i]))
            {
                if (input[i] == toupper(alphabet[j]))
                printf("%c", toupper(argv[1][j]));
            }
            else if (islower(input[i]))
            {
                if (input[i] == alphabet[j])
                printf("%c", tolower(argv[1][j]));
            }
            else
            {
                printf("%c", input[i]);
                break;
            }

        }
    }
    printf("\n");
}