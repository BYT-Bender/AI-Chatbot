import os

def check_files_and_directories():
    target_directory = 'D:/Files/Python/AI/CURRENT_VER/'  # Parent Directory

    expected_files_and_directories = [
        'chatbot.py',
        'config.json',
        'gui.py',
        'index.html',
        'requirements.txt',
        'server.py',
        'assets',
        'assets/admin_commands.py',
        'assets/analize.py',
        'assets/formatting.py',
        'assets/utilities.py',
        'assets/data',
        'assets/data/admin_commands.json',
        'assets/data/command_usage.csv',
        'assets/data/conversation_response_usage.csv',
        'assets/data/response_usage.csv',
        'assets/data/unrecognized.csv',
        'assets/responses',
        'assets/responses/calculation',
        'assets/responses/calculation/solve_expression.py',
        'assets/responses/conversation',
        'assets/responses/conversation/intents.json',
        'assets/responses/conversation/search_conversation.py',
        'assets/responses/dictionary',
        'assets/responses/dictionary/dictionary.json',
        'assets/responses/dictionary/word_definition.py',
        'assets/responses/elements',
        'assets/responses/elements/elements.json',
        'assets/responses/elements/intents.json',
        'assets/responses/elements/search_element.py',
        'assets/responses/elements/units.json',
        'assets/responses/wikipedia',
        'assets/responses/wikipedia/search_wikipedia.py',
        'assets/server',
        'assets/server/mark_pp.avif',
        'assets/server/stella_pp.webp',
        'assets/server/style.css',
        'dataset',
        'dataset/elements',
        'dataset/elements/__pycache__',
        'dataset/elements/__pycache__/response.cpython-311.pyc',
        'dataset/paradoxes',
        'dataset/paradoxes/paradoxes.json',
        'discord',
        'discord/.env',
        'discord/bot.py',
        'documentation',
        'documentation/Chatbot.md',
        'documentation/TextStyle.md',
        'log',
        'log/log_app.txt',
        'log/log_CL.txt',
        'log/log_discord.txt',
        'log/log_web.txt',
        'log/error.log',
        'test',
        'test/log.md',
        'test/gui',
        'test/gui/chatbot_gui.py',
        'test/gui/chatbot_modern_gui.py',
    ]

    missing_files_and_directories = []

    for item in expected_files_and_directories:
        path = os.path.join(target_directory, item)
        if not os.path.exists(path):
            missing_files_and_directories.append(path)

    if not missing_files_and_directories:
        print("All files and directories are present.")
    else:
        print("Missing files and directories:")
        for item in missing_files_and_directories:
            print(item)

if __name__ == '__main__':
    check_files_and_directories()
