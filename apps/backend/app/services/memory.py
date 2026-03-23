chat_history = []


def add_to_memory(query, response):
    """
    Add a query and its corresponding response to the chat memory.

    Args:
        query (str): The user's query.
        response (str): The AI's response to the query.
    """
    chat_history.append({"query": query, "response": response})


def get_memory():
    """
    Retrieve the chat history memory.

    Returns:
        list: A list of dictionaries containing past queries and responses.
    """
    return chat_history[-3:]  # Return the last 3 interactions for context
