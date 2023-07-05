const app = Vue.createApp({
  data() {
    return {
      userQuery: '',
      chatHistory: [],
      fileName: ''
    };
  },
  created() {
      // Call the backend function automatically when the chatbot is opened
      chrome.runtime.sendMessage({ action: "getCurrentTabUrl" }, (response) => {
        // Call the backend API to perform any initial action based on the tabUrl (if needed)
        fetch(`http://localhost:8000/scrap?tabUrl=${response.url}`)
            .then(r => console.info("data stored...")
        );
      });
    },
  methods: {
    submitQuery() {
      if (this.userQuery.trim() === '') {
        return;
      }

      chrome.runtime.sendMessage({ action: "getCurrentTabUrl" }, (response) => {
        const tabUrl = response.url;

        // Add the user query to the chat history
        this.chatHistory.push({ id: Date.now(), text: this.userQuery });

        // Call the backend API and handle the response
        const keyword = this.userQuery;
        fetch(`http://localhost:8000/search?tabUrl=${tabUrl}&keyword=${keyword}`)
          .then(response => response.json())
          .then(data => {
            const botResponse = data;
            // Add the bot response to the chat history
            this.chatHistory.push({ id: Date.now(), text: botResponse });
          })
          .catch(error => {
            console.error('Error:', error);
          });

        this.userQuery = '';
      });
    },
    handleDownload() {
      // Get the search query from the user input field
      const fileName = this.fileName;
      console.info(fileName)
      chrome.runtime.sendMessage({ action: "getCurrentTabUrl" }, function(response) {
        const url = response.url
        // Make a GET request to the backend API
        fetch(`http://localhost:8000/download?tabUrl=${url}&fileName=${fileName}`)
        .then(async response => {
          if (response.ok) {
            // Get the filename from the Content-Disposition header
            const blob = await response.blob();
            // Create a URL for the blob
            const url = URL.createObjectURL(blob);
            // Create a temporary link element
            const link = document.createElement('a');
            link.href = url;
            link.download = `${fileName}.txt`;
            // Programmatically click the link to initiate the download
            link.click();
            // Clean up the temporary link and URL object
            URL.revokeObjectURL(url);
            link.remove();
          } else {
            throw new Error('Failed to download file');
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      });
    }
  }
});

app.mount('#app');
