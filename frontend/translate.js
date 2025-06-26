const API_URL = 'https://0lx9vu4du8.execute-api.us-east-1.amazonaws.com/getPresignedUploadURL';

document.getElementById("translateForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const inputText = document.getElementById("englishText").value.trim();
  if (!inputText) return alert("Please enter text to translate.");

  const sourceLang = document.getElementById("sourceLang").value;
  const targetLang = document.getElementById("targetLang").value;

  const inputData = {
    source_language_code: sourceLang,
    target_language_code: targetLang,
    text_list: [inputText]
  };

  try {
    // Step 1: Get pre-signed S3 upload URL
    const response = await fetch(API_URL, { method: 'POST' });
    const { upload_url, file_key } = await response.json();

    // Step 2: Upload input JSON to S3
    const uploadResponse = await fetch(upload_url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputData)
    });

    if (!uploadResponse.ok) {
      throw new Error("Failed to upload JSON to S3");
    }

    // Step 3: Poll for translated file
    const responseBucket = 'translate-response-bucket-311141533760';
    const translatedKey = file_key.replace(".json", "_translated.json");
    const translatedUrl = `https://${responseBucket}.s3.amazonaws.com/${translatedKey}`;

    let attempts = 0;
    const maxAttempts = 10;
    const delay = 3000; // 3 seconds

    const pollForResult = async () => {
      try {
        const result = await fetch(translatedUrl);
        if (result.ok) {
          const translatedData = await result.json();
          document.getElementById("outputText").textContent = translatedData.translated[0];
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(pollForResult, delay);
        } else {
          document.getElementById("outputText").textContent = "❌ Translation timed out.";
        }
      } catch (fetchError) {
        document.getElementById("outputText").textContent = "❌ Failed to fetch translated result.";
        console.error("Polling error:", fetchError);
      }
    };

    document.getElementById("outputText").textContent = "⏳ Translating...";
    pollForResult();

  } catch (err) {
    console.error("Error:", err);
    document.getElementById("outputText").textContent = "❌ Something went wrong.";
  }
});
