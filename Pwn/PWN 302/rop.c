#include <stdio.h>
#include <stdlib.h>

const static char *bin_sh = "/bin/sh";

int main() {
    char buf[20];
    system("ls");
    fgets(buf, 100, stdin);
    return 0;
}
