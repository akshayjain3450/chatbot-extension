// Listen for messages from the popup script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "getCurrentTabUrl") {
    // Query the current active tab
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      var currentTabUrl = tabs[0].url;
      // Send the URL back to the popup script
      sendResponse({ url: currentTabUrl });
    });

    // Return true to indicate that the response will be sent asynchronously
    return true;
  }
});
