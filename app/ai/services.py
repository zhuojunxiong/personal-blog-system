class AIService:
    """V0.2 only reserves AI extension points."""

    unavailable_message = "AI 功能将在后续版本开放。"

    def generate_summary(self, content):
        return self.unavailable_message

    def recommend_tags(self, content):
        return self.unavailable_message

    def polish_article(self, content):
        return self.unavailable_message

    def chat_with_article(self, article_id, question):
        return self.unavailable_message


ai_service = AIService()
