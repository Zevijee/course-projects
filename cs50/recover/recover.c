#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  byte;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("a file is required for this program to work\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("could not open file\n");
        return 1;
    }

    int file_counter = 0;

    byte buffer[512];
    while (fread(buffer, sizeof(byte), 512, input) > 511)
    {
        if (buffer[0] == 0xff && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            char filename[9];
            sprintf(filename, "%03d.jpg", file_counter);
            FILE *img = fopen(filename, "w");
            fwrite(buffer, 512, 1, img);
            file_counter++;
            while (fread(buffer, sizeof(byte), 512, input) > 0)
            {
                if (buffer[0] == 0xff && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
                {
                    fclose(img);
                    sprintf(filename, "%03d.jpg", file_counter);
                    img = fopen(filename, "w");
                    fwrite(buffer, 512, 1, img);
                    file_counter++;
                }
                else
                {
                    fwrite(buffer, 512, 1, img);
                }
            }
            fclose(img);
        }
    }
    fclose(input);
    return 0;
}