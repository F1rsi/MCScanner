'''
TODO: Добавить чтение содержимого каждого хранилища (сундука).
'''

import anvil
import sys
import os
import json
import time


def analyze_region_file(region_file_name: str, region_file_path: str, output_folder: str) -> None:
    result = {}
    
    region_file_result_path = os.path.join(output_folder, region_file_name)

    if os.path.exists(region_file_result_path):
        result = json.load(open(region_file_result_path))
    
    if len(result.keys()) == 1024:
        print(f'Region "{region_file_name}" finished!')
        return

    region = anvil.Region.from_file(region_file_path)
    
    chunks_processed_coords = result.keys()

    for chunk_x in range(32):
        for chunk_z in range(32):
            chunk_coords = f'{chunk_x}:{chunk_z}'
            
            chunk = None
            try:
                chunk = anvil.Chunk.from_region(region, chunk_x, chunk_z)
            except anvil.errors.ChunkNotFound:
                pass

            if chunk is None or chunk_coords in chunks_processed_coords:
                # print(f'Chunk at {chunk_coords} skipped!')
                continue
            
            # print(f'Chunk at {chunk_coords} started!')

            blocks_in_chunk = {}

            for block_x in range(16):
                for block_y in range(256):
                    for block_z in range(16):
                        block = chunk.get_block(block_x, block_y, block_z)

                        try:
                            blocks_in_chunk[f'{block.id}:{block.data}'] += 1
                        except KeyError:
                            blocks_in_chunk[f'{block.id}:{block.data}'] = 1

            result[chunk_coords] = blocks_in_chunk

    
    with open(region_file_result_path, 'w') as f:
        json.dump(result, f)
    
    # print(f'Region "{region_file_name}" finished!')


path_to_region_files = sys.argv[1]
region_file_names = os.listdir(path_to_region_files)

output_folder = 'reports'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for region_file_name in region_file_names:
    region_file_path = os.path.join(path_to_region_files, region_file_name)
    
    time_begin = time.time()
    analyze_region_file(region_file_name, region_file_path, 'reports')
    time_end = time.time()

    print(f'Time elapsed: {time_end - time_begin}s')
