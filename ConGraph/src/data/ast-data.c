int outbyte(int c);
int putchar(int c);

//#define putchar(c) outbyte(c)

static void printchar(char **str, int c)
{
  if (str) {
    **str = c;
    ++(*str);
  }
  else {
    putchar(c);
  }
}
