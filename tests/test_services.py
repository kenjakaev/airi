from backend.services import ChatService


def test_process_message():
    service = ChatService()

    answer = service.process_message(
        user_id="user_1",
        conversation_id="chat_1",
        message="Hi, Airi!",
    )

    history = service.conversations[("user_1", "chat_1")]

    assert answer == "Hello! I'm Airi."
    assert len(history) == 2

    assert history[0] == {
        "role": "user",
        "content": "Hi, Airi!",
    }

    assert history[1] == {
        "role": "assistant",
        "content": "Hello! I'm Airi.",
    }

def test_conversation_history():
    service = ChatService()

    service.process_message("user_1", "chat_1", "Hello!")
    service.process_message("user_1", "chat_1", "How are you?")

    history = service.conversations[("user_1", "chat_1")]

    assert len(history) == 4
    assert history[0]["content"] == "Hello!"
    assert history[2]["content"] == "How are you?"

def test_user_isolation():
    service = ChatService()

    service.process_message("user_1", "chat_1", "Hello!")
    service.process_message("user_2", "chat_1", "Hi!")

    history_1 = service.conversations[("user_1", "chat_1")]
    history_2 = service.conversations[("user_2", "chat_1")]

    assert history_1 != history_2
    assert history_1[0]["content"] == "Hello!"
    assert history_2[0]["content"] == "Hi!"