#!/usr/bin/env python
import os
import sys
import argparse
from datetime import datetime
from HAbench import HABench

def parse_args():
    parser = argparse.ArgumentParser(
        description='HABench - Human Preference Aligned Video Generation Benchmark',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        default='./evaluation_results/',
        help="output path to save the evaluation results"
    )
    
    parser.add_argument(
        "--config_path",
        type=str,
        default='./config.json',
        help="path to the config file"
    )
    
    parser.add_argument(
        "--videos_path",
        type=str,
        required=True,
        help="folder that contains the videos to evaluate"
    )
    
    parser.add_argument(
        "--dimension",
        nargs='+',
        choices=[
            'color',
            'object_class',
            'scene',
            'action',
            'overall_consistency',
            'imaging_quality',
            'aesthetic_quality',
            'temporal_consistency',
            'motion_effects'
        ],
        required=True,
        help="evaluation dimensions to use"
    )
    
    parser.add_argument(
        "--full_json_dir",
        type=str,
        default=None,
        help="path to save the full evaluation information json file"
    )

    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)
    
    # Initialize benchmark
    benchmark = HABench()
    
    try:
        # Run evaluation
        results = benchmark.evaluate(
            videos_path=args.videos_path,
            dimensions=args.dimension,
            config_path=args.config_path,
            full_json_dir=args.full_json_dir
        )
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(args.output_path, f"results_{timestamp}.json")
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"\nEvaluation completed successfully!")
        print(f"Results saved to: {output_file}")
        
    except Exception as e:
        print(f"\nError during evaluation: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 