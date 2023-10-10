import { conversationTree ,extractMessages} from './conversation_chatbot.js';
import { prompts,replies,alternative } from './constants_chatbot.js'

let currentConversationNode = conversationTree;
let userInput = "";

function sendMessage() {
  const inputField = document.getElementById("input");
  let input = inputField.value;
  inputField.value = "";
 // let currentConversationNode="";
 //console.log("User Input:", input);
 
  if (currentConversationNode.input) {
    userInput = input; // Store user input
    console.log(userInput)
    //output(currentConversationNode.message, currentConversationNode.options);
  } else if (currentConversationNode.nodes && currentConversationNode.nodes[input]) {
    // Transition to the next node based on user input
    currentConversationNode = currentConversationNode.nodes[input];
    output(currentConversationNode.message, currentConversationNode.options);
  }
}


document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("input");
  const sendButton = document.getElementById("sendButton");
  //const sendButton = document.querySelector('.send__button');
  //let userInput = "";

  //let currentConversationNode = conversationTree;
  output(currentConversationNode.message, currentConversationNode.options);

  inputField.addEventListener("keydown", (e) => {
    if (e.code === "Enter") {
      let input = inputField.value;
      inputField.value = "";
      // userInput = input;
      // console.log("Enter button",userInput)
      // updateChatAndConstructString(userInput)   

      const isValidInput = input.length === 2 && [...input].every(char => char.charCodeAt(0) >= 48 && char.charCodeAt(0) <= 57);
  
      if (isValidInput) {
        console.log("Enter button", userInput);
        updateChatAndConstructString(userInput);
        output(input);
      } else {
        processInput(input);
      }
    }
  });

  //const sendButton = document.getElementById("sendButton");

  sendButton.addEventListener("click", () => {
    let input = inputField.value;
    inputField.value = "";
    sendMessage(input); // Call sendMessage function with the user's input
  });
});

function processInput(input) {
  let product;

  // Regex remove non word/space chars
  // Trim trailing whitespce
  // Remove digits - not sure if this is best
  // But solves problem of entering something like 'hi1'

  let text = input.toLowerCase().replace(/[^\w\s]/gi, "").replace(/[\d]/gi, "").trim();
  text = text
    .replace(/ a /g, " ")   // 'tell me a story' -> 'tell me story'
    .replace(/i feel /g, "")
    .replace(/whats/g, "what is")
    .replace(/please /g, "")
    .replace(/ please/g, "")
    .replace(/r u/g, "are you");

  if (compare(prompts, replies, text)) { 
    // Search for exact match in `prompts`
    product = compare(prompts, replies, text);
  } else if (text.match(/thank/gi)) {
    product = "You're welcome!"
  } //else if (text.match(/(corona|covid|virus)/gi)) {
    // If no match, check if message contains `coronavirus`
    //product = coronavirus[Math.floor(Math.random() * coronavirus.length)];
   else {
    // If all else fails: random alternative
    product = alternative[Math.floor(Math.random() * alternative.length)];
  }

  // Update DOM
  addChatMessages(input, product);
  output(currentConversationNode.message, currentConversationNode.options);
}


function output(message, options) {
  const messagesContainer = document.getElementById("messages");
  let botDiv = document.createElement("div");
  let botText = document.createElement("span");
  botDiv.id = "bot";
  botDiv.className = "bot response";
  botText.innerText = "Typing...";
  botDiv.appendChild(botText);
  messagesContainer.appendChild(botDiv);

  setTimeout(() => {
    botText.innerText = message;
   //userInput = message;
    //console.log(userInput);
    

  if (options) {
    let optionsDiv = document.createElement("div");
    optionsDiv.id = "options";
    optionsDiv.className = "options response";

    for (const option of options) {
      let optionButton = document.createElement("button");
      optionButton.textContent = option.text;
      optionButton.className = "chatbox__option";
      optionButton.addEventListener("click", () =>
        handleOptionClick(option.next, option.identifier)
      );
      optionsDiv.appendChild(optionButton);
    }

    messagesContainer.appendChild(optionsDiv);
  }

  
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }, 1000);
}

let selectedVerticalIdentifier = "";
let selectedBuildingIdentifier = "";
let selectedFloorIdentifier = "";
//let selectedNodeIdentifier = "";

