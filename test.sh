#!bin/bash
mojo llama2.mojo tl-chat.bin \
    -z tok_tl-chat.bin \
    -n 256 -t 0 -s 100 -i "<|im_start|>user\nCan you explain huggingface?<|im_end|>\n<|im_start|>assistant\n"
echo "============================================================"
# mojo llama2.mojo ../llama2.c/tl.bin \
#     -z ../llama2.c/tok_tl.bin \
#     -n 50 -t 0 -s 100 -i "What is the meaning of life?"
# echo "============================================================"
mojo llama2.mojo stories15M.bin \
    -n 100 -t 0 -s 100 -i "Once upon the time"
echo "============================================================"
mojo llama2.mojo stories110M.bin \
    -n 100 -t 0 -s 100 -i "Once upon the time"
