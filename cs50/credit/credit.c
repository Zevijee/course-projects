//credit card company atributes
/*
american_express:
    size = 15digits
    starts_with = 34 || 37

master_card:
    size = 16digits
    starts_with = range(51, 56)

visa:
    size = 13digits || 16digits
    starts_with = 4
*/
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    while (true)
    {
        long cc_number = get_long("card number: ");
        //printf("%li\n", cc_number);
        int number_counter;
        int x;
        long i;
        int j = 0;
        int num_a = 0;
        int num_b = 0;

        //printf("\nfirst numbers\n");

        for (i = 100; i < (cc_number * 10); i = i * 100)
        {
            long current_num = (cc_number % i) / (i / 10) * 2;
            if (current_num > 9)
            {
                num_a = num_a + (current_num % 10) + (current_num / 10);
            }
            else
            {
                num_a = num_a + current_num;
            }
            //printf("current_num = %li, i = %li, num_a = %i, j = %i\n", current_num, i, num_a, j);
            j = j + 1;
        }
        int stuff = cc_number / (i / 10000);
        //printf("\n2nd numbers\n");

        for (i = 10; i < (cc_number * 10); i = i * 100)
        {
            long current_num = (cc_number % i) / (i / 10);
            num_b = num_b + current_num;
            //printf("current_num = %li, i = %li, num_b = %i, j = %i\n", current_num, i, num_b, j);
            j = j+ 1;
        }
        int checksum = num_a + num_b;
        // printf("%i\n", checksum);
        //printf("%i\n", stuff/100);
        if (checksum % 10 == 0)
        {
            if (j == 16)
            {
                if (stuff / 10 == 4)
                {
                    printf("VALID\nVISA\n");
                    break;
                }
                else if (stuff > 50 && (stuff < 56))
                {
                    printf("VALID\nMASTERCARD\n");
                    break;
                }

            }

            else if (j == 15 && ((stuff / 10) == 34 || stuff / 10 == 37))
            {
                printf("VALID\nAMEX\n");
                break;
            }

            else if (j == 13 && ((stuff / 100) == 4))
            {
                printf("VALID\nVISA\n");
                break;
            }
        }
        printf("INVALID\n");
        break;
    }
}