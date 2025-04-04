import React, { useState } from "react";
import { uploadImage } from "../api";

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file.");
      return;
    }
    try {
      setMessage("Uploading...");
      const response = await uploadImage(file);
      setMessage(`Upload successful: ${response.image_path}`);
    } catch (error) {
      setMessage("Upload failed. Please try again.");
    }
  };

  return (
    <div>
      <h2>Upload Image</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Upload;
