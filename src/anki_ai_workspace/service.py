from __future__ import annotations

from .codex_client import MAX_STORED_CONVERSATION_TURNS, ChatTurn


class ConversationStore:
    """In-memory chat history for the current Anki session."""

    def __init__(self) -> None:
        self._turns_by_conversation_id: dict[str, list[ChatTurn]] = {}

    def turns_for(self, conversation_id: str) -> tuple[ChatTurn, ...]:
        return tuple(self._turns_by_conversation_id.get(str(conversation_id), ()))

    def add_exchange(
        self,
        conversation_id: str,
        user_message: str,
        assistant_message: str,
        *,
        show_user_message: bool = True,
        presentation: str = "message",
        display_text: str | None = None,
        state: str | None = None,
    ) -> None:
        self.add_user_message(
            conversation_id,
            user_message,
            visible=show_user_message,
            presentation=presentation,
            display_text=display_text,
            state=state,
        )
        self.add_assistant_message(conversation_id, assistant_message)

    def add_user_message(
        self,
        conversation_id: str,
        message: str,
        *,
        visible: bool = True,
        presentation: str = "message",
        display_text: str | None = None,
        state: str | None = None,
    ) -> None:
        turns = self._turns_by_conversation_id.setdefault(str(conversation_id), [])
        turns.append(
            ChatTurn(
                "user",
                str(message),
                visible=visible,
                presentation=presentation,
                display_text=display_text,
                state=state,
            )
        )
        del turns[:-MAX_STORED_CONVERSATION_TURNS]

    def add_assistant_message(self, conversation_id: str, message: str) -> None:
        turns = self._turns_by_conversation_id.setdefault(str(conversation_id), [])
        turns.append(ChatTurn("assistant", str(message)))
        del turns[:-MAX_STORED_CONVERSATION_TURNS]

    def discard(self, conversation_id: str) -> None:
        """Forget a temporary conversation when it is deleted."""

        self._turns_by_conversation_id.pop(str(conversation_id), None)


# Kept as an import-compatible alias for callers of the former card-only store.
CardConversationStore = ConversationStore


_store = ConversationStore()


def get_store() -> ConversationStore:
    return _store
