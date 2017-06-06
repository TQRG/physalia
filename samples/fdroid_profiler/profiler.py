"""Example of the usage of AndroidViewClientUseCase for
with F-Droid.
"""

from time import sleep
from samples.utils import AndroidViewClientUseCase

# pylint: disable=invalid-name
# this is just a script -- uppercase variables would look odd

def run_open_app(use_case):
    """Simply open F-droid."""
    use_case.open_app()
    sleep(2)
    use_case.refresh()
    use_case.view_client.findViewWithText(u'''What's New''')


def cleanup(use_case):
    """Close the app and wait a second."""
    use_case.kill_app()
    sleep(1)


open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./fdroid.apk",
    "org.fdroid.fdroid",
    "0.01",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

open_app_use_case.prepare_apk()
open_app_use_case.profile_and_persist()


# View a listed app
def prepare(use_case):
    """Open app and wait until it loads."""
    use_case.open_app()
    use_case.refresh()
    use_case.wait_for_id("org.fdroid.fdroid:id/icon")


def run_view_listed_app(use_case):
    """Interaction of getting info about an application."""
    app_icon = use_case.view_client.findViewById("org.fdroid.fdroid:id/icon")
    app_icon.touch()
    use_case.wait_for_id("org.fdroid.fdroid:id/ll_description")


view_listed_app_use_case = AndroidViewClientUseCase(
    "ViewListedApp",
    "./fdroid.apk",
    "org.fdroid.fdroid",
    "0.01",
    run_view_listed_app,
    prepare=prepare,
    cleanup=cleanup
)

view_listed_app_use_case.profile_and_persist()

def run_search_for_app(use_case):
    """Interaction of searching for an application."""
    search = use_case.view_client.findViewById("org.fdroid.fdroid:id/action_search")
    search.touch()
    sleep(1)
    use_case.device.type("Frood")
    use_case.wait_for_text("Froody")

search_app_use_case = AndroidViewClientUseCase(
    "SearchApp",
    "./fdroid.apk",
    "org.fdroid.fdroid",
    "0.01",
    run_search_for_app,
    prepare=prepare,
    cleanup=cleanup
)

search_app_use_case.profile_and_persist()
