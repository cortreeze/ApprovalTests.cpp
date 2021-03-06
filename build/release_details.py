import os

import version
from prepare_release import PrepareRelease
from deploy_release import DeployRelease

# TODO list
# Add CI step to check this prepare process works on every push
# Rewrite the SingleHpp Java program in Python
# Automate the check_steps
# Improve the chdir to start at the top-level directory - and check that we are the top-level
# Simplify pushdir/popdir - ideally make it RAII - with with!
# Review folder structure for Python scripts
# Add a reminder to close any release milestone

class ReleaseDetails:
    def __init__(self, old_version, new_version, publish_release):
        self.old_version = version.get_version(old_version)
        self.new_version = version.get_version(new_version)
        self.new_version_object = new_version
        self.push_to_production = publish_release

        self.old_single_header = F"ApprovalTests.{self.old_version}.hpp"
        self.new_single_header = F"ApprovalTests.{self.new_version}.hpp"

        self.approval_tests_dir = F"../ApprovalTests"
        self.build_dir = F"../build"
        self.release_dir = F"../build/releases"
        self.release_new_single_header = F"{self.release_dir}/{self.new_single_header}"

        self.conan_repo_dir = '../../../conan/conan-center-index-claremacrae'
        self.conan_approvaltests_dir = os.path.join(self.conan_repo_dir, 'recipes', 'approvaltests.cpp')

        self.main_project_dir = F"../../ApprovalTests.Cpp"
        self.starter_project_dir = F"../../ApprovalTests.Cpp.StarterProject"

        self.new_release_notes_path = os.path.join(self.build_dir, F'relnotes_{version.get_version_without_v(self.new_version)}.md')
        self.xxx_release_notes_path = os.path.join(self.build_dir, F'relnotes_x.y.z.md')
        self.template_release_notes_path = os.path.join(self.build_dir, F'relnotes_template.md')


def build(update_version, deploy):
    old_version = version.load_version()
    new_version = update_version(old_version)

    release_details = ReleaseDetails(old_version, new_version, deploy)
    prepare_release = PrepareRelease(release_details)
    prepare_release.prepare_everything()
    if not release_details.push_to_production:
        print("Everything worked - didn't commit or push")
    else:
        deploy_release = DeployRelease(release_details)
        deploy_release.push_everything_live()