function handleOptionClick(nextNode, identifier) {
  currentConversationNode = conversationTree.nodes[nextNode];

  if (identifier) {
    if (currentConversationNode === conversationTree.nodes.NodeSp) {
      selectedVerticalIdentifier = identifier;
    } else if (currentConversationNode === conversationTree.nodes.FloorNode) {
      selectedBuildingIdentifier = identifier;
    } else if (currentConversationNode === conversationTree.nodes.FinalNode) {
      selectedFloorIdentifier = identifier;
      //updateChatAndConstructString(userInput);
    }
    // else{
    //   userInput = input;
    // }
    // else if (currentConversationNode === conversationTree.nodes.CommonNode) {
    //   selectedNodeIdentifier = userInput;
    //   console.log("if condition",selectedNodeIdentifier)
    // }
  }

  // if (nextNode === "CommonNode") {
  //   // If transitioning to the FinalNode, capture the entered node ID
  //   selectedNodeIdentifier = userInput;
  //   console.log(selectedNodeIdentifier)
  // }

  // Update the chat and construct the concatenated string
  //updateChatAndConstructString();

  // Continue with displaying messages and options
  addChat(currentConversationNode.message, currentConversationNode.options);
}

function updateChatAndConstructString(updateduserInput) {
  
    // Construct the concatenated string based on selected identifiers
  //const finalString = `${selectedVerticalIdentifier}-${selectedBuildingIdentifier}${selectedFloorIdentifier}-${selectedNodeIdentifier}`;
  //console.log("Inside function",updateduserInput)
  const firstString = `AE-${selectedVerticalIdentifier}`;
  const finalString = `${selectedVerticalIdentifier}-${selectedBuildingIdentifier}${selectedFloorIdentifier}-${updateduserInput}`;
  // Update the chat or display the finalString wherever you want
  // For example, you can display it in the chatbox:
  console.log("First String:", firstString);
  console.log("Second String:", finalString);
  const apiUrl = `http://localhost:4000/data/${firstString}/${finalString}`;
  console.log("API URL:", apiUrl);
  if (currentConversationNode === conversationTree.nodes.FinalNode) {
    fetchExternalData(apiUrl, finalString);
  }
  
  // const messagesContainer = document.getElementById("messages");
  // let finalStringDiv = document.createElement("div");
  // let finalStringText = document.createElement("span");
  // finalStringDiv.id = "finalString";
  // finalStringDiv.className = "final-string response";
  // finalStringText.innerText = `Constructed String: ${finalString}`;
  // finalStringDiv.appendChild(finalStringText);
  // messagesContainer.appendChild(finalStringDiv);
}

function fetchExternalData(url,input) {
  var myHeaders = new Headers();
  myHeaders.append("X-M2M-Origin", "iiith_guest:iiith_guest");
  myHeaders.append("Accept", "application/json");

  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

  fetch(url, requestOptions)
    .then(response => response.json())
    .then(result => {
      
      printFetchedData(result,input);
    }
      )
    .catch(error => console.log('error', error));
}

function printFetchedData(data,input) {
  // Convert the data to a JSON string for printing
  const dataString = JSON.stringify(data, null, 2);
  const parsedData = JSON.parse(dataString);
  //const modifiedData = { ...parsedData };
  // if (parsedData['Timestamp']) {
  //   const timestamp = new Date(parsedData['Timestamp'] * 1000);
  //   const formattedTimestamp = `${timestamp.toLocaleDateString()} ${timestamp.toLocaleTimeString()}`;
  //   parsedData['Timestamp'] = formattedTimestamp;
  // }

  // Construct the formatted data string
  let formattedData = '';
  for (const key in data) {
          if (Object.prototype.hasOwnProperty.call(data, key)) {
            if(key=== "Timestamp'"){
      
              const epochTimestamp =data[key];
              const normalTime =new Date(epochTimestamp *1000).toLocaleString();
              formattedData += `${key.replace("'", '')}: ${normalTime}\n`;
            }
            else{
           
              formattedData += `${key.replace("'", '')}: ${parsedData[key]}\n`;
          }}
  }
  // for (const key in parsedData) {
  //   formattedData += `${key.replace("'", '')}: ${parsedData[key]}\n`;
  // }

  // Print the formatted data in the chatbox
  addChatMessages(input, formattedData);
}

// function printFetchedData(data, input) {
//     let formattedData = "";
  
//     for (const key in data) {
//       if (Object.prototype.hasOwnProperty.call(data, key)) {
//         if(key=== "Timestamp'"){
  
//           const epochTimestamp =data[key];
//           const normalTime =new Date(epochTimestamp *1000).toLocaleString();
//           formattedData += `${key}: ${normalTime}\n`;
//         }
//         else{
       
//         formattedData += `${key}: ${data[key]}\n`;
//       }}
//     }
  
