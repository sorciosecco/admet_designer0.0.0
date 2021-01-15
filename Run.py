
import argparse

from core import settings
from core.preprocessing import run_prefiltering_operations
from core.build import build_classification_model
from core.subset_selection import select_subset
from core.buildrc import build_class_regression_model
from core.balance import balance_sets
from core.build_regr_model import build_regression_model

description_message="Software for the development of prediction models focused on ADMET properties."
usage_message='''%(prog)s [<optional arguments>] COMMAND [<specific_options>]'''
epilog_message='''COMMANDS are:
    CREATE  For processing a set of molecules to create a matrix
    BUILDC  For running classification models
    SUBSET  For creating a training and a test set
    BUILDRC For running a regression study on a categorical response
    BUILDR  For running a regression study on a continue response'''

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=description_message, formatter_class=argparse.RawDescriptionHelpFormatter, usage=usage_message, epilog=epilog_message)
    
    parser.add_argument("-f", "--fit", type=str, help="TRAINING SET file with descriptors and response (; separated)")
    parser.add_argument("-p", "--predict", type=str, help="TEST SET file with descriptors and response (; separated)")
    parser.add_argument("-r", "--response", type=str, help="response variable name")
    parser.add_argument("-m", "--model", type=str, default="RF", help="available models: AB, ETC, GB, kNN, rNN, LDA, MLP, PLS, RF, SVM")
    parser.add_argument("-v", "--verbose", type=int, default=0, help="increase verbosity")
    parser.add_argument("-s", "--seed", type=int, default=666, help="set random seed")
    parser.add_argument("-sv", "--savevars", action="store_true", help="save variables importance on csv file")
    subparsers=parser.add_subparsers()
    
    parser_CREATE=subparsers.add_parser("CREATE")
    parser_CREATE.add_argument("-i", "--infile", type=str, help="Input file with molecules in sdf or text format (; separated .csv, .smi or .txt with header). In such case, the column ordering should follow a standard SMILES;ID;ACTIVITY ordering.")
    parser_CREATE.add_argument("-lmw", "--lowmw", type=int, help="min molecular weight allowed (default is 0)", default=0)
    parser_CREATE.add_argument("-hmw", "--highmw", type=int, help="max molecular weight allowed (default is 2k)", default=2000)
    parser_CREATE.add_argument("-lna", "--lowna", type=int, help="min non-H atoms allowed (default is 2)", default=2)
    parser_CREATE.add_argument("-hna", "--highna", type=int, help="max non-H atoms allowed (default is 120)", default=120)
    parser_CREATE.add_argument("-lr", "--lowresp", type=int, help="<for converting a continuous activity to a categorical one> low threshold")
    parser_CREATE.add_argument("-hr", "--highresp", type=int, help="<for converting a continuous activity to a categorical one> high threshold")
    parser_CREATE.set_defaults(func=run_prefiltering_operations)
    
    parser_BUILDC=subparsers.add_parser("BUILDC")
    parser_BUILDC.add_argument("-pc", "--probacutoff", type=float, default=None, help="generate predictions only for objects having a prediction probability above this cutoff")
    parser_BUILDC.add_argument("-np", "--npara", action="store_true", help="use non-default parameters for model training")
    parser_BUILDC.add_argument("-mc", "--multiclass", action="store_true", help="to model more than two classes")
    parser_BUILDC.add_argument("-gs", "--gridsearch", action="store_true", help="use grid search to detect optimal parameters")
    parser_BUILDC.add_argument("-bfe", "--backfeel", action="store_true", help="use Backward Feature Elimination to select the best descriptors")
    parser_BUILDC.add_argument("-sm", "--savemodel", action="store_true", help="save model")
    parser_BUILDC.add_argument("-sp", "--savepred", action="store_true", help="save predictions on csv file")
    parser_BUILDC.set_defaults(func=build_classification_model)
    
    parser_SUBSET = subparsers.add_parser("SUBSET")
    parser_SUBSET.add_argument("-p", "--percentage", type=int, help="sub-set amount (percentage)")
    parser_SUBSET.add_argument("-n", "--number", type=int, help="subset amount (integer number)")
    parser_SUBSET.add_argument("-b", "--balance", action="store_true", help="it produces a balanced selection amongst classes")
    parser_SUBSET.add_argument("-m", "--method", type=str, help="subselection method (R: random, D: most descriptive, L: most different)")
    parser_SUBSET.add_argument("-s1", "--strategy", action="store_true", help="TRUE: select a subsample for each activity class, FALSE: select a subsample from the entire list")
    parser_SUBSET.add_argument("-s2", "--seed", type=int, default=666, help="set random seed")
    parser_SUBSET.set_defaults(func=select_subset)
    
    parser_BALANC=subparsers.add_parser("BALANC")
    parser_BALANC.add_argument("-p", "--percentage", type=int, help="sub-set amount (percentage)", required=True)
    parser_BALANC.set_defaults(func=balance_sets)
    
    parser_BUILDRC=subparsers.add_parser("BUILDRC")
    parser_BUILDRC.add_argument("-lv", "--latent", type=int, help="[for PLS only] use a fixed number of latent variables (default is 10)")
    parser_BUILDRC.add_argument("-ht", "--highthreshold", type=float, help="high threshold value for scoring Yexp and Ypred")
    parser_BUILDRC.add_argument("-lt", "--lowthreshold", type=float, help="low threshold value for scoring Yexp and Ypred")
    parser_BUILDRC.add_argument("-sp", "--savepred", action="store_true", help="save predictions on csv file")
    parser_BUILDRC.set_defaults(func=build_class_regression_model)
    
    parser_BUILDR=subparsers.add_parser("BUILDR")
    parser_BUILDR.add_argument("-lv", "--latent", type=int, help="[for PLS only] use a fixed number of latent variables (default is 10)", default=10)
    parser_BUILDR.add_argument("-pc", "--probacutoff", type=float, default=0.5, help="[for ML only] generate predictions only for objects having a prediction probability above this cutoff")
    parser_BUILDR.add_argument("-cv", "--crossval", type=int, help="[for ML only] number of splits to perform the internal cross-validation (default is 5)", default=5)
    #parser_BUILDR.add_argument("-np", "--npara", action="store_true", help="[for ML only] use non-default parameters for model training")
    #parser_BUILDR.add_argument("-gs", "--gridsearch", action="store_true", help="[for ML only] use grid search to detect optimal parameters")
    #parser_BUILDR.add_argument("-sm", "--savemodel", action="store_true", help="save model")
    #parser_BUILDR.add_argument("-sp", "--savepred", action="store_true", help="save predictions on csv file")
    parser_BUILDR.set_defaults(func=build_regression_model)
    
    args = parser.parse_args()
    
    # variables included in settings set to information from ARGS
    settings.RESPONSE=args.response
    settings.FIT=args.fit
    settings.PREDICT=args.predict
    settings.VERBOSE=args.verbose
    settings.MODEL=args.model
    settings.SEED=args.seed
    settings.SAVEVARS=args.savevars
    # This launches the specific function, according to the specified command
    args.func(args)
    
