'''
TODO: Добавить чтение содержимого каждого хранилища (сундука).
'''

import anvil
import sys
import os
import json

path_to_region_files = sys.argv[1]
region_file_names = os.listdir(path_to_region_files)

for region_file_name in region_file_names[:2]:
    region_file_path = os.path.join(path_to_region_files, region_file_name)
    
    region = anvil.Region.from_file(region_file_path)
    
    chunks_processed = {}
    if os.path.exists('reports/' + region_file_name):
        chunks_processed = json.load(open('reports/' + region_file_name))
    
    if len(chunks_processed.keys()) == 1024:
        print(f'Region "{region_file_name}" finished!')
        continue
    
    chunks_processed_coords = chunks_processed.keys()

    for chunk_x in range(32):
        for chunk_z in range(32):
            chunk_coords = f'{chunk_x}:{chunk_z}'
        
            print(f'Chunk at {chunk_coords} started!')
            
            chunk = None
            try:
                chunk = anvil.Chunk.from_region(region, chunk_x, chunk_z)
            except anvil.errors.ChunkNotFound:
                pass

            blocks_in_chunk = {}
            
            if chunk is None:
                print(f'Chunk at {chunk_coords} skipped!')
                continue

            if chunk_coords not in chunks_processed_coords:
                for block_x in range(16):
                    for block_y in range(256):
                        for block_z in range(16):
                            block = chunk.get_block(block_x, block_y, block_z)
                            
                            try:
                                blocks_in_chunk[f'{block.id}:{block.data}'] += 1
                            except KeyError:
                                blocks_in_chunk[f'{block.id}:{block.data}'] = 1

                chunks_processed[chunk_coords] = blocks_in_chunk

    
    with open('reports/' + region_file_name, 'w') as f:
        json.dump(chunks_processed, f, indent=3)
            
    print(f'Region "{region_file_name}" finished!')
