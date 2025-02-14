const readline = require("readline");
const axios = require("axios");
const marked = require("marked"); // Import marked library
require("dotenv").config();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const chatHistory = [];

function loadChatHistory() {
  const chatHistoryStr = process.env.CHAT_HISTORY || "[]";
  return JSON.parse(chatHistoryStr);
}

function saveChatHistory(chatHistory) {
  process.env.CHAT_HISTORY = JSON.stringify(chatHistory);
}

async function generateAIResponse(promptText, selectedModel) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("API key is missing. Check your .env file.");
  }

  const url = `https://generativelanguage.googleapis.com/v1/models/${selectedModel}:generateContent?key=${apiKey}`;
  const headers = { "Content-Type": "application/json" };
  const data = {
    contents: [
      {
        parts: [
          {
            text: promptText,
          },
        ],
      },
    ],
  };

  try {
    const response = await axios.post(url, data, { headers });
    if (response.status === 200) {
      const responseJson = response.data;
      try {
        let aiResponse = responseJson.candidates[0].content.parts[0].text;
        // Handle responses containing "****"
        if (aiResponse.includes("****")) {
          aiResponse = aiResponse.replace("****", "[censored]");
        }
        // Ensure proper encoding
        aiResponse = decodeURIComponent(escape(aiResponse));
        
        // Ensure the response is focused on God, Bible, and motivation
        if (!["god", "bible", "verse", "motivation", "faith", "holy"].some(keyword => aiResponse.toLowerCase().includes(keyword))) {
          aiResponse = "Hello, I can only assist you with topics related to God, Bible verses, and motivation. How can I help you in that regard?";
        }
        
        // Parse the response with marked to handle Markdown syntax
        aiResponse = marked(aiResponse);
        
        return aiResponse;
      } catch (error) {
        return "Error: Unexpected response format.";
      }
    } else {
      return `Error: ${response.status} - ${response.statusText}`;
    }
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

function buildPrompt() {
  const systemPrompt =
    "You are a versatile AI assistant. You can help with a wide variety of topics about GOD, bible verse and motivation according to mood.";
  const promptSequence = [systemPrompt];
  const messageLog = loadChatHistory();
  for (const msg of messageLog) {
    if (msg.role === "user") {
      promptSequence.push(`User: ${msg.content}`);
    } else if (msg.role === "ai") {
      promptSequence.push(`✞: ${msg.content}`);
    }
  }
  return promptSequence.join("\n");
}

async function main() {
  console.log("Welcome to Your AI Assistant");
  const selectedModel = "gemini-1.5-pro"; // Default model, you can change this as needed

  while (true) {
    const userQuery = await new Promise((resolve) =>
      rl.question("You: ", resolve)
    );
    if (
      userQuery.toLowerCase() === "exit" ||
      userQuery.toLowerCase() === "quit"
    ) {
      break;
    }

    // Add user message to log
    chatHistory.push({ role: "user", content: userQuery });
    saveChatHistory(chatHistory);

    // Generate AI response
    const promptText = buildPrompt();
    const aiResponse = await generateAIResponse(promptText, selectedModel);

    // Add AI response to log
    chatHistory.push({ role: "ai", content: aiResponse });
    saveChatHistory(chatHistory);

    console.log(`AI: ${aiResponse}`);
  }

  rl.close();
}

main();
