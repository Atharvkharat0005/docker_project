FROM ollama/ollama

# Start server, wait, pull model, then keep server running
RUN ollama serve & sleep 5 && ollama pull gemma3:1b