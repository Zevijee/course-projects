// importing necessary libraries
#include <stdio.h>
#include <cs50.h>


// ?
int main(void)

//code
{
    // getting user input
    int height = get_int("enter the height it must be less than or equal to 8: ");

    // creating a forever loop to kee- checking if the user entered the apropriate input
    while(true)

    // checking if the input is to high or too low
    {if(height > 8 || height < 1)
    {
        // promting to the user to re-enter if the input is to high
        printf("too high or too low\n");
        height = get_int("please choose a positive number less than or equal to 8: ");
    }

    // if input isn't to high than run this code
    else
        {// creating the mainloop var
        int main_loop;

        // looping through the main loop
        for(main_loop=1; main_loop <= height; main_loop++)
        {
            // creating the drawing var
            int draw_loop;

            // looping through to insert the
            for(draw_loop = height; main_loop < draw_loop; draw_loop--)
            {
                printf(" ");
            }

            // creating the "#" loop var
            int i;

            // looping to draw the left
            for(i=0; i < draw_loop; i++)
            {
                printf("#");
            }

            // inserting the space in between the two sides
            printf("  ");

            // looping to draw the right side
            for(i=0; i < draw_loop; i++)
            {
                printf("#");
            }

            // moving the cursor to the next line
            printf("\n");
        }
        break;

    }}}