//     addChat(input, formattedData);
//   }
  
  
function compare(promptsArray, repliesArray, string) {
  let reply;
  let replyFound = false;
  for (let x = 0; x < promptsArray.length; x++) {
    for (let y = 0; y < promptsArray[x].length; y++) {
      if (promptsArray[x][y] === string) {
        let replies = repliesArray[x];
        reply = replies[Math.floor(Math.random() * replies.length)];
        replyFound = true;
        // Stop inner loop when input value matches prompts
        break;
      }
    }
    if (replyFound) {
      // Stop outer loop when reply is found instead of interating through the entire array
      break;
    }
  }
  return reply;
}

function addChat(message, options) {
  const messagesContainer = document.getElementById("messages");

  let botDiv = document.createElement("div");
  let botText = document.createElement("span");
  botDiv.id = "bot";
  botDiv.className = "bot response";
  botText.innerText = "Typing...";
  botDiv.appendChild(botText);
  messagesContainer.appendChild(botDiv);

  // Simulate bot typing delay
  setTimeout(() => {
    botText.innerText = message;
    if (options) {
      let optionsDiv = document.createElement("div");
      optionsDiv.id = "options";
      optionsDiv.className = "options response";

      for (const option of options) {
        let optionButton = document.createElement("button");
        optionButton.textContent = option.text;
        optionButton.className = "chatbox__option";
        optionButton.addEventListener("click", () => handleOptionClick(option.next, option.identifier));
        optionsDiv.appendChild(optionButton);
      }

      messagesContainer.appendChild(optionsDiv);
    }
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }, 1000);
}



function addChatMessages(input, product) {
  const messagesContainer = document.getElementById("messages");

  let userDiv = document.createElement("div");
  userDiv.id = "user";
  userDiv.className = "user response";
  userDiv.innerHTML = `<span>${input}</span>`;
  messagesContainer.appendChild(userDiv);

  let botDiv = document.createElement("div");
  let botImg = document.createElement("img");
  let botText = document.createElement("span");
  botDiv.id = "bot";
  //botImg.src = "images/bot-mini.png";
  //botImg.className = "avatar";
  botDiv.className = "bot response";
  botText.innerText = "Typing...";
  botDiv.appendChild(botText);
  botDiv.appendChild(botImg);
  messagesContainer.appendChild(botDiv);
  // Keep messages at most recent
  messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;

  // Fake delay to seem "real"
  setTimeout(() => {
    botText.innerText = `${product}`;
    //textToSpeech(product)
  }, 2000
  )

}
// Used to get the popup open and close 

class Chatbox {
  constructor() {
      this.args = {
          openButton: document.querySelector('.chatbox__button'),
          chatBox: document.querySelector('.chatbox__support'),
          sendButton: document.querySelector('.send__button'),
          minimizeButton: document.querySelector('.minimize-btn'), // New minimize button



      };
      

      this.state = false;
      this.messages = [];
  }

  display() {
      const {openButton, chatBox, sendButton,minimizeButton} = this.args;
      
      
      openButton.addEventListener('click', () => this.toggleState(chatBox));
      minimizeButton.addEventListener('click', () => this.toggleState(chatBox)); // Minimize button event listener
      sendButton.addEventListener('click', () => this.onSendButton(chatBox));

      const node = chatBox.querySelector('input');
      node.addEventListener("keyup", ({key}) => {
          if (key === "Enter") {
              this.onSendButton(chatBox);
          }
      });
  }

  toggleState(chatbox) {
      this.state = !this.state;

      // show or hides the box
      if(this.state) {
          chatbox.classList.add('chatbox--active')
      } else {
          chatbox.classList.remove('chatbox--active')
      }
  }

  onSendButton(chatbox) {
      var textField = chatbox.querySelector('input');
      let text1 = textField.value.trim();
      if (text1 === "") {
          return;
      }

      let msg1 = { name: "User", message: text1 }
      this.messages.push(msg1);

      fetch('/predict', {
          method: 'POST',
          body: JSON.stringify({ message: text1 }),
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json'
          },
        })
        .then(r => r.json())
        .then(r => {
          let msg2 = { name: "Sam", message: r.answer };
          this.messages.push(msg2);
          this.updateChatText(chatbox)
          textField.value = ''

      }).catch((error) => {
          console.error('Error:', error);
          this.updateChatText(chatbox)
          textField.value = ''
        });
  }

  updateChatText(chatbox) {
      var html = '';
      this.messages.slice().reverse().forEach(function(item, index) {
          if (item.name === "Sam")
          {
              html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
          }
          else
          {
              html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
          }
        });

      const chatmessage = chatbox.querySelector('.chatbox__messages');
      chatmessage.innerHTML = html;
  }
}


const chatbox = new Chatbox();
chatbox.display();