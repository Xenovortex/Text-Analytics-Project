import argparse

from utils import benchmark, downloader, traverser, evaluater, to_dataframe
from utils.sample import hello_world  # import of module from subfolder


"""
This script should serve as entrypoint to your program.
Every module or package it relies on has to be imported at the beginning.
The code that is actually executed is the one below 'if __name__ ...' (if run
as script).
"""


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", dest='download', action='store',
                        help="Download specific or all datasets. Options: 'all', 'TextComplexityDE19', 'Weebit', 'dw'")
    parser.add_argument("--experiment", dest='experiment', action='store',
                        help="Select experiment to perform. Options: 'vectorizer'")
    parser.add_argument("--search", dest='search', action='store', nargs=5,
                        help="Perform linear search for [hyperparameter, start, end, step, model]. Options: hyperparameter ['feature', 'window', 'count', 'epochs', 'lr', 'min_lr'], model ['word2vec']")
    parser.add_argument("--augmentation", dest="augmentation", action='store_true',
                        help="Augmentate the downloaded datasets and save the result in a h5 file")

    parser.set_defaults(download=None, experiment=None, search=None, augmentation=False)
    args = parser.parse_args()


    # load datasets
    if args.download is not None:
        if args.download == 'all':
            downloader.download_TextComplexityDE19()
            downloader.download_Weebit()
            downloader.download_dw_set()
        elif args.download == 'TextComplexityDE19':
            downloader.download_TextComplexityDE19()
        elif args.download == 'Weebit':
            downloader.download_Weebit()
        elif args.download == 'dw':
            downloader.download_dw_set()
        else:
            print("Input {} for --download is invalid. Choose one of the following: 'all', 'TextComplexityDE19', 'Weebit', 'dw'".format(args.download))
            exit()

    # augmentation
    if args.augmentation:
        to_dataframe.store_augmented_h5("all_data.h5", test_size=0.2)

    # hyperparameter search
    if args.search is not None:
            traverser.traverser(*args.search)


    # experiments
    if args.experiment is not None:
        # vectorizer
        if args.experiment == 'vectorizer':
            benchmark.benchmark_vectorizer()
        if args.experiment == 'test':
            MSE, RMSE, MAE, r_square = evaluater.evaluate_baseline()
            print(r_square)


