#include <stdio.h>

int main() {
    int tests;
    scanf("%d", &tests);
    while (tests--) {
        int n;
        scanf("%d", &n);
        printf("%d\n", n+1);
    }
    return 0;
}
