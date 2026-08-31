(() => {
  if (window.__ankiAIWorkspaceReviewerBridgeInstalled) {
    return;
  }
  window.__ankiAIWorkspaceReviewerBridgeInstalled = true;

  let observer;
  const activateCurrentCard = () => {
    const source = document.querySelector("#anki-ai-workspace-client");
    if (!source || source.dataset.ankiAIWorkspaceActivated) {
      return Boolean(source);
    }

    source.dataset.ankiAIWorkspaceActivated = "true";
    const client = document.createElement("script");
    client.textContent = source.textContent;
    document.head.appendChild(client);
    client.remove();
    return true;
  };

  // Reviewer can replace question HTML with answer HTML in the same document.
  // Keep observing so every replacement client is activated exactly once.
  observer = new MutationObserver(activateCurrentCard);
  observer.observe(document.documentElement, { childList: true, subtree: true });
  activateCurrentCard();
})();
