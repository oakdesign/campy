import argparse
import os
import sys
from extractors.cam_extractor import CamFile
from readers.plt_reader import PltFile
from readers.uni_reader import UniFile

def process_plt_files(output_dir):
    """Process .plt files in the output directory"""
    plt_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.plt'):
                plt_files.append(os.path.join(root, file))
    
    if not plt_files:
        print("No .plt files found")
        return
    
    for plt_file_path in plt_files:
        print(f"\nProcessing {plt_file_path}:")
        plt = PltFile(plt_file_path)
        
        # Print data in sections to avoid truncation
        print(f"Number of pilots: {plt.num_pilots}")
        print(f"Pilot information:")
        for i, pilot in enumerate(plt.pilot_info):
            if i < 20 or i > plt.num_pilots - 5:  # Print first 20 and last 5
                print(f"  Pilot {i+1}: Usage={pilot.usage}, Voice ID={pilot.voice_id}, Photo ID={pilot.photo_id}")
            elif i == 20:
                print(f"  ... {plt.num_pilots - 25} more pilots ...")
        
        print(f"Number of callsigns: {plt.num_callsigns}")
        
        # Save complete data to a text file
        output_file = plt_file_path + '.txt'
        with open(output_file, 'w') as f:
            f.write(str(plt))
        print(f"Complete data saved to {output_file}")

def process_uni_files(output_dir):
    """Process .uni files in the output directory"""
    uni_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.uni'):
                uni_files.append(os.path.join(root, file))
    
    if not uni_files:
        print("No .uni files found")
        return
    
    print(f"Found {len(uni_files)} UNI files to process")
    
    for uni_file_path in uni_files:
        print(f"\nProcessing {uni_file_path}:")
        try:
            uni = UniFile(uni_file_path)
            uni.save_decompressed(output_dir)
        except Exception as e:
            print(f"Error processing {uni_file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Unpack .cam files from Falcon BMS")
    parser.add_argument("camfile", help="Path to .cam file")
    parser.add_argument("outdir", help="Output directory for extracted files")
    parser.add_argument("--process", action="store_true", help="Process extracted files")
    args = parser.parse_args()

    cam = CamFile(args.camfile)
    cam.load()
    cam.extract_all(args.outdir)
    
    if args.process:
        # Process files based on their types
        process_plt_files(args.outdir)
        process_uni_files(args.outdir)


if __name__ == "__main__":
    main()