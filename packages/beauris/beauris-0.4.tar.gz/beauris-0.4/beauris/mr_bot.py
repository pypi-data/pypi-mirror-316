import logging
import os

import gitlab

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class MR_Bot():

    def __init__(self):
        self.ready = False

        needed_env_vars = [
            'CI_PROJECT_ID',
            'CI_SERVER_URL',
            'GITLAB_BOT_TOKEN',
        ]

        if not all(item in os.environ for item in needed_env_vars):
            log.info("Not in a GitLab MR / merge commit or missing env vars, cannot send message to bot")
            return

        gl_url = os.getenv('CI_SERVER_URL')
        gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))
        project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)

        mr_id = os.getenv('CI_MERGE_REQUEST_IID')

        if not mr_id:
            if os.getenv('CI_COMMIT_SHORT_SHA'):
                # Not in a merge request, but maybe this commit comes from a merged one on default branch
                commit = project.commits.get(os.getenv('CI_COMMIT_SHORT_SHA'))
                mrs = commit.merge_requests()
                # Is there any case where there are multiple MR for a single commit?
                if len(mrs) == 1 and 'iid' in mrs[0]:
                    mr_id = mrs[0]['iid']
                else:
                    log.info("{} MR(s) found for commit, or no ID available. Cannot send notifications".format(len(mrs)))
                    return
            else:
                log.info("Missing either CI_MERGE_REQUEST_IID or CI_COMMIT_SHORT_SHA env variable. Cannot send notifications")
                return

        self.mr = project.mergerequests.get(mr_id, lazy=True)
        self.ready = True

    def write_message(self, message):
        if self.ready:
            self.mr.notes.create({'body': message})
