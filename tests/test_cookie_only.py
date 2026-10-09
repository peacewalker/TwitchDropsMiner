import asyncio
from unittest.mock import MagicMock

from webui.adapters.login_form import LoginFormAdapter


def test_cookie_only_never_initializes_browser(monkeypatch):
    monkeypatch.delenv("WEBUI_TWITCH_LOGIN", raising=False)
    login = LoginFormAdapter(MagicMock())
    assert login.cookie_only_login
    assert not login.browser_login_enabled
    assert not hasattr(login, "_browser_display")


def test_missing_cookie_waits_until_shutdown_without_starting_login(monkeypatch):
    import sys
    import types
    from webui.manager import WebUIManager

    gui_stub = types.ModuleType("gui")
    gui_stub.GUIManager = WebUIManager
    monkeypatch.setitem(sys.modules, "gui", gui_stub)
    monkeypatch.delitem(sys.modules, "websocket")
    import twitch
    import webui.patches

    async def run():
        miner = MagicMock()

        async def until_closed(awaitable):
            return await awaitable

        miner.gui.coro_unless_closed.side_effect = until_closed
        state = twitch._AuthState(miner)
        task = asyncio.create_task(state._oauth_login())
        await asyncio.sleep(0)
        assert not task.done()
        miner.gui.login.update.assert_called_once()
        miner.gui.print.assert_called_once()
        miner.request.assert_not_called()
        miner.gui.login.ask_browser_login.assert_not_called()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(run())
