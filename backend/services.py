class ChatService:
    def __init__(self):
        self.conversations = {}

    def get_history(self, user_id, conversation_id):
        return self.conversations.setdefault(
            (user_id, conversation_id), []
        )

    def process_message(self, user_id, conversation_id, message):
        history = self.get_history(user_id, conversation_id)
        
        history.append({"role": "user", "content": message})
        
        answer = "Hello! I'm Airi."
        
        history.append({"role": "assistant", "content": answer})
        
        return answer