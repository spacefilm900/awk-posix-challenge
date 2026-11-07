BEGIN { n=0; if (1 || ++n) n+=10; if (0 && ++n) n+=100; print n }
