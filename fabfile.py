import os
import sys
from fabric.api import *
from fabric.colors import yellow, red

env.hosts = [os.getenv('HATCH_API_URL')]

CODE_DIR = '/srv/hatch/api'
VENV = 'source /srv/venv-devhatch/bin/activate'

@task
def deploy(repo_uri=None):
    """
    Deploy latest version of Hatch API from master
    """
    if repo_uri is None:
        repo_uri = 'git@github.com:pietdaniel/hatch-back-end.git'

    puts(yellow('Running tests'))
    with settings(warn_only=True):
        if local('nosetests').failed:
            puts(red('Tests failed!', bold=True))
            puts(red('Will not proceed', bold=True))
            return

    puts(yellow('Deploying hatch'))

    git_hash = "git ls-remote -h {} master | awk '{{print $1;}}' | cut -c -7".format(repo_uri)
    release_dir = '{}-`{}`'.format(CODE_DIR, git_hash)
    with settings(warn_only=True):
        if run('test -d {}'.format(release_dir)).succeeded:
            msg = 'Latest hatch version already deployed!'.format(git_hash)
            puts(red(msg, bold=True))
            run('ls -l /srv/hatch | grep `{}`'.format(git_hash))
            puts(red('Nothing to do', bold=True))
            return

    puts(yellow('Cloning latest master'))
    run('git clone {} {}'.format(repo_uri, release_dir))
    with settings(warn_only=True):
        use_stg_cfg = 'cp /home/deploy/application.cfg /srv/hatch/application.cfg.bak'
        if run('test -d {}'.format(CODE_DIR)).succeeded:
            with cd(CODE_DIR):
                save_cfg = 'cp instace/application.cfg /srv/hatch/application.cfg.bak'
                if run(save_cfg).failed:
                    puts(yellow('Failed to find existing app cfg, using staging defaults'))
                    run(use_stg_cfg)
                else:
                    puts(yellow('Using existing app cfg'))
            puts(yellow('Removing existing deploy symlink'))
            run('rm {}'.format(CODE_DIR))
        else:
            puts(yellow('No existing deployed code, using staging app cfg defaults'))
            run(use_stg_cfg)

    run('ln -s {} {}'.format(release_dir, CODE_DIR))
    with cd(CODE_DIR):
        run('rm instance/application.cfg')
        run('mv /srv/hatch/application.cfg.bak instance/application.cfg')
        with prefix(VENV):
            puts(yellow('Running any db migrations'))
            run('python manage.py db upgrade')
    puts(yellow('Restarting hatch_api service'))
    run('sudo supervisorctl restart hatch_api')
