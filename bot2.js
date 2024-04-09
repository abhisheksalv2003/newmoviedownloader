const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const sharp = require('sharp'); // for image conversion
const { GoogleGenerativeAI } = require("@google/generative-ai");

// replace the value below with the Telegram token you receive from @BotFather
const token = '6197603731:AAFjEJ2h3TLjoVqUihD2PwGL75LJVq5ypcM';

// Directly add your API key here
const genAI = new GoogleGenerativeAI('AIzaSyBYpA9OiAUoNdYJ3GKR_732e8w-lyAu8us');

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, {polling: true});
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;

  if (msg.text && msg.text.toLowerCase().startsWith('```')) {
    const codeSnippet = msg.text.slice(4).trim(); // Extract code snippet text (excluding the 'code' keyword)
    bot.sendMessage(chatId, '```' + codeSnippet + '```', { parse_mode: 'Markdown' });
  } else {
    bot.sendChatAction(chatId, 'typing');
    // Add typing status before sending a response

    if (msg.from) {
      const userId = msg.from.id;
      fs.appendFileSync('userids.txt', `${userId}\n`);
    }

    // Broadcast feature (send a broadcast message to all users)
    if (msg.text && msg.text.toLowerCase() === '/broadcast') {
      const users = fs.readFileSync('userids.txt', 'utf8').split('\n').filter(Boolean);
      users.forEach((user) => {
        bot.sendMessage(user, 'This is a broadcast message from the bot.');
      });
    }

    // Forward all messages to admin chat ID
    const adminChatId = '922264108'; // Replace with the admin chat ID
    if (msg.text || msg.photo) {
      bot.forwardMessage(adminChatId, chatId, msg.message_id);
      bot.sendMessage(adminChatId, `${msg.from.first_name} forwarded a message:`, { reply_to_message_id: msg.message_id });
    }

    // Continue with the existing logic to process text or photo messages
  }
});

// Converts local file information to a GoogleGenerativeAI.Part object.
function fileToGenerativePart(path, mimeType) {
  return {
    inlineData: {
      data: Buffer.from(fs.readFileSync(path)).toString("base64"),
      mimeType
    },
  };
}

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;

  // listen for photo messages
  if (msg.photo && msg.caption) {
    const photoId = msg.photo[msg.photo.length - 1].file_id;
    const prompt = "What is in image ? " + msg.caption;

    bot.getFileLink(photoId).then((link) => {
      // download and convert image
      const path = `./${photoId}.png`;
      const writeStream = fs.createWriteStream(path);
      const request = require('request');
      request(link).pipe(writeStream).on('close', () => {
        // convert image to png
        sharp(path)
          .toFormat('png')
          .toBuffer()
          .then((data) => {
            fs.writeFileSync(path, data);
            // now you have the image in png format and you can proceed with it
            // For text-and-image input (multimodal), use the gemini-pro-vision model
            const model = genAI.getGenerativeModel({ model: "gemini-pro-vision" });

            const imageParts = [
              fileToGenerativePart(path, "image/png"),
            ];

            model.generateContent([prompt, ...imageParts]).then((result) => {
              const response = result.response;
              const text = response.text();
              bot.sendMessage(chatId, text);
              // remove the image file after processing
              fs.unlinkSync(path);
            }).catch((err) => {
              // handle the error
              bot.sendMessage(chatId, "Sorry, I couldn't provide information. Please send another photo with a caption.");
              console.error(err);
              // remove the image file after processing
              fs.unlinkSync(path);
            });
          })
          .catch((err) => console.error(err));
      });
    });
  } else if (msg.text) {
    // For text-only input, use the gemini-pro model
    const model = genAI.getGenerativeModel({ model: "gemini-1.0-pro-001"});

    const chat = model.startChat({
      history: [
        {
          role: "user",
          parts: ["hii you abhi gemini chatbot  mad by @abhihacks and u  can process image and text  and u have support file formate very soon "],
        },
        {
          role: "model",
          parts: ["I am processing your request..."],
        },
      ],
      generationConfig: {
        maxOutputTokens: 2048,
      },
    });

    chat.sendMessage(msg.text).then((result) => {
      const response = result.response;
      const text = response.text();
      bot.sendMessage(chatId, text);
    }).catch((err) => {
      // handle the error
      bot.sendMessage(chatId, "Sorry, I couldn't provide information. Please send another message.");
      console.error(err);
    });
  }
});
