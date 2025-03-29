import google.generativeai as genai

genai.configure(api_key="")

def analyze_articles_with_gemini(articles):


    generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }


    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction = """
    You are an AI assistant tasked with analyzing a set of articles and extracting the most important insights. Your goal is to identify key points, trends, and actionable information from the articles. Follow these steps:

    1. **Read and Understand**: Carefully analyze each article to identify the main ideas, key facts, and any notable trends or patterns.
    2. **Extract Insights**: Focus on extracting insights such as:
    - Key statistics or data points.
    - Emerging trends or patterns.
    - Important opinions or arguments.
    - Actionable recommendations or conclusions.
    3. **Organize the Output**: Present the insights in a structured format:
    - Use bullet points for clarity.
    - Group related insights under relevant headings (e.g., 'Trends', 'Statistics', 'Recommendations').
    - Order the insights by importance, with the most critical points at the top.
    4. **Be Concise**: Keep the output concise and avoid unnecessary details.
    5. Make sure you only type your insights, do not say anything else.
    """)

    chat_session = model.start_chat(
    history=[
    ]
    )

    prompt = ''

    for article in articles:
                prompt += f"Title: {article['title']}\nSource: {article['source']}\n\n"

    response = chat_session.send_message(prompt)


    return response.text




def analyze_posts_with_ai( posts):


    generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }


    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction = """
    You are an AI assistant tasked with analyzing a set of media posts and extracting the most important insights related to disasters. Your goal is to identify key points, trends, and actionable information from the posts. Follow these steps:

    1. **Read and Understand**: Carefully analyze each media post to identify the main ideas, key facts, and any notable trends or patterns related to disasters.
    2. **Extract Insights**: Focus on extracting insights such as:
    - Key details about the disaster (e.g., type, location, severity).
    - Emerging trends or patterns (e.g., frequency, impact, response efforts).
    - Important opinions, warnings, or calls to action from authorities or communities.
    - Actionable recommendations or conclusions (e.g., preparedness, relief efforts, mitigation strategies).
    3. **Organize the Output**: Present the insights in a structured format:
    - Use bullet points for clarity.
    - Group related insights under relevant headings (e.g., 'Disaster Details', 'Trends', 'Response Efforts', 'Recommendations').
    - Order the insights by importance, with the most critical points at the top.
    4. **Be Concise**: Keep the output concise and avoid unnecessary details.
    5. Make sure you only type your insights, do not say anything else.
    """)

    chat_session = model.start_chat(
    history=[
    ]
    )

    prompt = ''

    for post in posts:
        prompt += f"Title: {post['text']}\n\n"

    response = chat_session.send_message(prompt)


    return response.text







def generate_evacuation_plan_with_gemini(disaster_info, news_info, social_media):
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 30,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=f"""
        You are an AI assistant tasked with generating a detailed evacuation plan based on disaster information, news updates, and social media reports. Your goal is to create a clear, actionable, and structured evacuation plan. Follow these steps:

        1. **Analyze Input Data**: Carefully review the disaster information, news updates, and social media reports to understand the situation.
        2. **Identify Key Details**: Extract critical information such as:
           - Type and severity of the disaster.
           - Affected areas and populations.
           - Current conditions (e.g., weather, infrastructure damage).
           - Available resources (e.g., shelters, transportation).
           - Urgent risks or hazards.
        3. **Formulate Evacuation Plan**: Create a structured evacuation plan that includes:
           - **Priority Zones**: Identify areas that need immediate evacuation.
           - **Evacuation Routes**: Suggest safe and efficient routes for evacuation.
           - **Shelter Locations**: List nearby shelters or safe zones.
           - **Resource Allocation**: Recommend how resources (e.g., food, water, medical supplies) should be distributed.
           - **Communication Plan**: Suggest methods for disseminating information to affected populations.
        4. **Be Clear and Concise**: Use bullet points and headings for clarity. Avoid unnecessary details.
        5. **Focus on Actionability**: Ensure the plan is practical and easy to implement.
        6. Do not use * in your answer and do not say anything in the beginning like "Okay depending on my.." just state what you want to say

        This is the Disaster info: {disaster_info}

        These are some news articles related to it: {news_info}

        """
    )

    chat_session = model.start_chat(history=[])


    prompt = (
        f"Disaster Information:\n{disaster_info}\n\n"
        f"News Updates:\n{news_info}\n\n"
        f"Social Media Reports:\n{social_media}\n\n"
        "Based on the above information, generate a detailed evacuation plan."
    )

    response = chat_session.send_message(prompt)
    return response.text