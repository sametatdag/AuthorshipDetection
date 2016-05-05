import os 
import sys
import errno
import getopt
import shutil
import random

def usage():
    print "\nUsage: /usr/bin/python2.7 build_test_and_training_sets.py --data-set /path/to/dataset " \
          "--training-set /path/to/training/set --test-set /path/to/test/set \n"

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:i:t:h', ['data-set=', 'training-set=', 'test-set='])
    if len(opts) < 3:
        usage()
        sys.exit(2)
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-d', '--data-set'):
        input_dir = arg
    elif opt in ('-i', '--training-set'):
        train_path = arg
    elif opt in ('-t', '--test-set'):
        test_path = arg
    else:
        usage()
        sys.exit(2)

print "Creating empty directories for train and test data..."
# First, we delete train and test directories. Then re-create these
# directories. If they already exists, we supress the error, since 
# it's no harm.
try:
    shutil.rmtree(train_path)
    shutil.rmtree(test_path)
except Exception as e:
    pass
try:
    os.makedirs(train_path)
    os.makedirs(test_path)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise


if os.path.isdir(input_dir):
    sub_dirs = [name for name in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, name))]
    for author in sub_dirs:

        new_train_dir = os.path.join(train_path, author)
        new_test_dir = os.path.join(test_path, author)

        os.makedirs(new_train_dir)
        os.makedirs(new_test_dir)

        author_path = os.path.join(input_dir, author)
        author_files = os.listdir(author_path)

        num_of_files = len(author_files)
        percent_60 = num_of_files * 60 / 100
        rest = num_of_files - percent_60

        random.shuffle(author_files)
        to_train = author_files[0:percent_60]
        to_test = author_files[percent_60:]

        for f in to_train:
            src = os.path.join(author_path, f)
            dst = os.path.join(new_train_dir, f)
            shutil.copyfile(src, dst)

        for f in to_test:
            src = os.path.join(author_path, f)
            dst = os.path.join(new_test_dir, f)
            shutil.copyfile(src, dst)

        log = "[%s] total: %d articles, copying %d to train, %d to test." % (author, num_of_files, percent_60, rest)
        print log
    print "\n\nFinished creating train and test directories.\n\n"
else:
    print "Given directory does not exists. (or it is not a directory, but a file.)"
