#!bin/bash
mojo llama2.mojo ../llama2.c/tl-chat.bin \
    -tk ../llama2.c/tok_tl-chat.bin \
    -n 50 -t 0 -s 100 -i "<|im_start|>user\n"
echo "============================================================"
mojo llama2.mojo ../llama2.c/tl.bin \
    -n 50 -t 0 -s 100 -i "What's the meaning of life?"
echo "============================================================"
mojo llama2.mojo stories15M.bin \
    -n 100 -t 0 -s 100 -i "Once upon the time,"
echo "============================================================"
mojo llama2.mojo stories110M.bin \
    -n 100 -t 0 -s 100 -i "Once upon the time,"