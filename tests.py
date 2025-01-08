from collections import defaultdict
import os
import os.path as osp
import pytest
from shutil import rmtree

from manage import Status, check_symlinks, setup, move_to_tomfig, create_symlink, handle_not_link, handle_incorrect


CORRECT_TEXT = "Lines of code await, \n" \
    "errors lurking in the dark, \n" \
    "truth in each small break. \n"

INCORRECT_TEXT = "Five, seven, then five, \n" \
    "words dance in a measured form, \n" \
    "brief worlds come alive. \n"


@pytest.fixture
def testing_root():
    tomfig_root = osp.dirname(osp.realpath(__file__))
    testing_root = osp.join(tomfig_root, 'testing')
    os.makedirs(testing_root, exist_ok=True)
    yield testing_root
    rmtree(testing_root, ignore_errors=True)


@pytest.fixture
def tmp_tomfig_dir(testing_root):
    configs_path = osp.join(testing_root, 'configs')
    os.makedirs(configs_path, exist_ok=True)
    yield configs_path
    rmtree(configs_path, ignore_errors=True)


@pytest.fixture
def tmp_config_dir(testing_root):
    configs_path = osp.join(testing_root, 'local_configs')
    os.makedirs(configs_path, exist_ok=True)
    yield configs_path
    rmtree(configs_path, ignore_errors=True)


@pytest.fixture
def tmp_config(tmp_config_dir):
    config_path = osp.join(tmp_config_dir, 'test')
    yield {'test': config_path}


@pytest.fixture
def tmp_config_file_in_tomfig(tmp_tomfig_dir, tmp_config):
    config_path = osp.join(tmp_tomfig_dir, 'test')
    with open(config_path, 'w') as file:
        file.write(CORRECT_TEXT)
    yield tmp_config
    rmtree(config_path, ignore_errors=True)


@pytest.fixture
def tmp_local_correct_config_file(tmp_config):
    config_path = tmp_config['test']
    with open(config_path, 'w') as file:
        file.write(CORRECT_TEXT)
    yield tmp_config
    rmtree(config_path, ignore_errors=True)


@pytest.fixture
def tmp_local_incorrect_config_file(tmp_config):
    config_path = tmp_config['test']
    with open(config_path, 'w') as file:
        file.write(INCORRECT_TEXT)
    yield tmp_config
    rmtree(config_path, ignore_errors=True)


def test_no_local(testing_root, tmp_config_file_in_tomfig):
    tmp_config = tmp_config_file_in_tomfig
    is_all_correct, report = check_symlinks(testing_root, tmp_config, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.LOCAL_MISSING)

    assert(setup(testing_root, tmp_config, False, False, False))
    assert(check_symlinks(testing_root, tmp_config, False)[0])


def test_not_link(testing_root, tmp_config_file_in_tomfig, tmp_local_incorrect_config_file):
    tmp_config = tmp_local_incorrect_config_file
    is_all_correct, report = check_symlinks(testing_root, tmp_config, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.NOT_LINK)

    assert(setup(testing_root, tmp_config, False, False, False))
    assert(check_symlinks(testing_root, tmp_config, False)[0])


def test_not_link_with_backup(testing_root, tmp_config_file_in_tomfig, tmp_local_incorrect_config_file):
    tmp_config = tmp_local_incorrect_config_file
    is_all_correct, report = check_symlinks(testing_root, tmp_config, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.NOT_LINK)

    assert(setup(testing_root, tmp_config, True, False, False))
    assert(check_symlinks(testing_root, tmp_config, False)[0])

    backup_path = tmp_config['test']+'.bckp'
    with open(backup_path, 'r') as file:
        backup_content = file.read()
    assert(INCORRECT_TEXT == backup_content)


def test_incorrect(testing_root, tmp_config_file_in_tomfig):
    tmp_config = tmp_config_file_in_tomfig
    os.symlink(testing_root, tmp_config['test'])

    is_all_correct, report = check_symlinks(testing_root, tmp_config, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.INCORRECT)

    assert(setup(testing_root, tmp_config, False, True, False))
    assert(check_symlinks(testing_root, tmp_config, False)[0])


def test_correct(testing_root, tmp_config_file_in_tomfig):
    tmp_config = tmp_config_file_in_tomfig
    create_symlink(testing_root, 'test', tmp_config['test'])

    is_all_correct, report = check_symlinks(testing_root, tmp_config, False)
    assert(is_all_correct)
    assert(report['test'] == Status.CORRECT)

    os.remove(tmp_config['test'])


def test_move_to_tomfig(testing_root, tmp_tomfig_dir, tmp_local_correct_config_file):
    tmp_config = tmp_local_correct_config_file

    move_to_tomfig(testing_root, 'test', tmp_config['test'], True)

    is_all_correct, report = check_symlinks(testing_root, tmp_config, False)
    assert(is_all_correct)
    assert(report['test'] == Status.CORRECT)

    os.remove(osp.join(tmp_tomfig_dir, 'test'))
    os.remove(tmp_config['test']+'.bckp')

