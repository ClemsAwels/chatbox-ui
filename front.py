import autogen
llm_config = {"model": "gpt-4o"}

task = '''
        Create a chatbot interface using React that allows users to send messages and receive responses in real-time. The chat interface should be visually appealing, user-friendly, and responsive on different devices. Write clean, well-structured code that follows best practices and adheres to modern front-end design principles. Focus on creating an intuitive layout, styling the chat messages, handling user input, and displaying bot responses. Ensure the chatbot interface is functional, interactive, and accessible to users of all levels.
        import React, { useState } from 'react';
        import './App.css';

        function App() {
        const [messages, setMessages] = useState([]);
        const [input, setInput] = useState('');

        const handleSend = () => {
            if (input.trim()) {
            setMessages([...messages, { sender: 'user', text: input }]);
            setInput('');

            // Simulate chatbot response
            setTimeout(() => {
                setMessages(prevMessages => [
                ...prevMessages,
                { sender: 'bot', text: `Vous avez dit : "${input}"` },
                ]);
            }, 500);
            }
        };

        return (
            <div className="App">
            <header className="App-header">
                <h1>Chatbot</h1>
                <div className="chat-container">
                <div className="chat-messages">
                    {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`chat-message ${msg.sender}`}
                    >
                        {msg.text}
                    </div>
                    ))}
                </div>
                <div className="chat-input">
                    <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Écrivez un message..."
                    />
                    <button onClick={handleSend}>Envoyer</button>
                </div>
                </div>
            </header>
            </div>
        );
        }

        export default App;

        .chat-container {
        display: flex;
        flex-direction: column;
        height: 80vh;
        width: 400px;
        margin: auto;
        border: 1px solid #ccc;
        border-radius: 8px;
        overflow: hidden;
        }

        .chat-messages {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
        background-color: #f9f9f9;
        }

        .chat-message {
        margin: 5px 0;
        padding: 10px;
        border-radius: 5px;
        }

        .chat-message.user {
        background-color: #d1e7dd;
        align-self: flex-end;
        }

        .chat-message.bot {
        background-color: #f8d7da;
        align-self: flex-start;
        }

        .chat-input {
        display: flex;
        padding: 10px;
        background-color: #fff;
        border-top: 1px solid #ccc;
        }

        .chat-input input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        }

        .chat-input button {
        margin-left: 10px;
        padding: 10px 20px;
        border: none;
        background-color: #007bff;
        color: white;
        border-radius: 4px;
        cursor: pointer;
        }

        .chat-input button:hover {
        background-color: #0056b3;
        }


       '''



writer = autogen.AssistantAgent(
    name="Code_writer",
    system_message="You are a front-end developer tasked with creating a chatbot interface using React. Your goal is to design and implement a chatbot UI that allows users to send messages and receive responses in real-time. The chat interface should be visually appealing, user-friendly, and responsive on different devices. You need to write clean, well-structured code that follows best practices and adheres to modern front-end design principles. Focus on creating an intuitive layout, styling the chat messages, handling user input, and displaying bot responses. Ensure the chatbot interface is functional, interactive, and accessible to users of all levels."
    "Your goal is to provide accurate, efficient, and well-documented code solutions that help developers understand and apply these technologies effectively. You must polish your writing based on the feedback you receive and provide a refined version. Only return your final work without additional comments."
,
    llm_config=llm_config,
)

reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])

print(reply)

critic = autogen.AssistantAgent(
    name="Code_critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a front-end UI code reviewer. You review the submitted front-end code and provide constructive feedback to help improve its styling, structure, and overall functionality. Your goal is to identify areas for improvement in the use of HTML, CSS, and JavaScript, suggest optimizations for design consistency, and offer guidance on best practices for creating clean, maintainable, and visually appealing code. Focus on aspects such as responsiveness, visual hierarchy, adherence to UI/UX principles, reusable styles, efficient layouts, and cross-browser compatibility. Your feedback should be clear, specific, and actionable, ensuring the code aligns with modern front-end and UI standards.",
)

res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

"""
Nested chat
"""

maximo_expert_reviewer = autogen.AssistantAgent(
    name="UI Expert Reviewer",
    llm_config=llm_config,
    system_message="You are a UI expert reviewer, specializing in front-end technologies such as HTML, CSS, and JavaScript. You have an in-depth understanding of modern UI/UX principles and are well-versed in leveraging the best front-end frameworks, libraries, and design patterns to create clean, minimalist, and highly functional interfaces. Your expertise includes evaluating and recommending the most effective components, layouts, and design systems to ensure clarity, responsiveness, and seamless user experiences. You excel in identifying areas for optimization, promoting reusable and modular code, and staying ahead of emerging trends to deliver visually appealing and efficient front-end solutions."
)

jython_expert_reviewer = autogen.AssistantAgent(
    name="React Expert Reviewer",
    llm_config=llm_config,
    system_message="You are a React expert reviewer, specializing in React, HTML, CSS, and JavaScript. You have a comprehensive understanding of modern front-end development, including component-based architecture, state management, and best practices for building scalable and maintainable applications. Your expertise extends to optimizing performance, ensuring responsive designs, and integrating accessible and user-friendly interfaces. You provide detailed code reviews, offering constructive feedback and actionable insights to enhance code quality, functionality, and adherence to industry standards. Focus on identifying inefficiencies, promoting reusable and modular components, and leveraging the latest advancements in the React ecosystem."
)

"""
Orchestrate the nested chats to solve the task
"""

def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

review_chats = [
    {
     "recipient": maximo_expert_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",},
     "max_turns": 1},
    {
    "recipient": jython_expert_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}.",},
     "max_turns": 1},
]

critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

"""
Get the summary
"""

print(res.summary)