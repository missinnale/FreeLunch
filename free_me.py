import os
import argparse
import re

args = None
given_steps = []
when_steps = []
then_steps = []
current_givens = []
current_whens = []
current_thens = []

def is_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file {} does not exist. Please provide a valid file.".format(arg))
    else:
        return arg

def apply_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('feature_file', type = lambda arg: is_file(parser, arg))
    parser.add_argument('step_file', type = lambda arg: is_file(parser, arg))
    parser.add_argument('page_file', type = lambda arg: is_file(parser, arg))
    parser.add_argument('locator_file', type = lambda arg: is_file(parser, arg))
    args = parser.parse_args()

def get_feature(feature_dir):
    global args
    f = open(feature_dir + args.feature_file, 'r')
    val = f.read()
    f.close()
    return val

def get_config_vals():
    import config
    return { 'feature': config.__dict__['FEATURE_DIR'],
             'step':config.__dict__['STEP_DIR'],
             'page':config.__dict__['PAGE_DIR'],
             'locator':config.__dict__['LOCATOR_DIR']}

def locate_steps(features):
    features = features.split('\n')
    global given_steps
    global when_steps
    global then_steps
    for line in features:
        if 'Given' in line:
            given = True
            then = False
            step = re.sub(r'Given ', '', line)
            if step not in given_steps:
                given_steps.append(step)
        elif 'When' in line:
            when = True
            given = False
            step = re.sub(r'When ', '', line)
            if step not in when_steps:
                when_steps.append(step)
        elif 'Then' in line:
            then = True
            when = False
            step = re.sub(r'Then ', '', line)
            if step not in then_steps:
                then_steps.append(step)
        elif 'And' in line:
            step = re.sub(r'And ', '', line)
            if then and step not in then_steps: then_steps.append(line)
            elif when and step not in when_steps: when_steps.append(line)
            elif given and step not in given_steps: given_steps.append(line)

def check_step_existence(step_dir):
    f = open(step_dir + args.step_file, 'r')
    global current_givens
    global current_whens
    global current_thens
    for line in f:
        step = re.search("@given\('(.+)'\)", line) or re.search("@when\('(.+)'\)", line) or re.search("@then\('(.+)'\)", line)
        if step is None:
            continue
        elif 'given' in step.group():
            if step.group(1) not in current_givens:
                current_givens.append(step.group(1))
        elif 'when' in step.group():
            if step.group(1) not in current_whens:
                current_whens.append(step.group(1))
        elif 'then' in step.group():
            if step.group(1) not in current_thens:
                current_thens.append(step.group(1))
    f.close()



def write_givens():
    pass

def write_whens():
    pass

def write_thens():
    pass


if __name__ = "__main__":
    apply_args()
    dirs = get_config_vals()
    feature_file = get_feature()