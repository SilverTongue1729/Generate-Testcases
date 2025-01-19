#include <stdio.h>

int max(int a, int b) {
  return (a > b) ? a : b;
}

int main() {
  int tests;
  scanf("%d", &tests);
  while (tests--) {
    int n;
    scanf("%d", &n);
    int a[n];
    for (int i = 0; i < n; i++) 
      scanf("%d", &a[i]);

    int dp[n];
    for (int i = n - 1; i >= 0; i--) {
      dp[i] = a[i];
      int j = i + a[i];
      if (j < n) 
        dp[i] += dp[j];
    }

    int max_val = dp[0];
    for (int i = 1; i < n; i++) 
      if (dp[i] > max_val) 
        max_val = dp[i];
      
    printf("%d\n", max_val);
    
  }
  return 0;
}
