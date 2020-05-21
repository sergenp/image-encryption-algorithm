# import zigzag,CKG,divide_blocks functions from util.py
from util import CKG, divide_blocks, get_from_PerTab, AES_SBOX, DES_IP

import itertools
flatten = itertools.chain.from_iterable

def encrypt_image(im):
    # STEP 3. Divide image to blocks of 256 pixels
    blocks = list(divide_blocks(im, 256))
    # for keeping track of padding and how many pixels we have generated to fill the last block
    pad = 0
    # STEP 4. Pad the last block
    if len(blocks[-1]) % 256 != 0:
        pad = 256 - len(blocks[-1])
        numbers_required = CKG(num_count=pad, upper_limit=256)
        # pad the block
        blocks[-1] = list(itertools.chain(blocks[-1], numbers_required))

    encrypted_blocks = []

    # STEP 5. Generate IV
    IV = CKG(256, 256)

    print("Total blocks", len(blocks))

    # STEP 6.
    for block_index, block in enumerate(blocks):
        # STEP 7. XOR Operation
        ciphered_image = []
        for i, el in enumerate(IV):
            ciphered_image.append(el^block[i])
        
        for rn in range(8):
            # STEP 9. generate a and b values
            a, b = CKG(1, 16)[0], CKG(1, 16)[0]
            # STEP 10
            cola, colb = get_from_PerTab(a), get_from_PerTab(b)

            aes_sbox = AES_SBOX()

            for index, k in enumerate(cola):
                # swap rows of sbox with value in the col1 array
                # ex: index = 0, k = 5, swap 0th row with 5th row,
                # index=1, k=10, swap 1th row with 10th row...
                aes_sbox.swap_aes_sbox_row(index, k)

            table1 = aes_sbox.AES_S.ravel() # turns 16x16 to 1x256
            for index, k in enumerate(table1):
                # ^= shorthand for ciphered_image[index] ^ table1[index]
                ciphered_image[index] ^= table1[index]

            key1 = CKG(256,256)
            
            for index, k in enumerate(key1):
                ciphered_image[index] ^= key1[index]

            # reset the aes sbox to default value
            aes_sbox.reset_aes_sbox()
            for index, k in enumerate(colb):
                # swap rows of sbox with value in the col1 array
                # ex: index = 0, k = 5, swap 0th row with 5th row,
                # index=1, k=10, swap 1th row with 10th row...
                aes_sbox.swap_aes_sbox_col(index, k)

            table2 = aes_sbox.AES_S.ravel()
            for index, k in enumerate(table2):
                ciphered_image[index] ^= table2[index]

            key2 = CKG(256,256)
            for index, k in enumerate(key2):
                ciphered_image[index] ^= key2[index]

            ciphered_image = list(divide_blocks(ciphered_image, 64))
            # get the sub_block from ciphered_image
            # swap the indexes of sub_block using the DES table
            sub_block = ciphered_image[rn%4]
            for index, k in enumerate(DES_IP):
                sub_block[index], sub_block[k] = sub_block[k], sub_block[index]
            ciphered_image[rn%4] = sub_block
            ciphered_image = list(flatten(ciphered_image))

        print(f"Block #{block_index+1}/{len(blocks)} Encrypted", end="\r")
        IV = list(ciphered_image) # copies the ciphered_image to IV
        encrypted_blocks.append(ciphered_image) 

    # undo padding if there is one
    if pad != 0:
        encrypted_blocks[-1] = encrypted_blocks[-1][:-pad]
    print("\nEncrypted succesfully")
    return encrypted_blocks

