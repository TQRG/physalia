"""Utils for Physalia samples"""

import sys
from com.dtmilano.android.viewclient import ViewClient
from physalia.energy_profiler import AndroidUseCase

class AndroidViewClientUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `AndroidViewClient`."""

    # pylint: disable=not-callable
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 run, prepare=None, cleanup=None):  # noqa: D102
        super(AndroidViewClientUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
            run, prepare, cleanup
        )
        self.device = None
        self.serialno = None
        self.view_client = None

    def start_view_client(self, force=False):
        """Setup `AndroidViewClient`.

        Args:
            force (boolean): force start even if it was previously done (default False).
        """
        # pylint: disable=attribute-defined-outside-init

        if self.view_client is None or force is True:
            original_argv = sys.argv
            sys.argv = original_argv[:1]
            kwargs1 = {'ignoreversioncheck': False,
                       'verbose': False,
                       'ignoresecuredevice': False}
            device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
            kwargs2 = {'forceviewserveruse': False,
                       'useuiautomatorhelper': False,
                       'ignoreuiautomatorkilled': True,
                       'autodump': False,
                       'startviewserver': True,
                       'compresseddump': True}
            view_client = ViewClient(device, serialno, **kwargs2)
            sys.argv = original_argv
            self.device = device
            self.serialno = serialno
            self.view_client = view_client
        #always refresh
        self.refresh()

    def prepare(self):
        """Prepare environment for running.

        Setup Android View Client in order to run experiments.
        """
        self.start_view_client()
        self._prepare()

    def refresh(self):
        """Refresh `AndroidViewClient`."""
        while True:
            try:
                self.view_client.dump(window='-1')
            except RuntimeError:
                continue
            break

    def wait_for_id(self, view_id):
        """Refresh `AndroidViewClient` until view id is found."""
        view = self.view_client.findViewById(view_id)
        while view is None:
            self.refresh()
            view = self.view_client.findViewById(view_id)
        return view

    def wait_for_text(self, text):
        """Refresh `AndroidViewClient` until text is found."""
        view = self.view_client.findViewWithText(text)
        while view is None:
            self.refresh()
            view = self.view_client.findViewWithText(text)
        return view

    def wait_for_content_description(self, content_description):
        """Refresh `AndroidViewClient` until content description is found."""
        view = self.view_client.findViewWithContentDescription(
            content_description
        )
        while view is None:
            self.refresh()
            view = self.view_client.findViewWithContentDescription(
                content_description
            )
        return view
