import unittest

from anki_ai_workspace.service import CardConversationStore


class CardConversationStoreTests(unittest.TestCase):
    def test_conversations_are_separate_by_card(self) -> None:
        store = CardConversationStore()
        store.add_exchange(1, "One", "First")
        store.add_exchange(2, "Two", "Second")

        self.assertEqual([turn.text for turn in store.turns_for(1)], ["One", "First"])
        self.assertEqual([turn.text for turn in store.turns_for(2)], ["Two", "Second"])

    def test_automatic_action_message_can_be_hidden_but_remains_in_history(
        self,
    ) -> None:
        store = CardConversationStore()
        store.add_exchange(
            1,
            "Internal preset instruction",
            "Visible answer",
            show_user_message=False,
        )

        turns = store.turns_for(1)
        self.assertFalse(turns[0].visible)
        self.assertTrue(turns[1].visible)
        self.assertEqual(
            [turn.text for turn in turns],
            ["Internal preset instruction", "Visible answer"],
        )

    def test_action_can_display_a_safe_label_while_storing_its_instruction(
        self,
    ) -> None:
        store = CardConversationStore()
        store.add_exchange(
            1,
            "Internal preset instruction",
            "Visible answer",
            presentation="action",
            display_text="Explain grammar",
        )

        action, answer = store.turns_for(1)
        self.assertEqual(action.text, "Internal preset instruction")
        self.assertEqual(action.display_text, "Explain grammar")
        self.assertEqual(action.presentation, "action")
        self.assertTrue(action.visible)
        self.assertEqual(answer.text, "Visible answer")

    def test_failed_action_is_retained_without_an_assistant_message(self) -> None:
        store = CardConversationStore()
        store.add_user_message(
            1,
            "Internal preset instruction",
            presentation="action",
            display_text="Explain grammar",
            state="failed",
        )

        (action,) = store.turns_for(1)
        self.assertEqual(action.text, "Internal preset instruction")
        self.assertEqual(action.display_text, "Explain grammar")
        self.assertEqual(action.state, "failed")

    def test_display_history_keeps_the_latest_twenty_pairs(self) -> None:
        store = CardConversationStore()
        for index in range(25):
            store.add_exchange(1, f"question-{index}", f"answer-{index}")

        turns = store.turns_for(1)
        self.assertEqual(len(turns), 40)
        self.assertEqual(turns[0].text, "question-5")
        self.assertEqual(turns[-1].text, "answer-24")

    def test_discard_removes_only_the_closed_card_conversation(self) -> None:
        store = CardConversationStore()
        store.add_exchange(1, "One", "First")
        store.add_exchange(2, "Two", "Second")

        store.discard(1)

        self.assertEqual(store.turns_for(1), ())
        self.assertEqual([turn.text for turn in store.turns_for(2)], ["Two", "Second"])
